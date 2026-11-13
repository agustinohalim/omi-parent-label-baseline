"""Fase C OMI (Prareg_OMI_C.md, terkunci 13 Nov 2026): uji ukur kriteria STEMI dan latih ulang di dalam infark.

Masukan di luar repo ($OMI_DATA/): csv/CSV/train.csv, ciri_st_train.csv, med/med_data/<id>.med,
oof_m01.csv, oof_m2_utama.npz, oof_m3a.npz, emb_ecgfounder_train.npy.

C1  aturan STEMI K2 (titik J) dan varian J + 60 ms lawan diagnosis STEMI pulang; per kuartil Time_Interval.
C2  tiga AUROC berpasangan (OMI / AMI tanpa OMI / tanpa AMI) untuk skor OMI kohort penuh.
C3  latih ulang M0, M1, probe ECGFounder di dalam AMI=1 dan STEMI=1 (prosedur fase A).
C4  M3a dilatih ulang di NSTEMI (pra-daftar asli): net benefit 1–40 %, EKG di bawah ambang, rentang 1–60 %.
C5  karakteristik per kelompok (Tabel 1 baru).

Pakai: python-gpu analysis/omi_fase_c.py [--B 2000] [--butir C1,C2,C3,C4,C5]
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, CIRI_ST, indeks_bootstrap, metrik, oof, ringkas  # noqa: E402
from omi_ciri_st import SADAPAN, baca_med, deteksi  # noqa: E402
from omi_konstruk import ambang_v23, cetak, muat, nb, sel  # noqa: E402

PASANGAN = [("II", "III"), ("II", "aVF"), ("III", "aVF"), ("I", "aVL")] + \
           [(f"V{k}", f"V{k + 1}") for k in range(1, 6)]
AMBANG_C4 = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]


def ambang_sadapan(gen, usia):
    laki = (gen == 1)
    u = float(usia) if pd.notna(usia) else 99.0
    return np.array([ambang_v23(laki, u) if s in ("V2", "V3") else 0.10 for s in SADAPAN])


def aturan(st_mv, ab):
    """st_mv, ab: (12,) mV. Kembalikan (positif, elevasi pasangan terbesar di atas ambang)."""
    idx = {s: i for i, s in enumerate(SADAPAN)}
    lebih = st_mv - ab
    m = max(min(lebih[idx[a]], lebih[idx[b]]) for a, b in PASANGAN)
    return int(m >= 0), m


def c1(ut):
    print("## C1. Aturan STEMI otomatis lawan diagnosis STEMI pulang\n")
    st = pd.read_csv(AKAR / "ciri_st_train.csv").set_index("ecg_med_record")
    n = len(ut)
    rj, rj60, mj = np.zeros(n, int), np.zeros(n, int), np.full(n, np.nan)
    for r, (rec, gen, usia) in enumerate(zip(ut.ecg_med_record, ut.gender, ut.age)):
        if st.status.loc[rec] != "ok":  # sama dengan K2: gagal -> negatif
            continue
        ab = ambang_sadapan(gen, usia)
        x = baca_med(AKAR / "med/med_data" / rec)
        _, awal, j = deteksi(x)
        pr = x[:, awal - 15:awal - 5].mean(axis=1)
        rj[r], mj[r] = aturan((x[:, j] - pr) / 1000.0, ab)
        rj60[r], _ = aturan(st.loc[rec, [f"st60_{s}" for s in SADAPAN]].values.astype(float), ab)
    assert rj.sum() == 2111, rj.sum()  # sama dengan K2 (Hasil_OMI_6.md)
    print(f"Aturan titik J positif: {rj.sum()} dari {n}; varian J + 60 ms positif: {rj60.sum()}.\n")
    s, o = ut.STEMI.values.astype(int), ut.OMI.values.astype(int)
    print("| Aturan | Sasaran | n positif sasaran | Se | Sp |")
    print("| --- | --- | --- | --- | --- |")
    for nama, a in [("titik J", rj), ("J + 60 ms", rj60)]:
        for sas, y in [("STEMI", s), ("OMI", o)]:
            print(f"| {nama} | {sas} | {y.sum()} | {a[y == 1].mean():.3f} | {1 - a[y == 0].mean():.3f} |")
    q = pd.qcut(ut.Time_Interval, 4, labels=["Q1", "Q2", "Q3", "Q4"])
    print("\nSensitivitas untuk STEMI per kuartil Time_Interval (batas P4):\n")
    print("| Kuartil | n STEMI | Se titik J | Se J + 60 ms |")
    print("| --- | --- | --- | --- |")
    for k in ["Q1", "Q2", "Q3", "Q4"]:
        m = (q == k).values & (s == 1)
        print(f"| {k} | {m.sum()} | {rj[m].mean():.3f} | {rj60[m].mean():.3f} |")
    m = (s == 1) & np.isfinite(mj)
    v = mj[m]
    print(f"\nElevasi pasangan terbesar di atas ambang (mV), STEMI dengan deteksi ok (n = {m.sum()}): median "
          f"{np.median(v):.3f}, IQR {np.quantile(v, .25):.3f} sampai {np.quantile(v, .75):.3f}; "
          f"bagian ≥ 0: {np.mean(v >= 0):.3f}.\n")


def c2(ut, P, B):
    print("## C2. Tiga AUROC berpasangan (skor OMI kohort penuh)\n")
    o, a, g_all = ut.OMI.values.astype(int), ut.AMI.values.astype(int), ut.Patient_id.values
    kel = np.where(o == 1, 2, np.where(a == 1, 1, 0))  # 2 OMI, 1 AMI tanpa OMI, 0 tanpa AMI
    print(f"OMI {np.sum(kel == 2)}, AMI tanpa OMI {np.sum(kel == 1)}, tanpa AMI {np.sum(kel == 0)}.\n")
    rng = np.random.default_rng(20261120)
    perb = {"(a) OMI lawan tanpa AMI": (2, 0), "(b) AMI tanpa OMI lawan tanpa AMI": (1, 0),
            "(c) OMI lawan AMI tanpa OMI": (2, 1)}
    print("| Pasangan | " + " | ".join(P) + " |")
    print("| --- | " + " | ".join("---" for _ in P) + " |")
    for nama, (pos, neg) in perb.items():
        s = np.flatnonzero((kel == pos) | (kel == neg))
        y, g = (kel[s] == pos).astype(int), g_all[s]
        titik, ci, _ = ringkas(y, g, {m: [p[s] for p in ps] for m, ps in P.items()},
                               lambda yy, pp: {"AUROC": roc_auc_score(yy, pp)}, B, rng)
        print(f"| {nama} | " + " | ".join(sel(titik[m]["AUROC"], ci[m][0]["AUROC"], ci[m][1]["AUROC"])
                                          for m in P) + " |")
    print()


def c3(ut, P, B):
    print("## C3. Latih ulang di dalam AMI=1 dan STEMI=1 (prosedur fase A)\n")
    st = pd.read_csv(AKAR / "ciri_st_train.csv").set_index("ecg_med_record")
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    E_all = np.load(AKAR / "emb_ecgfounder_train.npy")
    assert E_all.shape == (len(tr), 1024)
    E = E_all[np.flatnonzero((tr.Paced != 1).values)]
    assert len(E) == len(ut)
    rng = np.random.default_rng(20261121)
    for nama, mask in [("AMI=1", ut.AMI == 1), ("STEMI=1", ut.STEMI == 1)]:
        s = np.flatnonzero(mask.values)
        d = ut.iloc[s]
        y, g = d.OMI.values.astype(int), d.Patient_id.values
        X = {"M0 latih ulang": (d[["age", "gender"]].values.astype(float), False),
             "M1 latih ulang": (st.loc[d.ecg_med_record, CIRI_ST].values.astype(float), True),
             "M3a latih ulang": (E[s], True)}
        pr, Cs = {}, {}
        for m, (x, pilih) in X.items():
            h = [oof(x, y, g, b, pilih) for b in BENIH]
            pr[m] = [hh[0][:, 1] for hh in h]
            Cs[m] = sorted({c for hh in h for c in hh[1]})
        pr["M3a kohort penuh"] = [p[s] for p in P["M3a"]]
        titik, ci, ulang = ringkas(y, g, pr, metrik, B, rng)
        print(f"### {nama}: n EKG {len(y)}, OMI {y.sum()} ({100 * y.mean():.1f} %), pasien {len(np.unique(g))}. "
              f"C terpilih: " + "; ".join(f"{m} {Cs[m]}" for m in Cs if m != "M0 latih ulang") + "\n")
        cetak(titik, ci, ["AUROC", "AUPRC", "Brier", "Se@Sp90", "slope", "intercept"])
        for a_, b_ in [("M3a latih ulang", "M3a kohort penuh"), ("M3a latih ulang", "M1 latih ulang")]:
            dd = ulang[a_]["AUROC"].values - ulang[b_]["AUROC"].values
            print(f"\nSelisih AUROC {a_} − {b_}: "
                  f"{sel(titik[a_]['AUROC'] - titik[b_]['AUROC'], np.quantile(dd, .025), np.quantile(dd, .975))}.")
        print()


def c4(ut, B):
    print("## C4. M3a dilatih ulang di NSTEMI (pra-daftar asli): EKG di bawah ambang\n")
    o3 = np.load(AKAR / "oof_m3a.npz")
    s = np.flatnonzero((ut.NSTEMI == 1).values)
    y, g = ut.OMI.values[s].astype(int), ut.Patient_id.values[s]
    ps = [o3[f"nstemi_{b}"] for b in BENIH]
    assert all(len(p) == len(s) for p in ps)
    prev = y.mean()
    print(f"n EKG {len(y)}, OMI {y.sum()} ({100 * prev:.1f} %).\n")
    rng = np.random.default_rng(20261122)

    def f(yy, pp):
        pv = yy.mean()
        out = {}
        for t in AMBANG_C4:
            k = int(round(t * 100))
            out[f"NB{k}"] = nb(yy, pp, t)
            out[f"D{k}"] = out[f"NB{k}"] - (pv - (1 - pv) * t / (1 - t))
        return out

    titik, ci, _ = ringkas(y, g, {"M3a": ps}, f, B, rng)
    print("| Ambang | Obati semua | M3a NB | M3a − obati semua | EKG di bawah ambang (OMI), rata-rata benih |")
    print("| --- | --- | --- | --- | --- |")
    for t in AMBANG_C4:
        k = int(round(t * 100))
        bawah = np.mean([np.sum(p < t) for p in ps])
        omi_b = np.mean([np.sum((p < t) & (y == 1)) for p in ps])
        print(f"| {k} % | {prev - (1 - prev) * t / (1 - t):.3f} | "
              f"{sel(titik['M3a'][f'NB{k}'], ci['M3a'][0][f'NB{k}'], ci['M3a'][1][f'NB{k}'])} | "
              f"{sel(titik['M3a'][f'D{k}'], ci['M3a'][0][f'D{k}'], ci['M3a'][1][f'D{k}'])} | "
              f"{bawah:.0f} ({omi_b:.0f}) |")
    t_all = np.arange(1, 61) / 100
    nbm = np.array([np.mean([nb(y, p, t) for p in ps]) for t in t_all])
    nba = prev - (1 - prev) * t_all / (1 - t_all)
    di_atas = t_all[(nbm > nba) & (nbm > 0)]
    print(f"\nAmbang 1–60 % (langkah 1 %) dengan NB rata-rata benih > obati semua dan > 0: "
          f"{', '.join(f'{int(round(100 * t))}' for t in di_atas) or 'tidak ada'} %.\n")


def c5(ut):
    print("## C5. Karakteristik per kelompok (analisis utama)\n")
    o, a = ut.OMI.values.astype(int), ut.AMI.values.astype(int)
    kel = {"OMI": o == 1, "AMI tanpa OMI": (a == 1) & (o == 0), "tanpa AMI": a == 0}

    def mi(v):
        return f"{np.median(v):.0f} ({np.quantile(v, .25):.0f}–{np.quantile(v, .75):.0f})"

    baris = [("n EKG", lambda d: f"{len(d)}"), ("n pasien", lambda d: f"{d.Patient_id.nunique()}"),
             ("usia, median (IQR)", lambda d: mi(d.age)),
             ("laki-laki (gender = 1), %", lambda d: f"{100 * (d.gender == 1).mean():.1f}"),
             ("Time_Interval menit, median (IQR)", lambda d: mi(d.Time_Interval))]
    for c in ["STEMI", "NSTEMI", "UA", "Prior_PCI", "VF_VT", "PCI", "CTO"]:
        baris.append((f"{c}, n (%)", lambda d, c=c: f"{int(d[c].sum())} ({100 * d[c].mean():.1f})"))
    print("| Ciri | " + " | ".join(kel) + " |")
    print("| --- | " + " | ".join("---" for _ in kel) + " |")
    for nama, fn in baris:
        print(f"| {nama} | " + " | ".join(fn(ut[m]) for m in kel.values()) + " |")
    x = ut[(ut.AMI == 1) & (ut.STEMI == 0) & (ut.NSTEMI == 0)]
    print(f"\nAMI = 1 tanpa STEMI maupun NSTEMI: {len(x)} EKG (OMI {int(x.OMI.sum())}). "
          f"STEMI = 1 dan NSTEMI = 1 bersamaan: {int(((ut.STEMI == 1) & (ut.NSTEMI == 1)).sum())}. "
          f"STEMI atau NSTEMI dengan AMI = 0: {int((((ut.STEMI == 1) | (ut.NSTEMI == 1)) & (ut.AMI == 0)).sum())}.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--butir", default="C1,C2,C3,C4,C5")
    arg = ap.parse_args()
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase C OMI — keluaran omi_fase_c.py (B = {arg.B})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    if "C5" in butir:
        c5(ut)
    if "C1" in butir:
        c1(ut)
    if "C2" in butir:
        c2(ut, P, arg.B)
    if "C4" in butir:
        c4(ut, arg.B)
    if "C3" in butir:
        c3(ut, P, arg.B)


if __name__ == "__main__":
    main()
