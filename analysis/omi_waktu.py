"""Eksploratif (Prareg_OMI.md, Penyimpangan P4 butir 2): AUROC M1, M2, M3a per kuartil Time_Interval.

Analisis utama (tanpa Paced). Prediksi out-of-fold yang sudah ada (oof_m01.csv, oof_m2_utama.npz, oof_m3a.npz), tanpa
latih ulang. Time_Interval = menit dari EKG ke angiografi (makalah data). Batas kuartil dari semua EKG analisis utama
yang punya nilai; per kuartil AUROC rata-rata benih dan selisih M3a − M2, CI 95 % bootstrap bergugus pasien 2.000
(benih 20261113) di dalam kuartil. Deskriptif, tanpa uji heterogenitas.
Pakai: python-gpu analysis/omi_waktu.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, indeks_bootstrap  # noqa: E402


def main(B=2000):
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    ut = tr[tr.Paced != 1].reset_index(drop=True)
    y, g = ut.OMI.values.astype(int), ut.Patient_id.values
    o1 = pd.read_csv(AKAR / "oof_m01.csv")
    assert (o1.ecg_med_record.values == ut.ecg_med_record.values).all()
    o2 = np.load(AKAR / "oof_m2_utama.npz", allow_pickle=True)
    assert (o2["ecg_row_record"] == ut.ecg_row_record.values).all()
    o3 = np.load(AKAR / "oof_m3a.npz")
    P = {"M1": [o1[f"M1_{s}"].values for s in BENIH],
         "M2": [o2[f"M2_{s}"] for s in BENIH],
         "M3a": [o3[f"utama_{s}"] for s in BENIH]}
    ti = pd.to_numeric(ut.Time_Interval, errors="coerce")
    ada = ti.notna().values
    q, batas = pd.qcut(ti[ada], 4, labels=False, retbins=True)
    kuart = np.full(len(y), -1)
    kuart[ada] = q.values
    print("## Strata Time_Interval — analisis utama tanpa Paced (eksploratif, P4 butir 2)\n")
    print(f"n EKG = {len(y)}; tanpa Time_Interval {int((~ada).sum())} (dikeluarkan); Time_Interval < 0: "
          f"{int((ti < 0).sum())}. Batas kuartil (menit): " + ", ".join(f"{b:.0f}" for b in batas) + ".\n")

    def auc(yy, ps):
        return np.mean([roc_auc_score(yy, p) for p in ps])

    rng = np.random.default_rng(20261113)
    print("| Kuartil | Menit (rentang) | Jam (median) | n EKG | OMI (%) | M1 | M2 | M3a | M3a − M2 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for k in range(4):
        s = np.flatnonzero(kuart == k)
        ys, gs = y[s], g[s]
        sub = {m: [p[s] for p in ps] for m, ps in P.items()}
        titik = {m: auc(ys, ps) for m, ps in sub.items()}
        ulang = {m: [] for m in sub}
        beda = []
        for idx in indeks_bootstrap(gs, rng, B):
            if len(np.unique(ys[idx])) < 2:
                continue
            a = {m: auc(ys[idx], [p[idx] for p in ps]) for m, ps in sub.items()}
            for m in a:
                ulang[m].append(a[m])
            beda.append(a["M3a"] - a["M2"])

        def sel(t, v):
            return f"{t:.3f} [{np.quantile(v, .025):.3f}, {np.quantile(v, .975):.3f}]"

        tk = ti.values[s]
        print(f"| Q{k + 1} | {tk.min():.0f}–{tk.max():.0f} | {np.median(tk) / 60:.1f} | {len(s)} | "
              f"{ys.sum()} ({100 * ys.mean():.1f}) | " + " | ".join(sel(titik[m], ulang[m]) for m in sub)
              + f" | {sel(titik['M3a'] - titik['M2'], beda)} |")
        print(f"<!-- Q{k + 1}: replikat terpakai {len(beda)} dari {B} -->")


if __name__ == "__main__":
    main()
