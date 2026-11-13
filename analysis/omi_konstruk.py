"""Fase B OMI (Prareg_OMI_B.md, terkunci 12 Nov 2026): uji konstruk K1–K5 atas prediksi out-of-fold yang tersimpan.

Tidak ada model yang dilatih. Masukan di luar repo ($OMI_DATA/):
    csv/CSV/train.csv, oof_m01.csv (M0, M1), oof_m2_utama.npz (M2), oof_m3a.npz (M3a), med/med_data/<id>.med (K2)
Analisis utama = train.csv tanpa Paced (17.622 EKG), urutan baris sama untuk semua berkas (diperiksa assert).

K1  oklusi di luar infark: AMI=1, STEMI=1, NSTEMI=1, STEMI=0; skor OMI untuk sasaran AMI; rujukan label AMI/STEMI.
K2  aturan kriteria STEMI (Fourth UDMI) dari amplitudo ST di titik J (deteksi P1, omi_ciri_st.deteksi).
K3  per kuartil Time_Interval (batas = P4) AUROC di dalam AMI=1; kuartil terpendek: ukuran lengkap.
K4  M2 dengan koreksi bobot kelas: logit - log((1-p)/p), p = prevalensi lipatan latih (lipatan dibangun ulang).
K5  net benefit 1–40 % di NSTEMI=1 dan AMI=1, dengan jumlah EKG dan OMI di bawah tiap ambang.

Bootstrap 2.000 bergugus pasien, satu benih per butir (20261115–19), seperti pra-daftar.
Pakai: python-gpu analysis/omi_konstruk.py [--B 2000] [--butir K1,K2,K3,K4,K5]
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, indeks_bootstrap, lipatan, logistik_1d, metrik, ringkas  # noqa: E402
from omi_ciri_st import SADAPAN, baca_med, deteksi  # noqa: E402

AMBANG_K5 = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]


def muat():
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    ut = tr[tr.Paced != 1].reset_index(drop=True)
    o1 = pd.read_csv(AKAR / "oof_m01.csv")
    assert (o1.ecg_med_record.values == ut.ecg_med_record.values).all()
    o2 = np.load(AKAR / "oof_m2_utama.npz", allow_pickle=True)
    assert (o2["ecg_row_record"] == ut.ecg_row_record.values).all()
    o3 = np.load(AKAR / "oof_m3a.npz")
    P = {"M0": [o1[f"M0_{s}"].values for s in BENIH],
         "M1": [o1[f"M1_{s}"].values for s in BENIH],
         "M2": [o2[f"M2_{s}"] for s in BENIH],
         "M3a": [o3[f"utama_{s}"] for s in BENIH]}
    for m, ps in P.items():
        assert all(len(p) == len(ut) for p in ps), m
    return ut, P


def m_ringan(y, p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    lg = np.log(p / (1 - p))
    _, slope = logistik_1d(lg, y)
    intercept, _ = logistik_1d(lg, y, offset_saja=True)
    thr = np.quantile(p[y == 0], 0.9)
    return {"AUROC": roc_auc_score(y, p), "AUPRC": average_precision_score(y, p),
            "Se@Sp90": np.mean(p[y == 1] > thr), "slope": slope, "intercept": intercept}


def sel(t, lo, hi):
    return f"{t:.3f} [{lo:.3f}, {hi:.3f}]"


def cetak(titik, ci, kolom):
    print("| Model | " + " | ".join(kolom) + " |")
    print("| --- | " + " | ".join("---" for _ in kolom) + " |")
    for m in titik:
        print(f"| {m} | " + " | ".join(sel(titik[m][k], ci[m][0][k], ci[m][1][k]) for k in kolom) + " |")


def beda_auc(y, g, pa, pb, rng, B):
    t = np.mean([roc_auc_score(y, p) for p in pa]) - np.mean([roc_auc_score(y, p) for p in pb])
    v = []
    for idx in indeks_bootstrap(g, rng, B):
        if len(np.unique(y[idx])) < 2:
            continue
        v.append(np.mean([roc_auc_score(y[idx], p[idx]) for p in pa])
                 - np.mean([roc_auc_score(y[idx], p[idx]) for p in pb]))
    return t, np.quantile(v, .025), np.quantile(v, .975), len(v)


def k1(ut, P, B):
    print("## K1. Oklusi di luar infark (prediksi kohort penuh, tanpa latih ulang)\n")
    y_all, g_all = ut.OMI.values.astype(int), ut.Patient_id.values
    rng = np.random.default_rng(20261115)
    sub = {"K1a AMI=1": ut.AMI == 1, "K1b STEMI=1": ut.STEMI == 1, "K1c NSTEMI=1": ut.NSTEMI == 1,
           "K1d STEMI=0": ut.STEMI == 0}
    for nama, mask in sub.items():
        s = np.flatnonzero(mask.values)
        y, g = y_all[s], g_all[s]
        pr = {m: [p[s] for p in ps] for m, ps in P.items()}
        titik, ci, _ = ringkas(y, g, pr, m_ringan, B, rng)
        print(f"### {nama}: n EKG {len(s)}, OMI {y.sum()} ({100 * y.mean():.1f} %), pasien {len(np.unique(g))}\n")
        cetak(titik, ci, ["AUROC", "AUPRC", "Se@Sp90", "slope", "intercept"])
        t, lo, hi, n = beda_auc(y, g, pr["M3a"], pr["M2"], rng, B)
        print(f"\nSelisih AUROC M3a − M2: {sel(t, lo, hi)} (replikat {n}).\n")
    # skor OMI untuk sasaran AMI
    ya = ut.AMI.values.astype(int)
    print("### Skor OMI tiap model untuk sasaran AMI (semua EKG analisis utama)\n")
    print(f"n EKG {len(ya)}, AMI {ya.sum()}.\n")
    print("| Model | AUROC skor OMI untuk AMI | AUROC skor OMI untuk OMI |")
    print("| --- | --- | --- |")
    for m, ps in P.items():
        print(f"| {m} | {np.mean([roc_auc_score(ya, p) for p in ps]):.3f} | "
              f"{np.mean([roc_auc_score(y_all, p) for p in ps]):.3f} |")
    print("\n### Rujukan label klinis (tidak tersedia saat EKG dibaca)\n")
    print("| Skor | Himpunan | Se untuk OMI | Sp untuk OMI | AUROC |")
    print("| --- | --- | --- | --- | --- |")
    for lab, mask, nm in [("AMI", np.ones(len(ut), bool), "analisis utama"),
                          ("STEMI", np.ones(len(ut), bool), "analisis utama"),
                          ("STEMI", (ut.AMI == 1).values, "AMI=1")]:
        y, x = y_all[mask], ut[lab].values[mask].astype(int)
        print(f"| {lab} | {nm} | {x[y == 1].mean():.3f} | {1 - x[y == 0].mean():.3f} | {roc_auc_score(y, x):.3f} |")
    print()


def ambang_v23(laki, usia):
    if not laki:
        return 0.15
    return 0.20 if usia >= 40 else 0.25


def k2(ut, P, B):
    print("## K2. Aturan kriteria STEMI otomatis (Fourth UDMI, titik J, denyut median)\n")
    idx = {s: i for i, s in enumerate(SADAPAN)}
    pasangan = [("II", "III"), ("II", "aVF"), ("III", "aVF"), ("I", "aVL")] + \
               [(f"V{k}", f"V{k + 1}") for k in range(1, 6)]
    st = pd.read_csv(AKAR / "ciri_st_train.csv").set_index("ecg_med_record").status
    aturan, gagal = np.zeros(len(ut), int), 0
    for r, (rec, gen, usia) in enumerate(zip(ut.ecg_med_record, ut.gender, ut.age)):
        if st.loc[rec] != "ok":  # status P1 (omi_ciri_st.py) selain ok -> negatif
            gagal += 1
            continue
        x = baca_med(AKAR / "med/med_data" / rec)
        _, awal, j = deteksi(x)
        pr = x[:, awal - 15:awal - 5].mean(axis=1)
        stj = (x[:, j] - pr) / 1000.0
        laki = (gen == 1)
        u = float(usia) if pd.notna(usia) else 99.0
        ab = {s: (ambang_v23(laki, u) if s in ("V2", "V3") else 0.10) for s in SADAPAN}
        naik = {s: stj[idx[s]] >= ab[s] for s in SADAPAN}
        aturan[r] = int(any(naik[a] and naik[b] for a, b in pasangan))
    print(f"Deteksi gagal atau di luar batas P1 (dihitung negatif): {gagal} dari {len(ut)} EKG. "
          f"Aturan positif: {aturan.sum()} ({100 * aturan.mean():.1f} %).\n")
    y_all, g_all = ut.OMI.values.astype(int), ut.Patient_id.values
    rng = np.random.default_rng(20261116)
    print("| Himpunan | n EKG / OMI | Aturan Se | Aturan Sp | M2 Se pada Sp aturan | M3a Se pada Sp aturan |")
    print("| --- | --- | --- | --- | --- | --- |")
    for nama, mask in [("analisis utama", np.ones(len(ut), bool)), ("AMI=1", (ut.AMI == 1).values),
                       ("NSTEMI=1", (ut.NSTEMI == 1).values)]:
        s = np.flatnonzero(mask)
        y, g, a = y_all[s], g_all[s], aturan[s]

        def ukur(ii):
            yy, aa = y[ii], a[ii]
            se, sp = aa[yy == 1].mean(), 1 - aa[yy == 0].mean()
            out = [se, sp]
            for m in ("M2", "M3a"):
                v = []
                for p in P[m]:
                    pp = p[s][ii]
                    thr = np.quantile(pp[yy == 0], sp)
                    v.append(np.mean(pp[yy == 1] > thr))
                out.append(np.mean(v))
            return np.array(out)

        t = ukur(np.arange(len(s)))
        rep = np.array([ukur(ii) for ii in indeks_bootstrap(g, rng, B) if len(np.unique(y[ii])) == 2])
        lo, hi = np.quantile(rep, .025, axis=0), np.quantile(rep, .975, axis=0)
        print(f"| {nama} | {len(s)} / {y.sum()} | " + " | ".join(sel(t[k], lo[k], hi[k]) for k in range(4)) + " |")
    print()


def k3(ut, P, B):
    print("## K3. Kuartil Time_Interval (batas P4)\n")
    y_all, g_all = ut.OMI.values.astype(int), ut.Patient_id.values
    ti = pd.to_numeric(ut.Time_Interval, errors="coerce")
    ada = ti.notna().values
    q, batas = pd.qcut(ti[ada], 4, labels=False, retbins=True)
    kuart = np.full(len(ut), -1)
    kuart[ada] = q.values
    print("Batas kuartil (menit): " + ", ".join(f"{b:.0f}" for b in batas) + ".\n")
    rng = np.random.default_rng(20261117)
    print("### AUROC di dalam AMI=1 per kuartil\n")
    print("| Kuartil | n EKG AMI / OMI | M1 | M2 | M3a |")
    print("| --- | --- | --- | --- | --- |")
    for k in range(4):
        s = np.flatnonzero((kuart == k) & (ut.AMI.values == 1))
        y, g = y_all[s], g_all[s]
        pr = {m: [p[s] for p in P[m]] for m in ("M1", "M2", "M3a")}
        titik = {m: np.mean([roc_auc_score(y, p) for p in ps]) for m, ps in pr.items()}
        ulang = {m: [] for m in pr}
        for ii in indeks_bootstrap(g, rng, B):
            if len(np.unique(y[ii])) < 2:
                continue
            for m, ps in pr.items():
                ulang[m].append(np.mean([roc_auc_score(y[ii], p[ii]) for p in ps]))
        print(f"| Q{k + 1} | {len(s)} / {y.sum()} | " + " | ".join(
            sel(titik[m], np.quantile(ulang[m], .025), np.quantile(ulang[m], .975)) for m in pr) + " |")
    s = np.flatnonzero(kuart == 0)
    y, g = y_all[s], g_all[s]
    pr = {m: [p[s] for p in ps] for m, ps in P.items()}
    titik, ci, _ = ringkas(y, g, pr, metrik, B, rng)
    print(f"\n### Kuartil terpendek Q1, sasaran utama: n EKG {len(s)}, OMI {y.sum()} ({100 * y.mean():.1f} %)\n")
    cetak(titik, ci, ["AUROC", "AUPRC", "Brier", "Se@Sp90", "slope", "intercept"])
    print()


def m2_koreksi(ut, P):
    y, g = ut.OMI.values.astype(int), ut.Patient_id.values
    out = []
    for s, p in zip(BENIH, P["M2"]):
        geser = np.empty(len(y))
        for a, b in lipatan(y, g, s):
            pa = y[a].mean()
            geser[b] = np.log((1 - pa) / pa)
        pp = np.clip(p, 1e-6, 1 - 1e-6)
        out.append(1 / (1 + np.exp(-(np.log(pp / (1 - pp)) - geser))))
    return out


def nb(y, p, t):
    n = len(y)
    return (np.sum((p >= t) & (y == 1)) - np.sum((p >= t) & (y == 0)) * t / (1 - t)) / n


def k4(ut, P, P2k, B):
    print("## K4. M2 dengan koreksi bobot kelas\n")
    y, g = ut.OMI.values.astype(int), ut.Patient_id.values
    rng = np.random.default_rng(20261118)
    pr = {"M2 mentah": P["M2"], "M2 terkoreksi": P2k, "M3a": P["M3a"]}
    titik, ci, ulang = ringkas(y, g, pr, metrik, B, rng)
    cetak(titik, ci, ["AUROC", "Brier", "slope", "intercept", "NB1", "NB2", "NB5", "NB10"])
    print("\n| Ambang | Obati semua | NB M3a − M2 terkoreksi |")
    print("| --- | --- | --- |")
    for t in (1, 2, 5, 10):
        d = ulang["M3a"][f"NB{t}"].values - ulang["M2 terkoreksi"][f"NB{t}"].values
        dt = titik["M3a"][f"NB{t}"] - titik["M2 terkoreksi"][f"NB{t}"]
        print(f"| {t} % | {titik['M3a'][f'NBall{t}']:.4f} | {dt:.4f} [{np.quantile(d, .025):.4f}, "
              f"{np.quantile(d, .975):.4f}] |")
    print()


def k5(ut, P, P2k, B):
    print("## K5. Net benefit 1–40 % di NSTEMI=1 dan AMI=1 (prediksi kohort penuh)\n")
    y_all, g_all = ut.OMI.values.astype(int), ut.Patient_id.values
    rng = np.random.default_rng(20261119)
    pr_all = {"M2 terkoreksi": P2k, "M3a": P["M3a"]}
    for nama, mask in [("NSTEMI=1", ut.NSTEMI == 1), ("AMI=1", ut.AMI == 1)]:
        s = np.flatnonzero(mask.values)
        y, g = y_all[s], g_all[s]
        prev = y.mean()
        pr = {m: [p[s] for p in ps] for m, ps in pr_all.items()}

        def f(yy, ps_list):
            return [np.mean([nb(yy, p, t) for p in ps_list]) for t in AMBANG_K5]

        titik = {m: f(y, ps) for m, ps in pr.items()}
        ulang = {m: [] for m in pr}
        for ii in indeks_bootstrap(g, rng, B):
            if len(np.unique(y[ii])) < 2:
                continue
            for m, ps in pr.items():
                ulang[m].append(f(y[ii], [p[ii] for p in ps]))
        print(f"### {nama}: n EKG {len(s)}, OMI {y.sum()} ({100 * prev:.1f} %)\n")
        print("| Ambang | Obati semua | M2 terkoreksi NB | M3a NB | M3a: EKG di bawah ambang (OMI di antaranya) |")
        print("| --- | --- | --- | --- | --- |")
        for k, t in enumerate(AMBANG_K5):
            semua = prev - (1 - prev) * t / (1 - t)
            c = [sel(titik[m][k], *np.quantile(np.array(ulang[m])[:, k], [.025, .975])) for m in pr]
            bawah = np.mean([np.sum(p[s] < t) for p in P["M3a"]])
            omi_b = np.mean([np.sum((p[s] < t) & (y == 1)) for p in P["M3a"]])
            print(f"| {int(t * 100)} % | {semua:.3f} | " + " | ".join(c) + f" | {bawah:.0f} ({omi_b:.0f}) |")
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--butir", default="K1,K2,K3,K4,K5")
    a = ap.parse_args()
    butir = a.butir.split(",")
    ut, P = muat()
    print(f"# Fase B OMI — keluaran omi_konstruk.py (B = {a.B})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    P2k = m2_koreksi(ut, P) if {"K4", "K5"} & set(butir) else None
    for k, fn in [("K1", lambda: k1(ut, P, a.B)), ("K2", lambda: k2(ut, P, a.B)), ("K3", lambda: k3(ut, P, a.B)),
                  ("K4", lambda: k4(ut, P, P2k, a.B)), ("K5", lambda: k5(ut, P, P2k, a.B))]:
        if k in butir:
            fn()
            sys.stdout.flush()


if __name__ == "__main__":
    main()
