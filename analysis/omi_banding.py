"""Perbandingan utama OMI (Prareg_OMI.md bagian 4): M3 terbaik lawan M2 dan lawan M1, analisis utama tanpa Paced.

Masukan (prediksi out-of-fold, urutan baris = train.csv tanpa Paced, sama untuk semua model):
  $OMI_DATA/oof_m01.csv          M0, M1 per benih (omi_m01.py)
  $OMI_DATA/oof_m2_utama.npz     M2 per benih (omi_m2.py)
  $OMI_DATA/oof_m3a.npz          M3a per benih, kunci utama_<benih> (omi_m3_ecgfounder.py)
M3 terbaik = model M3 dengan AUROC rata-rata benih tertinggi (sekarang hanya M3a; pemilihan dinyatakan sebagai sumber
optimisme bila ada lebih dari satu).

Ukuran:
  - DeLong berpasangan (Sun & Xu 2014) per benih: selisih AUROC, galat baku, p dua sisi. DeLong menganggap EKG saling
    bebas; 855 pasien punya > 1 EKG, jadi p ini sedikit terlalu optimistis — karena itu juga:
  - Bootstrap bergugus pasien 2.000 (benih 20261112): selisih AUROC rata-rata tiga benih, CI persentil 95 %.
Pakai: python-gpu analysis/omi_banding.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, indeks_bootstrap  # noqa: E402


def delong(y, a, b):
    """Selisih AUROC a − b, galat baku, p (DeLong, algoritme cepat Sun & Xu)."""
    pos, neg = y == 1, y == 0
    m, n = pos.sum(), neg.sum()

    def komponen(s):
        from scipy.stats import rankdata
        r_all = rankdata(s)
        r_pos = rankdata(s[pos])
        r_neg = rankdata(s[neg])
        auc = (r_all[pos].sum() - m * (m + 1) / 2) / (m * n)
        v10 = (r_all[pos] - r_pos) / n
        v01 = 1 - (r_all[neg] - r_neg) / m
        return auc, v10, v01

    a1, v10a, v01a = komponen(a)
    a2, v10b, v01b = komponen(b)
    s10 = np.cov(np.vstack([v10a, v10b]))
    s01 = np.cov(np.vstack([v01a, v01b]))
    S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    d = a1 - a2
    se = np.sqrt(var)
    return d, se, 2 * norm.sf(abs(d) / se)


def main():
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
    for m, ps in P.items():
        assert all(len(p) == len(y) for p in ps), m
    auc = {m: np.mean([roc_auc_score(y, p) for p in ps]) for m, ps in P.items()}
    m3 = max([k for k in P if k.startswith("M3")], key=auc.get)
    print("## Perbandingan utama — analisis utama tanpa Paced\n")
    print(f"n EKG = {len(y)}, OMI = {y.sum()}. AUROC rata-rata benih: "
          + "; ".join(f"{m} {v:.3f}" for m, v in auc.items()) + f". M3 terbaik: {m3}.\n")
    pasangan = [(m3, "M2"), (m3, "M1"), ("M2", "M1")]
    print("| Perbandingan | Benih | Selisih AUROC | SE DeLong | p DeLong |")
    print("| --- | --- | --- | --- | --- |")
    for a, b in pasangan:
        for s, pa, pb in zip(BENIH, P[a], P[b]):
            d, se, p = delong(y, pa, pb)
            print(f"| {a} − {b} | {s} | {d:.3f} | {se:.4f} | {p:.2g} |")
    rng = np.random.default_rng(20261112)
    ulang = {k: [] for k in pasangan}
    for idx in indeks_bootstrap(g, rng, 2000):
        if len(np.unique(y[idx])) < 2:
            continue
        a_m = {m: np.mean([roc_auc_score(y[idx], p[idx]) for p in ps]) for m, ps in P.items()}
        for a, b in pasangan:
            ulang[(a, b)].append(a_m[a] - a_m[b])
    print("\n| Perbandingan | Selisih AUROC (rata-rata benih) | CI 95 % bootstrap bergugus pasien |")
    print("| --- | --- | --- |")
    for a, b in pasangan:
        v = np.array(ulang[(a, b)])
        print(f"| {a} − {b} | {auc[a] - auc[b]:.3f} | [{np.quantile(v, .025):.3f}, {np.quantile(v, .975):.3f}] |")
    print(f"\nReplikat bootstrap terpakai: {len(ulang[pasangan[0]])} dari 2000.")


if __name__ == "__main__":
    main()
