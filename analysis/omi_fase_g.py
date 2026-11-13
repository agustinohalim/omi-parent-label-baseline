"""Fase G OMI (Prareg_OMI_G.md, terkunci 13 Nov 2026): komposisi STEMI dan uji "differ only".

Masukan di luar repo ($OMI_DATA): seperti omi_fase_f.py.

Pakai:
  python omi_fase_g.py --permutasi [--n 100]   # G1(ii): nol permutasi berlapis tipe infark -> perm_g1.csv (bisa dilanjutkan)
  python omi_fase_g.py --butir G1,G2,G3 [--B 2000]   # G3: penyimpangan P1
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR  # noqa: E402
from omi_konstruk import beda_auc, muat, sel  # noqa: E402
from omi_fase_d import emb_utama, kelompok  # noqa: E402
from omi_fase_f import muat_ami, probe_oof  # noqa: E402

PERM_G = AKAR / "perm_g1.csv"
PERM_F = AKAR / "perm_f1.csv"


def lapis_tipe(ut):
    st, ns = (ut.STEMI == 1).values, (ut.NSTEMI == 1).values
    return np.where(st, "STEMI", np.where(ns, "NSTEMI", "lain"))


# ---------------------------------------------------------------- G1(ii): latih
def permutasi(n):
    ut, _ = muat()
    E, g = emb_utama(ut), ut.Patient_id.values
    kel = kelompok(ut)
    yo = ut.OMI.values.astype(int)
    lp = lapis_tipe(ut)
    ami = kel >= 1
    st, ns = ami & (lp == "STEMI"), ami & (lp == "NSTEMI")
    sudah = pd.read_csv(PERM_G) if PERM_G.exists() else pd.DataFrame(columns=["perm"])
    baris = sudah.to_dict("records")
    t0 = time.time()
    for k in range(1001, 1001 + n):
        if k in set(sudah.perm):
            continue
        rng = np.random.default_rng(k)
        yp = np.zeros_like(yo)
        for nama in ["STEMI", "NSTEMI", "lain"]:
            ix = np.flatnonzero(ami & (lp == nama))
            m = int(yo[ix].sum())
            if m:
                yp[rng.choice(ix, m, replace=False)] = 1
        assert yp.sum() == yo.sum() and yp[kel == 0].sum() == 0
        assert all(yp[ami & (lp == t)].sum() == yo[ami & (lp == t)].sum() for t in ["STEMI", "NSTEMI", "lain"])
        p = probe_oof(E, yp, g)
        baris.append({"perm": k, "auc_c": roc_auc_score(yo[ami], p[ami]), "auc_stemi": roc_auc_score(yo[st], p[st]),
                      "auc_nstemi": roc_auc_score(yo[ns], p[ns])})
        pd.DataFrame(baris).to_csv(PERM_G, index=False)
        print(f"permutasi {k}: (c) {baris[-1]['auc_c']:.4f} ({(time.time() - t0) / 60:.1f} menit)", flush=True)


# ---------------------------------------------------------------- analisis
def g1(ut, P, B):
    print("## G1. Komposisi STEMI\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    lp = lapis_tipe(ut)
    pa, ca = muat_ami(ut)
    rng = np.random.default_rng(20261150)
    print("(i) Selisih label oklusi − label infark di dalam tipe infark (prediksi tersimpan, tiga penetapan):\n")
    print("| Lapis | n OMI / n tanpa OMI | probe-OMI | probe-AMI | selisih probe | CNN-OMI | CNN-AMI | selisih CNN |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for t in ["STEMI", "NSTEMI"]:
        s = np.flatnonzero((kel >= 1) & (lp == t))
        y = ut.OMI.values[s].astype(int)
        r = []
        for po, pi in [(P["M3a"], pa), (P["M2"], ca)]:
            ao = np.mean([roc_auc_score(y, p[s]) for p in po])
            ai = np.mean([roc_auc_score(y, p[s]) for p in pi])
            d = beda_auc(y, g[s], [p[s] for p in po], [p[s] for p in pi], rng, B)
            r.append(f"{ao:.3f} | {ai:.3f} | {sel(*d[:3])}")
        print(f"| {t} | {y.sum()} / {len(y) - y.sum()} | {r[0]} | {r[1]} |", flush=True)
    print("\n(ii) Nol permutasi berlapis tipe infark (probe, C = 0,001, lipatan 20261107):\n")
    d = pd.read_csv(PERM_G)
    f = pd.read_csv(PERM_F)
    asli = f[f.perm == -1].iloc[0].auc_c
    q95 = np.quantile(d.auc_c, .95)
    print(f"Permutasi selesai: {len(d)}. AUROC (c) label asli {asli:.4f} (F1).")
    print(f"Nol berlapis AUROC (c): rerata {d.auc_c.mean():.4f}, SB {d.auc_c.std():.4f}, persentil 2,5/50/95/97,5 "
          f"{np.quantile(d.auc_c, .025):.4f} / {d.auc_c.median():.4f} / {q95:.4f} / {np.quantile(d.auc_c, .975):.4f}, "
          f"maksimum {d.auc_c.max():.4f}.")
    print(f"Label asli − rerata nol berlapis: {asli - d.auc_c.mean():.4f}; permutasi ≥ label asli: "
          f"{int((d.auc_c >= asli).sum())} dari {len(d)} (p = {((d.auc_c >= asli).sum() + 1) / (len(d) + 1):.3f}).")
    print(f"Nol berlapis di dalam STEMI: rerata {d.auc_stemi.mean():.4f} (rentang {d.auc_stemi.min():.4f}–"
          f"{d.auc_stemi.max():.4f}); di dalam NSTEMI: rerata {d.auc_nstemi.mean():.4f} (rentang "
          f"{d.auc_nstemi.min():.4f}–{d.auc_nstemi.max():.4f}).")
    print(f"Nol tak berlapis (F1) sebagai pembanding: rerata {f[f.perm >= 1].auc_c.mean():.4f}.")
    print(f"Aturan: label asli > persentil ke-95 nol berlapis: **{'ya' if asli > q95 else 'tidak'}**.\n")


def g2(ut, P, B):
    print("## G2. Uji \"differ only\"\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    pa, ca = muat_ami(ut)
    rng = np.random.default_rng(20261151)
    sas = {"OMI lawan semua": (np.ones(len(ut), bool), "OMI"), "OMI lawan tanpa infark": (kel != 1, "OMI"),
           "(c) OMI lawan AMI tanpa OMI": (kel >= 1, "OMI"), "AMI lawan tanpa AMI": (np.ones(len(ut), bool), "AMI")}
    print("| Sasaran | n pos / n | selisih probe | selisih CNN |")
    print("| --- | --- | --- | --- |")
    hasil = {}
    for nama, (m, kol) in sas.items():
        s = np.flatnonzero(m)
        y = ut[kol].values[s].astype(int)
        dp = beda_auc(y, g[s], [p[s] for p in P["M3a"]], [p[s] for p in pa], rng, B)
        dc = beda_auc(y, g[s], [p[s] for p in P["M2"]], [p[s] for p in ca], rng, B)
        hasil[nama] = (dp, dc)
        print(f"| {nama} | {y.sum()} / {len(y)} | {sel(*dp[:3])} | {sel(*dc[:3])} |", flush=True)

    def ok(d):
        return -0.03 < d[1] and d[2] < 0.03 and d[1] <= 0 <= d[2]
    for mn, k in [("probe", 0), ("CNN", 1)]:
        a, b = hasil["OMI lawan tanpa infark"][k], hasil["AMI lawan tanpa AMI"][k]
        print(f"\nAturan \"only\" ({mn}): OMI lawan tanpa infark di dalam ±0,03 dan memuat 0: {'ya' if ok(a) else 'tidak'}; "
              f"infark lawan tanpa infark: {'ya' if ok(b) else 'tidak'} → **{'only boleh' if ok(a) and ok(b) else 'only tidak dipakai'}**.")
    print()


def g3(ut, P, B):
    print("## G3. Model berlabel infark per baris Tabel 4; probe lawan CNN (penyimpangan P1)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    pa, ca = muat_ami(ut)
    rng = np.random.default_rng(20261152)
    lp = lapis_tipe(ut)
    pci = (ut.PCI == 1).values
    tanpa = kel == 0
    inf_no = kel == 1
    baris = {"OMI lawan tanpa infark": (kel == 2, tanpa),
             "Infark tanpa oklusi lawan tanpa infark": (inf_no, tanpa),
             "  STEMI": (inf_no & (lp == "STEMI"), tanpa),
             "  NSTEMI": (inf_no & (lp == "NSTEMI"), tanpa),
             "  dengan PCI": (inf_no & pci, tanpa),
             "  tanpa PCI": (inf_no & ~pci, tanpa),
             "  NSTEMI tanpa PCI": (inf_no & (lp == "NSTEMI") & ~pci, tanpa)}
    print("(i) Skor OMI tiap model untuk pasangan kelompok (pos lawan neg):\n")
    print("| Pasangan | n pos / n neg | probe-OMI | probe-AMI | selisih probe | CNN-OMI | CNN-AMI | selisih CNN | ±0,03 probe |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for nama, (pos, neg) in baris.items():
        s = np.flatnonzero(pos | neg)
        y = pos[s].astype(int)
        r = []
        for po, pi in [(P["M3a"], pa), (P["M2"], ca)]:
            ao = np.mean([roc_auc_score(y, p[s]) for p in po])
            ai = np.mean([roc_auc_score(y, p[s]) for p in pi])
            d = beda_auc(y, g[s], [p[s] for p in po], [p[s] for p in pi], rng, B)
            r.append((ao, ai, d))
        ok = -0.03 < r[0][2][1] and r[0][2][2] < 0.03
        print(f"| {nama} | {y.sum()} / {len(y) - y.sum()} | {r[0][0]:.3f} | {r[0][1]:.3f} | {sel(*r[0][2][:3])} | "
              f"{r[1][0]:.3f} | {r[1][1]:.3f} | {sel(*r[1][2][:3])} | {'ya' if ok else 'tidak'} |", flush=True)
    print("\n(ii) Selisih probe-OMI − CNN-OMI:\n")
    print("| Sasaran | n pos / n | probe-OMI | CNN-OMI | selisih |")
    print("| --- | --- | --- | --- | --- |")
    hasil = {}
    for nama, m in [("OMI lawan semua", np.ones(len(ut), bool)), ("(c) OMI lawan AMI tanpa OMI", kel >= 1),
                    ("di dalam STEMI", (kel >= 1) & (lp == "STEMI")), ("di dalam NSTEMI", (kel >= 1) & (lp == "NSTEMI"))]:
        s = np.flatnonzero(m)
        y = ut.OMI.values[s].astype(int)
        ap = np.mean([roc_auc_score(y, p[s]) for p in P["M3a"]])
        ac = np.mean([roc_auc_score(y, p[s]) for p in P["M2"]])
        d = beda_auc(y, g[s], [p[s] for p in P["M3a"]], [p[s] for p in P["M2"]], rng, B)
        hasil[nama] = d
        print(f"| {nama} | {y.sum()} / {len(y)} | {ap:.3f} | {ac:.3f} | {sel(*d[:3])} |", flush=True)
    d = hasil["(c) OMI lawan AMI tanpa OMI"]
    print(f"\nAturan: CI selisih (c) memuat 0: {'ya → anak kalimat boleh' if d[1] <= 0 <= d[2] else 'tidak → anak kalimat dihapus'}.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--butir", default="")
    ap.add_argument("--permutasi", action="store_true")
    arg = ap.parse_args()
    if arg.permutasi:
        return permutasi(arg.n)
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase G OMI — keluaran omi_fase_g.py (B = {arg.B}, butir {arg.butir})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    t0 = time.time()
    for k, fn in [("G1", lambda: g1(ut, P, arg.B)), ("G2", lambda: g2(ut, P, arg.B)), ("G3", lambda: g3(ut, P, arg.B))]:
        if k in butir:
            fn()
    print(f"Waktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
