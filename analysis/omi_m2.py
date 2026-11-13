"""M2 — CNN 1D pada EKG mentah 10 s untuk artikel OMI (Prareg_OMI.md bagian 3 + Penyimpangan P3, 11 Nov 2026).

Resep pola Arrest (Uji_Arrest/02_cnn_arrest.py) apa adanya: masukan 12 × 2.500 (500 → 250 Hz, rerata dua sampel),
rerata per sadapan dibuang, dibagi simpangan baku global lipatan latih; empat blok Conv1d(7) + BatchNorm + ReLU +
MaxPool(4), kanal 32-64-64-128, rerata global, dropout 0,3, linear. Adam 1e-3, 20 epoch tetap, batch 64, bobot kelas
seimbang (biner: pos_weight = (1 − p)/p; teritori: bobot CrossEntropy n/(3·n_k)). Model epoch terakhir.

Lipatan, benih, bootstrap, ukuran, dan susunan analisis sama dengan omi_m01.py (fungsi diimpor dari sana):
utama tanpa Paced; sekunder 1 dilatih ulang di dalam NSTEMI; sekunder 2 softmax tiga kelas pada OMI satu teritori
(NSTEMI-OMI = subset prediksi model semua-OMI, sama dengan M1); kepekaan dengan Paced. Tidak menyentuh test.csv.

Masukan di luar repo: $OMI_DATA/csv/CSV/train.csv, $OMI_DATA/row_data/*.dat (WFDB format 16,
12 sadapan berselang, 5.000 sampel, 1000/mV;
rekaman yang lebih pendek diisi nol di ujung sesudah rerata dibuang, jumlahnya dicetak). Singgahan $OMI_DATA/raw250_train.npy (float16, µV).
Keluaran: tabel Markdown di stdout; prediksi out-of-fold $OMI_DATA/oof_m2_<analisis>.npz.

Pakai (GPU environment):  python-gpu analysis/omi_m2.py [--boot 2000] [--uji]
--uji = satu benih, 2 epoch, bootstrap 20, hanya analisis utama (cek jalan, angkanya tidak dipakai).
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import (AKAR, AMBANG_NB, BENIH, TERITORI, lipatan, metrik, ringkas, tabel)  # noqa: E402

EPOCH, BATCH = 20, 64
DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def muat_sinyal(tr):
    cache = AKAR / "raw250_train.npy"
    if cache.exists():
        X = np.load(cache, mmap_mode="r")
        assert X.shape == (len(tr), 12, 2500)
        return X
    X = np.empty((len(tr), 12, 2500), np.float16)
    for i, rec in enumerate(tr.ecg_row_record):
        a = np.fromfile(AKAR / "row_data" / rec, dtype="<i2")
        n = a.size // 12
        assert a.size % 24 == 0 and n <= 5000, rec
        x = a.reshape(n, 12).T.astype(np.float32).reshape(12, n // 2, 2).mean(axis=2)
        x = x - x.mean(axis=1, keepdims=True)
        X[i] = 0
        X[i, :, :n // 2] = x  # rekaman pendek (2 di latih, 7 s) diisi nol di ujung
        if n < 5000:
            print(f"Rekaman pendek: {rec}, {n} sampel; diisi nol sampai 5.000.")
    np.save(cache, X)
    return np.load(cache, mmap_mode="r")


class Jaringan(nn.Module):
    def __init__(self, keluaran=1):
        super().__init__()
        blok, cin = [], 12
        for cout in (32, 64, 64, 128):
            blok += [nn.Conv1d(cin, cout, 7, padding=3), nn.BatchNorm1d(cout), nn.ReLU(), nn.MaxPool1d(4)]
            cin = cout
        self.fitur = nn.Sequential(*blok)
        self.kepala = nn.Sequential(nn.Dropout(0.3), nn.Linear(128, keluaran))

    def forward(self, x):
        return self.kepala(self.fitur(x).mean(dim=2))


def latih_prediksi(X, y, a, b, benih, epoch):
    """X: larik (n, 12, 2500) float16 di CPU; a/b indeks latih/uji. Kembalikan probabilitas (len(b), k)."""
    torch.manual_seed(benih)
    np.random.seed(benih)
    kelas = np.unique(y)
    biner = len(kelas) == 2
    xa = torch.from_numpy(np.ascontiguousarray(X[a])).to(DEV)
    sd = float(torch.std(xa.float())) + 1e-6
    ya = torch.tensor(y[a], device=DEV)
    m = Jaringan(1 if biner else len(kelas)).to(DEV)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    if biner:
        p = y[a].mean()
        loss = nn.BCEWithLogitsLoss(pos_weight=torch.tensor((1 - p) / p, dtype=torch.float32, device=DEV))
    else:
        n_k = np.bincount(y[a], minlength=len(kelas))
        w = torch.tensor(len(a) / (len(kelas) * n_k), dtype=torch.float32, device=DEV)
        loss = nn.CrossEntropyLoss(weight=w)
    g = torch.Generator(device="cpu").manual_seed(benih)
    for _ in range(epoch):
        m.train()
        perm = torch.randperm(len(a), generator=g).to(DEV)
        for i in range(0, len(a), BATCH):
            j = perm[i:i + BATCH]
            out = m(xa[j].float() / sd)
            opt.zero_grad()
            (loss(out.squeeze(1), ya[j].float()) if biner else loss(out, ya[j].long())).backward()
            opt.step()
    del xa
    m.eval()
    hasil = []
    with torch.no_grad():
        for i in range(0, len(b), 512):
            xb = torch.from_numpy(np.ascontiguousarray(X[b[i:i + 512]])).to(DEV).float() / sd
            o = m(xb)
            hasil.append((torch.sigmoid(o) if biner else torch.softmax(o, 1)).cpu().numpy())
    P = np.concatenate(hasil)
    return np.column_stack([1 - P[:, 0], P[:, 0]]) if biner else P


def oof(X, y, g, benih, epoch):
    k = len(np.unique(y))
    P = np.zeros((len(y), k))
    for a, b in lipatan(y, g, benih):
        P[b] = latih_prediksi(X, y, a, b, benih, epoch)
    return P


def biner(df, X, nama, B, rng, benih, epoch, simpan):
    y = df.OMI.values.astype(int)
    g = df.Patient_id.values
    t0 = time.time()
    ps = [oof(X, y, g, s, epoch)[:, 1] for s in benih]
    np.savez(simpan, ecg_row_record=df.ecg_row_record.values, OMI=y, **{f"M2_{s}": p for s, p in zip(benih, ps)})
    titik, ci, ulang = ringkas(y, g, {"M2": ps}, metrik, B, rng)
    print(f"\n### {nama}\n")
    print(f"n EKG = {len(y)}, pasien = {len(np.unique(g))}, OMI = {y.sum()} ({100 * y.mean():.2f} %). "
          f"Waktu latih: {(time.time() - t0) / 60:.1f} menit.\n")
    tabel(titik, ci, ["AUROC", "AUPRC", "Brier", "Se@Sp90", "slope", "intercept"], {})
    print(f"\nReplikat bootstrap dengan slope tak terhitung (P2): M2 {int(ulang['M2']['slope'].isna().sum())} "
          f"dari {len(ulang['M2'])}.\n")
    print("| Model | " + " | ".join(f"NB {int(t * 100)} %" for t in AMBANG_NB) + " |")
    print("| --- | " + " | ".join("---" for _ in AMBANG_NB) + " |")
    print("| M2 | " + " | ".join(
        f"{titik['M2'][f'NB{int(t * 100)}']:.4f} [{ci['M2'][0][f'NB{int(t * 100)}']:.4f}, "
        f"{ci['M2'][1][f'NB{int(t * 100)}']:.4f}]" for t in AMBANG_NB) + " |")
    print("| Rawat semua | " + " | ".join(f"{titik['M2'][f'NBall{int(t * 100)}']:.4f}" for t in AMBANG_NB) + " |")
    from sklearn.metrics import roc_auc_score
    print("\nPer benih (AUROC): M2 " + ", ".join(f"{roc_auc_score(y, p):.3f}" for p in ps) + ".")


def teritori(df, X, B, rng, benih, epoch, simpan):
    from sklearn.metrics import roc_auc_score
    akut = {t: (df[s] == 1).any(axis=1) for t, s in TERITORI.items()}
    jml = sum(a.astype(int) for a in akut.values())
    satu = ((df.OMI == 1) & (jml == 1) & (~akut["LM"])).values
    d = df[satu].copy()
    d["ter"] = np.select([akut["LAD"][satu], akut["LCX"][satu], akut["RCA"][satu]], [0, 1, 2])
    y, g = d.ter.values, d.Patient_id.values
    Xs = X[np.flatnonzero(satu)]
    nst = (d.NSTEMI == 1).values
    print("\n### Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)\n")
    print(f"n EKG = {len(y)} (LAD {np.sum(y == 0)}, LCX {np.sum(y == 1)}, RCA {np.sum(y == 2)}); "
          f"di antaranya NSTEMI-OMI {nst.sum()}.\n")

    def auc_ovr(yy, P):
        out = {nm: roc_auc_score(yy == k, P[:, k]) for k, nm in enumerate(["LAD", "LCX", "RCA"])}
        out["makro"] = np.mean(list(out.values()))
        return out

    ps = [oof(Xs, y, g, s, epoch) for s in benih]
    np.savez(simpan, ecg_row_record=d.ecg_row_record.values, ter=y, **{f"M2_{s}": p for s, p in zip(benih, ps)})
    for sub, nama in [(np.ones(len(y), bool), "semua OMI satu teritori"), (nst, "NSTEMI-OMI (eksploratif)")]:
        titik, ci, _ = ringkas(y[sub], g[sub], {"M2": [P[sub] for P in ps]}, auc_ovr, B, rng)
        print(f"**{nama}** (AUROC satu-lawan-sisanya)\n")
        tabel(titik, ci, ["LAD", "LCX", "RCA", "makro"], {})
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--uji", action="store_true")
    arg = ap.parse_args()
    B, benih, epoch = (20, BENIH[:1], 2) if arg.uji else (arg.boot, BENIH, EPOCH)
    t0 = time.time()
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    X = muat_sinyal(tr)
    print(f"## M2 — CNN 1D pola Arrest, {DEV}, {len(benih)} benih, {epoch} epoch, bootstrap {B}"
          f"{' (UJI JALAN, ANGKA TIDAK DIPAKAI)' if arg.uji else ''}\n")
    print(f"Sinyal dimuat: {X.shape}, {(time.time() - t0) / 60:.1f} menit.")
    rng = np.random.default_rng(20261111)
    iu = np.flatnonzero((tr.Paced != 1).values)
    utama = tr.iloc[iu].reset_index(drop=True)
    akhiran = "_uji" if arg.uji else ""
    biner(utama, X[iu] if arg.uji else np.asarray(X[iu]), "Utama — OMI lawan bukan-OMI, tanpa Paced", B, rng,
          benih, epoch, AKAR / f"oof_m2_utama{akhiran}.npz")
    if not arg.uji:
        jn = iu[(utama.NSTEMI == 1).values]
        biner(tr.iloc[jn].reset_index(drop=True), np.asarray(X[jn]),
              "Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced", B, rng, benih, epoch,
              AKAR / "oof_m2_nstemi.npz")
        teritori(utama, np.asarray(X[iu]), B, rng, benih, epoch, AKAR / "oof_m2_teritori.npz")
        biner(tr.reset_index(drop=True), np.asarray(X), "Kepekaan — utama dengan Paced", B, rng, benih, epoch,
              AKAR / "oof_m2_kepekaan.npz")
    print(f"\nWaktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
