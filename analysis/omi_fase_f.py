"""Fase F OMI (Prareg_OMI_F.md, terkunci 13 Nov 2026, e9c7062): nol permutasi label oklusi di dalam infark,
selisih label per kuartil jarak ke angiografi, OMI lawan CTO, ragam pelatihan CNN.

Masukan di luar repo ($OMI_DATA): seperti omi_fase_e.py (oof_m3a.npz, oof_m3a_ami.npz, oof_m2_utama.npz,
oof_m2_ami.npz, emb_ecgfounder_train.npy, raw250_train.npy).

Pakai:
  python omi_fase_f.py --permutasi [--n 100]          # F1: 100 probe berlabel teracak -> perm_f1.csv (bisa dilanjutkan)
  python-gpu omi_fase_f.py --cnn-benih           # F4b: CNN 5 benih x 2 label -> oof_m2_benih.npz (bisa dilanjutkan)
  python omi_fase_f.py --butir F1,F2,F3,F4 [--B 2000] # analisis
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, indeks_bootstrap, lipatan, pipa  # noqa: E402
from omi_konstruk import beda_auc, muat, sel  # noqa: E402
from omi_fase_d import auc_ci, emb_utama, kelompok  # noqa: E402

C_TETAP = 0.001
LIP = 20261107
PERM = AKAR / "perm_f1.csv"
OOF_BENIH = AKAR / "oof_m2_benih.npz"
BENIH_INIT = [20261140, 20261141, 20261142, 20261143, 20261144]


def probe_oof(E, y, g):
    p = np.zeros(len(y))
    for a, b in lipatan(y, g, LIP):
        p[b] = pipa(C_TETAP).fit(E[a], y[a]).predict_proba(E[b])[:, 1]
    return p


# ---------------------------------------------------------------- F1: latih
def permutasi(n):
    ut, _ = muat()
    E, g = emb_utama(ut), ut.Patient_id.values
    kel = kelompok(ut)
    ami = np.flatnonzero(kel >= 1)
    yo = ut.OMI.values.astype(int)
    c = ami  # (c): OMI lawan AMI tanpa OMI
    sudah = pd.read_csv(PERM) if PERM.exists() else pd.DataFrame(columns=["perm", "auc_c", "auc_semua"])
    baris = sudah.to_dict("records")
    t0 = time.time()
    if -1 not in set(sudah.perm):
        p = probe_oof(E, yo, g)
        baris.append({"perm": -1, "auc_c": roc_auc_score(yo[c], p[c]), "auc_semua": roc_auc_score(yo, p)})
        pd.DataFrame(baris).to_csv(PERM, index=False)
        print(f"label asli: (c) {baris[-1]['auc_c']:.4f}, semua {baris[-1]['auc_semua']:.4f} "
              f"({(time.time() - t0) / 60:.1f} menit)", flush=True)
    for k in range(1, n + 1):
        if k in set(sudah.perm):
            continue
        rng = np.random.default_rng(k)
        yp = np.zeros_like(yo)
        yp[rng.choice(ami, int(yo.sum()), replace=False)] = 1
        assert yp.sum() == yo.sum() and yp[kel == 0].sum() == 0
        p = probe_oof(E, yp, g)
        baris.append({"perm": k, "auc_c": roc_auc_score(yo[c], p[c]), "auc_semua": roc_auc_score(yo, p)})
        pd.DataFrame(baris).to_csv(PERM, index=False)
        print(f"permutasi {k}: (c) {baris[-1]['auc_c']:.4f} ({(time.time() - t0) / 60:.1f} menit)", flush=True)


# ---------------------------------------------------------------- F4b: latih (GPU environment)
def cnn_benih():
    from omi_m2 import EPOCH, latih_prediksi, muat_sinyal
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    X = muat_sinyal(tr)
    iu = np.flatnonzero((tr.Paced != 1).values)
    ut = tr.iloc[iu].reset_index(drop=True)
    Xu = np.asarray(X[iu])
    g = ut.Patient_id.values
    simpan = dict(np.load(OOF_BENIH, allow_pickle=True)) if OOF_BENIH.exists() else {}
    simpan["ecg_row_record"] = ut.ecg_row_record.values
    t0 = time.time()
    for lab in ["OMI", "AMI"]:
        y = ut[lab].values.astype(int)
        lip = lipatan(y, g, LIP)
        for b in BENIH_INIT:
            kunci = f"{lab}_{b}"
            if kunci in simpan:
                continue
            p = np.zeros(len(y))
            for a, u in lip:
                p[u] = latih_prediksi(Xu, y, a, u, b, EPOCH)[:, 1]
            simpan[kunci] = p
            np.savez(OOF_BENIH, **simpan)
            print(f"{kunci}: AUROC {lab} {roc_auc_score(y, p):.3f}, OMI {roc_auc_score(ut.OMI, p):.3f} "
                  f"({(time.time() - t0) / 60:.1f} menit)", flush=True)


# ---------------------------------------------------------------- analisis
def f1():
    print("## F1. Nol permutasi label oklusi di dalam infark (probe, C = 0,001, lipatan 20261107)\n")
    d = pd.read_csv(PERM)
    asli = d[d.perm == -1].iloc[0]
    nol = d[d.perm >= 1]
    q95 = np.quantile(nol.auc_c, .95)
    print(f"Permutasi selesai: {len(nol)}. AUROC (c) label asli {asli.auc_c:.4f}; OMI lawan semua {asli.auc_semua:.4f}.")
    print(f"Sebaran nol AUROC (c): rerata {nol.auc_c.mean():.4f}, SB {nol.auc_c.std():.4f}, "
          f"persentil 2,5/50/95/97,5 {np.quantile(nol.auc_c, .025):.4f} / {nol.auc_c.median():.4f} / {q95:.4f} / "
          f"{np.quantile(nol.auc_c, .975):.4f}, maksimum {nol.auc_c.max():.4f}.")
    print(f"Label asli − rerata nol: {asli.auc_c - nol.auc_c.mean():.4f}; permutasi ≥ label asli: "
          f"{int((nol.auc_c >= asli.auc_c).sum())} dari {len(nol)} (p = {((nol.auc_c >= asli.auc_c).sum() + 1) / (len(nol) + 1):.3f}).")
    print(f"Sebaran nol AUROC OMI lawan semua: rerata {nol.auc_semua.mean():.4f}, rentang "
          f"{nol.auc_semua.min():.4f}–{nol.auc_semua.max():.4f}.")
    print(f"Aturan: label asli > persentil ke-95 nol: **{'ya' if asli.auc_c > q95 else 'tidak'}**.\n")


def muat_ami(ut):
    oa = np.load(AKAR / "oof_m3a_ami.npz")
    o2 = np.load(AKAR / "oof_m2_ami.npz", allow_pickle=True)
    assert (o2["ecg_row_record"] == ut.ecg_row_record.values).all()
    return [oa[f"ami_{b}"] for b in BENIH], [o2[f"M2ami_{b}"] for b in BENIH]


def f2(ut, P, B):
    print("## F2. Selisih label per kuartil jarak EKG ke angiografi\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    pa, ca = muat_ami(ut)
    q = pd.qcut(ut.Time_Interval, 4, labels=["Q1", "Q2", "Q3", "Q4"]).astype(str).values
    rng = np.random.default_rng(20261131)
    print("| Kuartil | Sasaran | n pos / n | probe-OMI − probe-AMI | CNN-OMI − CNN-AMI |")
    print("| --- | --- | --- | --- | --- |")
    for k in ["Q1", "Q2", "Q3", "Q4"]:
        for nama, m in [("(c) OMI lawan AMI tanpa OMI", kel >= 1), ("OMI lawan semua", np.ones(len(ut), bool))]:
            s = np.flatnonzero((q == k) & m)
            y = ut.OMI.values[s].astype(int)
            tp = beda_auc(y, g[s], [p[s] for p in P["M3a"]], [p[s] for p in pa], rng, B)
            tc = beda_auc(y, g[s], [p[s] for p in P["M2"]], [p[s] for p in ca], rng, B)
            print(f"| {k} | {nama} | {y.sum()} / {len(y)} | {sel(*tp[:3])} | {sel(*tc[:3])} |", flush=True)
    print()


def f3(ut, P, B):
    print("## F3. Oklusi kronis lawan oklusi akut\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    pa, _ = muat_ami(ut)
    cto = (ut.CTO.values == 1) & (kel == 0)
    ref = (kel == 0) & ~cto
    omi = kel == 2
    pr = {"probe-OMI": P["M3a"], "probe-AMI": pa}
    rng = np.random.default_rng(20261132)
    s = np.flatnonzero(omi | cto)
    r = auc_ci(omi[s].astype(int), g[s], {k: [p[s] for p in v] for k, v in pr.items()}, rng, B)
    print(f"(i) OMI lawan CTO langsung ({int(omi.sum())} / {int(cto.sum())}): probe-OMI {sel(*r['probe-OMI'])}; "
          f"probe-AMI {sel(*r['probe-AMI'])}.\n")
    s = np.flatnonzero(omi | cto | ref)
    gs = g[s]
    print(f"(ii) Rujukan sama: tanpa AMI non-CTO ({int(ref.sum())}).\n")
    print("| Model | OMI lawan rujukan | CTO lawan rujukan | selisih |")
    print("| --- | --- | --- | --- |")
    for nama, ps in pr.items():
        def dua(ix):
            o, c, rf = omi[s][ix], cto[s][ix], ref[s][ix]
            a1 = np.mean([roc_auc_score(np.r_[np.ones(o.sum()), np.zeros(rf.sum())],
                                        np.r_[p[s][ix][o], p[s][ix][rf]]) for p in ps])
            a2 = np.mean([roc_auc_score(np.r_[np.ones(c.sum()), np.zeros(rf.sum())],
                                        np.r_[p[s][ix][c], p[s][ix][rf]]) for p in ps])
            return a1, a2
        t1, t2 = dua(np.arange(len(s)))
        v = np.array([dua(ix) for ix in indeks_bootstrap(gs, rng, B)])
        lo, hi = np.quantile(v, .025, axis=0), np.quantile(v, .975, axis=0)
        dd = v[:, 0] - v[:, 1]
        print(f"| {nama} | {sel(t1, lo[0], hi[0])} | {sel(t2, lo[1], hi[1])} | "
              f"{sel(t1 - t2, np.quantile(dd, .025), np.quantile(dd, .975))} |", flush=True)
    print("\n(iii) CTO lawan rujukan, menurut Prior_PCI:\n")
    print("| Prior_PCI | n CTO / n rujukan | probe-OMI | probe-AMI |")
    print("| --- | --- | --- | --- |")
    pp = ut.Prior_PCI.values == 1
    for nama, m in [("ya", pp), ("tidak", ~pp)]:
        s = np.flatnonzero((cto & m) | ref)
        y = (cto & m)[s].astype(int)
        r = auc_ci(y, g[s], {k: [p[s] for p in v] for k, v in pr.items()}, rng, B)
        print(f"| {nama} | {y.sum()} / {len(y) - y.sum()} | {sel(*r['probe-OMI'])} | {sel(*r['probe-AMI'])} |",
              flush=True)
    print()


def f4(ut, P, B):
    print("## F4. Ragam pelatihan\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    pa, ca = muat_ami(ut)
    sas = {"OMI lawan semua": (np.ones(len(ut), bool), "OMI"), "(c) OMI lawan AMI tanpa OMI": (kel >= 1, "OMI"),
           "AMI lawan tanpa AMI": (np.ones(len(ut), bool), "AMI")}
    print("(a) Selisih AUROC label oklusi − label infark per penetapan lipatan (prediksi tersimpan):\n")
    print("| Sasaran | Model | " + " | ".join(str(b) for b in BENIH) + " |")
    print("| --- | --- | " + " | ".join("---" for _ in BENIH) + " |")
    for nama, (m, kol) in sas.items():
        s = np.flatnonzero(m)
        y = ut[kol].values[s].astype(int)
        for mn, po, pi in [("probe", P["M3a"], pa), ("CNN", P["M2"], ca)]:
            print(f"| {nama} | {mn} | " + " | ".join(
                f"{roc_auc_score(y, po[k][s]) - roc_auc_score(y, pi[k][s]):.3f}" for k in range(len(BENIH))) + " |")
    print("\n(b) CNN, lima benih inisialisasi, penetapan lipatan 20261107:\n")
    o = np.load(OOF_BENIH, allow_pickle=True)
    assert (o["ecg_row_record"] == ut.ecg_row_record.values).all()
    rng = np.random.default_rng(20261133)
    for nama, (m, kol) in sas.items():
        s = np.flatnonzero(m)
        y = ut[kol].values[s].astype(int)
        ao = [roc_auc_score(y, o[f"OMI_{b}"][s]) for b in BENIH_INIT]
        ai = [roc_auc_score(y, o[f"AMI_{b}"][s]) for b in BENIH_INIT]
        d = np.array(ao) - np.array(ai)
        mo = np.mean([o[f"OMI_{b}"][s] for b in BENIH_INIT], 0)
        mi = np.mean([o[f"AMI_{b}"][s] for b in BENIH_INIT], 0)
        t = beda_auc(y, g[s], [mo], [mi], rng, B)
        print(f"- {nama}: AUROC label OMI per benih " + ", ".join(f"{a:.3f}" for a in ao)
              + "; label AMI " + ", ".join(f"{a:.3f}" for a in ai)
              + f"; selisih per pasangan " + ", ".join(f"{x:+.3f}" for x in d)
              + f" (rerata {d.mean():+.3f}, rentang {d.min():+.3f} sampai {d.max():+.3f}, > 0: {int((d > 0).sum())} "
              f"dari 5); prediksi rerata lima benih: {sel(*t[:3])}.", flush=True)
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--butir", default="")
    ap.add_argument("--permutasi", action="store_true")
    ap.add_argument("--cnn-benih", action="store_true")
    arg = ap.parse_args()
    if arg.permutasi:
        return permutasi(arg.n)
    if arg.cnn_benih:
        return cnn_benih()
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase F OMI — keluaran omi_fase_f.py (B = {arg.B}, butir {arg.butir})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    t0 = time.time()
    for k, f in [("F1", f1), ("F2", lambda: f2(ut, P, arg.B)), ("F3", lambda: f3(ut, P, arg.B)),
                 ("F4", lambda: f4(ut, P, arg.B))]:
        if k in butir:
            f()
    print(f"Waktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
