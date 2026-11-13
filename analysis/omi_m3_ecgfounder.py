"""M3a — ECGFounder beku + probe regresi logistik L2 untuk artikel OMI (Prareg_OMI.md + Penyimpangan P3, 11 Nov 2026).

Model: PKUDigitalHealth/ECGFounder `12_lead_ECGFounder.pth` (MIT, SHA-256 ee199f37…aca7997), kode Net1D dari
NickLJLee/ECGFounder (MIT, komit 67367071), disimpan di luar repo ($ECGFOUNDER_CODE,
C:/Data/models/ECGFounder). Konfigurasi Net1D = ft_12lead_ECGFounder (finetune_model.py).

Pra-proses mengikuti kode resmi (dataset.py + util.filter_bandpass), ditetapkan sebelum dijalankan:
  1. Rekaman mentah 12 × 5.000 (500 Hz, 10 s), satuan mV (µV / 1000, seperti wfdb.rdsamp); urutan sadapan
     I, II, III, aVR, aVL, aVF, V1–V6 sama dengan urutan model. Rekaman pendek (2 di latih) diisi nol di ujung.
  2. filter_bandpass(·, 500): notch 50 Hz (Q 30), Butterworth orde 4 pita 0,67–40 Hz (filtfilt), lalu dikurangi
     median bergerak 201 sampel. Median bergerak dihitung dengan scipy.ndimage.median_filter(mode="constant", cval=0),
     setara scipy.signal.medfilt (bantalan nol) tetapi lebih cepat; kesetaraannya diperiksa pada 5 rekaman pertama.
  3. Normalisasi z-score atas seluruh larik 12 × 5.000 (satu rerata dan satu simpangan baku, seperti kode resmi).
Embedding = `deep_features` Net1D (rerata waktu keluaran tahap terakhir, 1.024 dimensi), mode eval, tanpa gradien.

Probe: SimpleImputer + StandardScaler + LogisticRegression L2, C dari CV bersarang dengan kisi dan log-loss sama
dengan M1 (omi_m01.oof dengan pilih=True). Lipatan, benih, bootstrap, ukuran, susunan analisis sama dengan M0/M1.

Pakai (GPU environment):
  python-gpu analysis/omi_m3_ecgfounder.py --embed          # tulis $OMI_DATA/emb_ecgfounder_train.npy
  python-gpu analysis/omi_m3_ecgfounder.py --probe [--boot 2000]
  python-gpu analysis/omi_m3_ecgfounder.py --embed-uji        # test.csv -> emb_ecgfounder_test.npy (P4 butir 4)
  python-gpu analysis/omi_m3_ecgfounder.py --kisi-lebar       # P4 butir 3, eksploratif
  python-gpu analysis/omi_m3_ecgfounder.py --server           # P4 butir 4: kirim_server_m3a.csv
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, AMBANG_NB, BENIH, TERITORI, metrik, oof, ringkas, tabel  # noqa: E402

import os  # noqa: E402
KODE = Path(os.environ.get("ECGFOUNDER_CODE", "ext/ECGFounder"))
BOBOT = Path(os.environ.get("ECGFOUNDER_WEIGHTS", "ext/12_lead_ECGFounder.pth"))
EMB = AKAR / "emb_ecgfounder_train.npy"


def baca_mentah(rec):
    a = np.fromfile(AKAR / "row_data" / rec, dtype="<i2")
    n = a.size // 12
    x = np.zeros((12, 5000), np.float64)
    x[:, :n] = a.reshape(n, 12).T / 1000.0
    return x


def praproses(x, cepat=True):
    from scipy.ndimage import median_filter
    from scipy.signal import butter, filtfilt, iirnotch, medfilt
    b, a = iirnotch(50, 30, 500)
    f = np.array([filtfilt(b, a, c) for c in x])
    b, a = butter(N=4, Wn=[0.67, 40], btype="bandpass", fs=500)
    f = np.array([filtfilt(b, a, c) for c in f])
    k = int(0.4 * 500) + 1
    base = (np.array([median_filter(c, size=k, mode="constant", cval=0.0) for c in f]) if cepat
            else np.array([medfilt(c, kernel_size=k) for c in f]))
    f = f - base
    return (f - f.mean()) / (f.std() + 1e-8)


def embed(csv="train.csv", keluar=EMB):
    import torch
    sys.path.insert(0, str(KODE))
    from net1d import Net1D
    tr = pd.read_csv(AKAR / "csv/CSV" / csv, dtype={"Patient_id": str})
    for rec in tr.ecg_row_record[:5]:
        x = baca_mentah(rec)
        assert np.allclose(praproses(x, True), praproses(x, False)), rec
    print("Median bergerak cepat = medfilt pada 5 rekaman pertama: ya.")
    dev = torch.device("cuda")
    m = Net1D(in_channels=12, base_filters=64, ratio=1, filter_list=[64, 160, 160, 400, 400, 1024, 1024],
              m_blocks_list=[2, 2, 2, 3, 3, 4, 4], kernel_size=16, stride=2, groups_width=16, verbose=False,
              use_bn=False, use_do=False, n_classes=150, return_features=True)
    # Titik periksa memuat skalar numpy di luar state_dict; hanya dua global itu yang diizinkan, tetap weights_only.
    import numpy.core.multiarray as nca
    # numpy 2: nama lama skalar dipetakan eksplisit; kelas dtype numpy ikut diizinkan
    izin = ([(nca.scalar, "numpy.core.multiarray.scalar"), np.dtype]
            + [getattr(np.dtypes, n) for n in dir(np.dtypes) if n.endswith("DType")])
    with torch.serialization.safe_globals(izin):
        ck = torch.load(BOBOT, map_location="cpu", weights_only=True)
    print(f"Kunci titik periksa: {sorted(ck)}.")
    sd = ck["state_dict"]
    hilang, lebih = m.load_state_dict(sd, strict=False)
    print(f"Muat bobot: kunci hilang {len(hilang)} {hilang[:4]}, kunci lebih {len(lebih)} {lebih[:4]}.")
    assert not [k for k in hilang if not k.startswith("dense.")], "bobot tidak termuat"
    m.to(dev).eval()
    E = np.zeros((len(tr), 1024), np.float32)
    t0, buf, idx = time.time(), [], []
    with torch.no_grad():
        for i, rec in enumerate(tr.ecg_row_record):
            buf.append(praproses(baca_mentah(rec)).astype(np.float32))
            idx.append(i)
            if len(buf) == 64 or i == len(tr) - 1:
                _, f = m(torch.from_numpy(np.stack(buf)).to(dev))
                E[idx] = f.cpu().numpy()
                buf, idx = [], []
            if i % 2000 == 0:
                print(f"  {i}/{len(tr)} ({(time.time() - t0) / 60:.1f} menit)", flush=True)
    assert np.isfinite(E).all()
    np.save(keluar, E)
    print(f"Embedding {E.shape} disimpan, {(time.time() - t0) / 60:.1f} menit.")


def biner(df, E, nama, B, rng):
    y = df.OMI.values.astype(int)
    g = df.Patient_id.values
    hasil = [oof(E, y, g, s, True) for s in BENIH]
    ps = [h[0][:, 1] for h in hasil]
    Cs = sorted({c for h in hasil for c in h[1]})
    titik, ci, ulang = ringkas(y, g, {"M3a": ps}, metrik, B, rng)
    print(f"\n### {nama}\n")
    print(f"n EKG = {len(y)}, pasien = {len(np.unique(g))}, OMI = {y.sum()} ({100 * y.mean():.2f} %). "
          f"C terpilih: {Cs}.\n")
    tabel(titik, ci, ["AUROC", "AUPRC", "Brier", "Se@Sp90", "slope", "intercept"], {})
    print(f"\nReplikat bootstrap dengan slope tak terhitung (P2): M3a {int(ulang['M3a']['slope'].isna().sum())} "
          f"dari {len(ulang['M3a'])}.\n")
    print("| Model | " + " | ".join(f"NB {int(t * 100)} %" for t in AMBANG_NB) + " |")
    print("| --- | " + " | ".join("---" for _ in AMBANG_NB) + " |")
    print("| M3a | " + " | ".join(
        f"{titik['M3a'][f'NB{int(t * 100)}']:.4f} [{ci['M3a'][0][f'NB{int(t * 100)}']:.4f}, "
        f"{ci['M3a'][1][f'NB{int(t * 100)}']:.4f}]" for t in AMBANG_NB) + " |")
    print("| Rawat semua | " + " | ".join(f"{titik['M3a'][f'NBall{int(t * 100)}']:.4f}" for t in AMBANG_NB) + " |")
    print("\nPer benih (AUROC): M3a " + ", ".join(f"{roc_auc_score(y, p):.3f}" for p in ps) + ".")
    return ps


def teritori(df, E, B, rng):
    akut = {t: (df[s] == 1).any(axis=1) for t, s in TERITORI.items()}
    jml = sum(a.astype(int) for a in akut.values())
    satu = ((df.OMI == 1) & (jml == 1) & (~akut["LM"])).values
    d = df[satu].copy()
    d["ter"] = np.select([akut["LAD"][satu], akut["LCX"][satu], akut["RCA"][satu]], [0, 1, 2])
    y, g, Es = d.ter.values, d.Patient_id.values, E[satu]
    nst = (d.NSTEMI == 1).values
    print("\n### Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)\n")
    print(f"n EKG = {len(y)} (LAD {np.sum(y == 0)}, LCX {np.sum(y == 1)}, RCA {np.sum(y == 2)}); "
          f"di antaranya NSTEMI-OMI {nst.sum()}.\n")

    def auc_ovr(yy, P):
        out = {nm: roc_auc_score(yy == k, P[:, k]) for k, nm in enumerate(["LAD", "LCX", "RCA"])}
        out["makro"] = np.mean(list(out.values()))
        return out

    ps = [oof(Es, y, g, s, True)[0] for s in BENIH]
    for sub, nama in [(np.ones(len(y), bool), "semua OMI satu teritori"), (nst, "NSTEMI-OMI (eksploratif)")]:
        titik, ci, _ = ringkas(y[sub], g[sub], {"M3a": [P[sub] for P in ps]}, auc_ovr, B, rng)
        print(f"**{nama}** (AUROC satu-lawan-sisanya)\n")
        tabel(titik, ci, ["LAD", "LCX", "RCA", "makro"], {})
        print()
    return ps


def probe(B):
    t0 = time.time()
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    E = np.load(EMB)
    assert E.shape == (len(tr), 1024)
    print(f"## M3a — ECGFounder beku + probe L2, 3 benih, bootstrap {B} bergugus pasien\n")
    rng = np.random.default_rng(20261111)
    iu = np.flatnonzero((tr.Paced != 1).values)
    utama = tr.iloc[iu].reset_index(drop=True)
    simpan = {"utama": biner(utama, E[iu], "Utama — OMI lawan bukan-OMI, tanpa Paced", B, rng)}
    jn = iu[(utama.NSTEMI == 1).values]
    simpan["nstemi"] = biner(tr.iloc[jn].reset_index(drop=True), E[jn],
                             "Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced", B, rng)
    simpan["teritori"] = teritori(utama, E[iu], B, rng)
    simpan["kepekaan"] = biner(tr.reset_index(drop=True), E, "Kepekaan — utama dengan Paced", B, rng)
    np.savez(AKAR / "oof_m3a.npz", **{f"{k}_{s}": p for k, ps in simpan.items() for s, p in zip(BENIH, ps)})
    print(f"\nWaktu jalan: {(time.time() - t0) / 60:.1f} menit.")


def kisi_lebar(B):
    """P4 butir 3 (eksploratif): M3a analisis utama dengan kisi C diperlebar ke bawah."""
    import omi_m01
    omi_m01.C_GRID = [1e-6, 1e-5, 1e-4] + omi_m01.C_GRID
    t0 = time.time()
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    E = np.load(EMB)
    iu = np.flatnonzero((tr.Paced != 1).values)
    print(f"## M3a — kisi C diperlebar {omi_m01.C_GRID} (kepekaan, P4 butir 3), bootstrap {B}\n")
    ps = biner(tr.iloc[iu].reset_index(drop=True), E[iu], "Utama — kisi lebar", B, np.random.default_rng(20261114))
    np.savez(AKAR / "oof_m3a_kisilebar.npz", **{f"utama_{s}": p for s, p in zip(BENIH, ps)})
    print(f"\nWaktu jalan: {(time.time() - t0) / 60:.1f} menit.")


def server():
    """P4 butir 4: model akhir M3a (kisi terkunci) atas semua EKG analisis utama, prediksi biner test.csv."""
    from omi_m01 import pilih_C, pipa
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    te = pd.read_csv(AKAR / "csv/CSV/test.csv", dtype={"Patient_id": str})
    E, Et = np.load(EMB), np.load(EMB_UJI)
    assert Et.shape == (len(te), 1024)
    iu = np.flatnonzero((tr.Paced != 1).values)
    y, g = tr.OMI.values[iu].astype(int), tr.Patient_id.values[iu]
    C = pilih_C(E[iu], y, g, BENIH[0])
    m = pipa(C).fit(E[iu], y)
    o3 = np.load(AKAR / "oof_m3a.npz")
    ambang = [np.quantile(o3[f"utama_{s}"][y == 0], 0.9) for s in BENIH]
    thr = float(np.mean(ambang))
    p = m.predict_proba(Et)[:, 1]
    lab = (p >= thr).astype(int)
    dasar = te[["Patient_id", "ecg_row_record", "ecg_med_record"]]
    dasar.assign(OMI=lab).to_csv(AKAR / "kirim_server_m3a.csv", index=False)
    dasar.assign(p_OMI=p, OMI=lab).to_csv(AKAR / "kirim_server_m3a_prob.csv", index=False)
    print("## Server penilai — prediksi M3a untuk test.csv (P4 butir 4)\n")
    print(f"C terpilih (semua EKG analisis utama, benih {BENIH[0]}): {C}. Ambang Sp90 OOF per benih: "
          + ", ".join(f"{a:.4f}" for a in ambang) + f"; rata-rata {thr:.4f}.")
    print(f"Prevalensi OMI latih analisis utama {100 * y.mean():.2f} %. Test: n EKG {len(te)}, pasien "
          f"{te.Patient_id.nunique()}; prediksi positif {lab.sum()} ({100 * lab.mean():.2f} %); "
          f"median p {np.median(p):.4f}.")
    print("Berkas: kirim_server_m3a.csv (biner, untuk diunggah) dan kirim_server_m3a_prob.csv (tidak diunggah).")


EMB_UJI = AKAR / "emb_ecgfounder_test.npy"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--embed", action="store_true")
    ap.add_argument("--embed-uji", action="store_true")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--kisi-lebar", action="store_true")
    ap.add_argument("--server", action="store_true")
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    if a.embed:
        embed()
    if a.embed_uji:
        embed("test.csv", EMB_UJI)
    if a.probe:
        probe(a.boot)
    if a.kisi_lebar:
        kisi_lebar(a.boot)
    if a.server:
        server()
