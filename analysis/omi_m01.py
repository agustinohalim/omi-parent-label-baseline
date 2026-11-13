"""M0 (usia + jenis kelamin) dan M1 (ciri ST denyut median) untuk artikel OMI, validasi silang per pasien.

Rancangan: Prareg_OMI.md bagian 1–5 dan Penyimpangan P1 (11 Nov 2026). Tidak menyentuh test.csv (server
penilai dipakai sekali di akhir untuk model terbaik). Masukan di luar repo:
    $OMI_DATA/csv/CSV/train.csv
    $OMI_DATA/ciri_st_train.csv      (dari omi_ciri_st.py)
Keluaran: tabel Markdown di stdout (disalin apa adanya ke Hasil_OMI_1.md) dan prediksi out-of-fold
$OMI_DATA/oof_m01.csv.

Pakai:
    python-gpu analysis/omi_m01.py [--boot 2000]
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import os  # noqa: E402
AKAR = Path(os.environ.get("OMI_DATA", "data/chongqing"))
BENIH = [20261107, 20261108, 20261109]
C_GRID = [1e-3, 1e-2, 1e-1, 1, 10, 100]
AMBANG_NB = [0.01, 0.02, 0.05, 0.10]
SADAPAN = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
CIRI_ST = [f"st60_{s}" for s in SADAPAN] + [f"st80_{s}" for s in SADAPAN]
TERITORI = {"LAD": ["PLAD", "MLAD", "DLAD", "DB"], "LCX": ["PLCX", "MLCX", "DLCX", "OM"],
            "RCA": ["PRCA", "MRCA", "DRCA"], "LM": ["LM"]}


def pipa(C):
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                         LogisticRegression(C=C, max_iter=2000))


def lipatan(y, g, benih):
    """5 lipatan per pasien, berstrata: label pasien = label terbesar EKG-nya (biner) atau label EKG pertama
    (multikelas). Setara StratifiedGroupKFold untuk data ini (855 dari 17.018 pasien punya > 1 EKG), jauh lebih cepat."""
    d = pd.DataFrame({"y": y, "g": g})
    lab = d.groupby("g", sort=True).y.max() if len(np.unique(y)) == 2 else d.groupby("g", sort=True).y.first()
    pas = lab.index.values
    f_pas = np.empty(len(pas), int)
    for k, (_, b) in enumerate(StratifiedKFold(5, shuffle=True, random_state=benih).split(pas, lab.values)):
        f_pas[b] = k
    f = pd.Series(f_pas, index=pas).loc[g].values
    return [(np.flatnonzero(f != k), np.flatnonzero(f == k)) for k in range(5)]


def pilih_C(X, y, g, benih):
    terbaik, skor_terbaik = None, np.inf
    split = lipatan(y, g, benih)
    for C in C_GRID:
        ll = []
        for a, b in split:
            m = pipa(C).fit(X[a], y[a])
            p = np.clip(m.predict_proba(X[b]), 1e-12, 1)
            ll.append(-np.mean(np.log(p[np.arange(len(b)), np.searchsorted(m.classes_, y[b])])))
        if np.mean(ll) < skor_terbaik:
            terbaik, skor_terbaik = C, np.mean(ll)
    return terbaik


def oof(X, y, g, benih, pilih):
    """Prediksi out-of-fold. pilih=True: C dari CV dalam; selain itu C = 1."""
    kelas = np.unique(y)
    P = np.zeros((len(y), len(kelas)))
    Cs = []
    for a, b in lipatan(y, g, benih):
        C = pilih_C(X[a], y[a], g[a], benih) if pilih else 1.0
        Cs.append(C)
        P[b] = pipa(C).fit(X[a], y[a]).predict_proba(X[b])
    return P, Cs


def logistik_1d(x, y, offset_saja=False):
    """Newton teredam (P2, 11 Nov 2026): y ~ a + b*x (atau a + x bila offset_saja). Kembalikan (a, b).

    Langkah dipotong separuh sampai log-likelihood tidak turun; eta dibatasi +-30 agar exp tidak meluap.
    Tak konvergen dalam 100 iterasi, atau |b| > 1e3 (pemisahan / prediksi hampir konstan) -> (nan, nan),
    dan replikat itu tidak ikut kuantil CI (jumlahnya dilaporkan).
    """
    def ll(a, b):
        eta = np.clip(a + (x if offset_saja else b * x), -30, 30)
        return np.sum(y * eta - np.log1p(np.exp(eta)))

    p0 = np.clip(y.mean(), 1e-6, 1 - 1e-6)
    a, b = float(np.log(p0 / (1 - p0))), 1.0
    lama = ll(a, b)
    for _ in range(100):
        eta = np.clip(a + (x if offset_saja else b * x), -30, 30)
        p = 1 / (1 + np.exp(-eta))
        w = np.clip(p * (1 - p), 1e-12, None)
        if offset_saja:
            step = np.array([np.sum(y - p) / np.sum(w), 0.0])
        else:
            Xd = np.column_stack([np.ones_like(x), x])
            H = Xd.T @ (Xd * w[:, None])
            step = np.linalg.lstsq(H, Xd.T @ (y - p), rcond=None)[0]
        t = 1.0
        for _ in range(40):
            baru = ll(a + t * step[0], b + (0 if offset_saja else t * step[1]))
            if baru >= lama - 1e-12:
                break
            t /= 2
        a, b = a + t * step[0], b + (0 if offset_saja else t * step[1])
        lama = baru
        if np.max(np.abs(t * step)) < 1e-8:
            return (a, b) if abs(b) <= 1e3 else (np.nan, np.nan)
    return np.nan, np.nan


def metrik(y, p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    lg = np.log(p / (1 - p))
    _, slope = logistik_1d(lg, y)
    intercept, _ = logistik_1d(lg, y, offset_saja=True)
    thr = np.quantile(p[y == 0], 0.9)
    out = {"AUROC": roc_auc_score(y, p), "AUPRC": average_precision_score(y, p),
           "Brier": np.mean((p - y) ** 2), "slope": slope, "intercept": intercept,
           "Se@Sp90": np.mean(p[y == 1] > thr)}
    n, prev = len(y), y.mean()
    for t in AMBANG_NB:
        tp = np.sum((p >= t) & (y == 1)) / n
        fp = np.sum((p >= t) & (y == 0)) / n
        out[f"NB{int(t * 100)}"] = tp - fp * t / (1 - t)
        out[f"NBall{int(t * 100)}"] = prev - (1 - prev) * t / (1 - t)
    return out


def indeks_bootstrap(g, rng, B):
    """Ulangan bootstrap bergugus pasien: daftar array indeks baris."""
    unik, inv = np.unique(g, return_inverse=True)
    baris_per = [np.flatnonzero(inv == k) for k in range(len(unik))]
    for _ in range(B):
        pilih = rng.integers(0, len(unik), len(unik))
        yield np.concatenate([baris_per[k] for k in pilih])


def ringkas(y, g, prediksi, fungsi, B, rng):
    """prediksi: {model: [p_benih1, p_benih2, p_benih3]}. Titik = rata-rata metrik antarbenih; CI bootstrap."""
    titik = {m: pd.DataFrame([fungsi(y, p) for p in ps]).mean() for m, ps in prediksi.items()}
    ulang = {m: [] for m in prediksi}
    for idx in indeks_bootstrap(g, rng, B):
        if len(np.unique(y[idx])) < 2:
            continue
        for m, ps in prediksi.items():
            ulang[m].append(pd.DataFrame([fungsi(y[idx], p[idx]) for p in ps]).mean())
    ci = {m: (pd.DataFrame(v).quantile(0.025), pd.DataFrame(v).quantile(0.975)) for m, v in ulang.items()}
    return titik, ci, {m: pd.DataFrame(v) for m, v in ulang.items()}


def tabel(titik, ci, kolom, judul_model):
    print("| Model | " + " | ".join(kolom) + " |")
    print("| --- | " + " | ".join("---" for _ in kolom) + " |")
    for m in titik:
        sel = [f"{titik[m][k]:.3f} [{ci[m][0][k]:.3f}, {ci[m][1][k]:.3f}]" for k in kolom]
        print(f"| {judul_model.get(m, m)} | " + " | ".join(sel) + " |")


def biner(df, X_kolom, nama, B, rng, simpan=None):
    y = df.OMI.values.astype(int)
    g = df.Patient_id.values
    prediksi, Cs = {}, {}
    for m, kol, pilih in [("M0", ["age", "gender"], False), ("M1", CIRI_ST, True),
                          ("M0+M1", ["age", "gender"] + CIRI_ST, True)]:
        X = df[kol].values.astype(float)
        hasil = [oof(X, y, g, s, pilih) for s in BENIH]
        prediksi[m] = [h[0][:, 1] for h in hasil]
        Cs[m] = sorted({c for h in hasil for c in h[1]})
    titik, ci, ulang = ringkas(y, g, prediksi, metrik, B, rng)
    print(f"\n### {nama}\n")
    print(f"n EKG = {len(y)}, pasien = {len(np.unique(g))}, OMI = {y.sum()} ({100 * y.mean():.2f} %). "
          f"C terpilih (semua lipatan dan benih): " + "; ".join(f"{m} {Cs[m]}" for m in Cs) + ".\n")
    tabel(titik, ci, ["AUROC", "AUPRC", "Brier", "Se@Sp90", "slope", "intercept"], {})
    print("\nReplikat bootstrap dengan slope tak terhitung (P2): " + "; ".join(
        f"{m} {int(ulang[m]['slope'].isna().sum())} dari {len(ulang[m])}" for m in ulang) + ".")
    print()
    print("| Model | " + " | ".join(f"NB {int(t * 100)} %" for t in AMBANG_NB) + " |")
    print("| --- | " + " | ".join("---" for _ in AMBANG_NB) + " |")
    for m in titik:
        print(f"| {m} | " + " | ".join(
            f"{titik[m][f'NB{int(t * 100)}']:.4f} [{ci[m][0][f'NB{int(t * 100)}']:.4f}, "
            f"{ci[m][1][f'NB{int(t * 100)}']:.4f}]" for t in AMBANG_NB) + " |")
    m0 = titik["M0"]
    print("| Rawat semua | " + " | ".join(f"{m0[f'NBall{int(t * 100)}']:.4f}" for t in AMBANG_NB) + " |")
    d = ulang["M1"]["AUROC"].values - ulang["M0"]["AUROC"].values
    d2 = ulang["M0+M1"]["AUROC"].values - ulang["M1"]["AUROC"].values
    print(f"\nSelisih AUROC (deskriptif, bootstrap berpasangan): M1 − M0 = "
          f"{titik['M1']['AUROC'] - titik['M0']['AUROC']:.3f} [{np.quantile(d, .025):.3f}, {np.quantile(d, .975):.3f}]; "
          f"M0+M1 − M1 = {titik['M0+M1']['AUROC'] - titik['M1']['AUROC']:.3f} "
          f"[{np.quantile(d2, .025):.3f}, {np.quantile(d2, .975):.3f}].")
    print("\nPer benih (AUROC): " + "; ".join(
        f"{m} " + ", ".join(f"{roc_auc_score(y, p):.3f}" for p in prediksi[m]) for m in prediksi) + ".")
    if simpan is not None:
        out = pd.DataFrame({"ecg_med_record": df.ecg_med_record.values, "OMI": y})
        for m, ps in prediksi.items():
            for s, p in zip(BENIH, ps):
                out[f"{m}_{s}"] = p
        out.to_csv(simpan, index=False)


def teritori(df, B, rng):
    akut = {t: (df[s] == 1).any(axis=1) for t, s in TERITORI.items()}
    jml = sum(a.astype(int) for a in akut.values())
    satu = (df.OMI == 1) & (jml == 1) & (~akut["LM"])
    d = df[satu].copy()
    d["ter"] = np.select([akut["LAD"][satu], akut["LCX"][satu], akut["RCA"][satu]], [0, 1, 2])
    y, g = d.ter.values, d.Patient_id.values
    nst = (d.NSTEMI == 1).values
    print(f"\n### Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)\n")
    print(f"n EKG = {len(y)} (LAD {np.sum(y == 0)}, LCX {np.sum(y == 1)}, RCA {np.sum(y == 2)}); "
          f"di antaranya NSTEMI-OMI {nst.sum()} (LAD {np.sum(y[nst] == 0)}, LCX {np.sum(y[nst] == 1)}, "
          f"RCA {np.sum(y[nst] == 2)}).\n")

    def auc_ovr(yy, P):
        out = {}
        for k, nm in enumerate(["LAD", "LCX", "RCA"]):
            out[nm] = roc_auc_score(yy == k, P[:, k])
        out["makro"] = np.mean(list(out.values()))
        return out

    for sub, nama in [(np.ones(len(y), bool), "semua OMI satu teritori"), (nst, "NSTEMI-OMI (eksploratif)")]:
        prediksi = {}
        for m, kol, pilih in [("M0", ["age", "gender"], False), ("M1", CIRI_ST, True)]:
            X = d[kol].values.astype(float)
            prediksi[m] = [oof(X, y, g, s, pilih)[0] for s in BENIH]
        pr_sub = {m: [P[sub] for P in ps] for m, ps in prediksi.items()}
        titik, ci, _ = ringkas(y[sub], g[sub], pr_sub, auc_ovr, B, rng)
        print(f"**{nama}** (AUROC satu-lawan-sisanya)\n")
        tabel(titik, ci, ["LAD", "LCX", "RCA", "makro"], {})
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=2000)
    B = ap.parse_args().boot
    t0 = time.time()
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    st = pd.read_csv(AKAR / "ciri_st_train.csv")
    assert (st.ecg_med_record.values == tr.ecg_med_record.values).all()
    df = pd.concat([tr, st.drop(columns=["ecg_med_record"])], axis=1)
    rng = np.random.default_rng(20261111)
    utama = df[df.Paced != 1].reset_index(drop=True)
    print(f"## M0/M1 — validasi silang 5 lipatan per pasien, 3 benih, bootstrap {B} bergugus pasien\n")
    print(f"Ciri ST kosong (gagal deteksi, diisi median lipatan latih): {int(utama.st60_I.isna().sum())} "
          f"dari {len(utama)} EKG analisis utama.")
    biner(utama, CIRI_ST, "Utama — OMI lawan bukan-OMI, tanpa Paced", B, rng, AKAR / "oof_m01.csv")
    nst = utama[utama.NSTEMI == 1].reset_index(drop=True)
    biner(nst, CIRI_ST, "Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced", B, rng)
    teritori(utama, B, rng)
    biner(df.reset_index(drop=True), CIRI_ST, "Kepekaan — utama dengan Paced", B, rng)
    print(f"\nWaktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
