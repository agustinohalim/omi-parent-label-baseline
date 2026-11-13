"""Cek titik J dan tata letak berkas .med untuk ciri ST M1 (Hasil_OMI_1.md §7, ⬜ sebelum angka M1 masuk naskah).

Di luar pra-daftar, deskriptif, tanpa label: tidak membaca kolom hasil apa pun dan tidak mengubah ciri atau model.
Dua pemeriksaan:
1. Tata letak .med (objektif): bila susunan (500, 12) benar, hukum Einthoven berlaku per sampel — III = II − I dan
   aVR = −(I + II) / 2. Galat relatif dihitung untuk susunan yang dipakai `omi_ciri_st.py` dan untuk susunan
   alternatif (12, 500), pada semua EKG latih analisis utama (Paced != 1).
2. Titik J (visual): 30 EKG analisis utama dengan status ciri "ok", dipilih acak (benih 20261115). Tiap EKG satu
   panel: 12 sadapan ditumpuk (dikurangi garis PR masing-masing), garis tegak di awal QRS, titik J, J+60 ms, dan
   jendela PR. Dua halaman PNG ke folder keluaran; dibaca asisten AI (bukan manusia).
3. Jumlah EKG dengan |ST60| di sadapan mana pun di atas 0,5 / 1 / 2 / 5 mV (artefak; ditambahkan sesudah gambar
   menunjukkan satu sadapan V6 ±15 mV pada 07712.med).
Data di luar repo: $OMI_DATA. Keluaran gambar: argumen pertama (folder), bukan repo.

Pakai:
    python-gpu analysis/omi_cek_titik_j.py <folder_keluaran>
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from omi_ciri_st import AKAR, FS, SADAPAN, baca_med, deteksi  # noqa: E402


def galat_einthoven(x):
    i, ii, iii, avr = x[0], x[1], x[2], x[3]
    skala = np.abs(x[:6]).mean() + 1e-9
    return (np.abs(iii - (ii - i)).mean() / skala, np.abs(avr + (i + ii) / 2).mean() / skala)


def main(keluar):
    keluar = Path(keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    ut = tr[tr.Paced != 1].reset_index(drop=True)
    ci = pd.read_csv(AKAR / "ciri_st_train.csv")
    ok = set(ci.loc[ci.status == "ok", "ecg_med_record"])

    print("## Cek tata letak .med dan titik J (deskriptif, di luar pra-daftar)\n")
    g = {"dipakai (500, 12).T": [], "alternatif (12, 500)": []}
    for rec in ut.ecg_med_record:
        mentah = np.fromfile(AKAR / "med/med_data" / rec, dtype="<i2").astype(float)
        g["dipakai (500, 12).T"].append(galat_einthoven(mentah.reshape(500, 12).T))
        g["alternatif (12, 500)"].append(galat_einthoven(mentah.reshape(12, 500)))
    print(f"n EKG = {len(ut)}. Galat relatif = rata-rata |selisih| / rata-rata |amplitudo| sadapan ekstremitas.\n")
    print("| Susunan | III − (II − I), median | p95 | aVR + (I + II)/2, median | p95 |")
    print("| --- | --- | --- | --- | --- |")
    for k, v in g.items():
        a = np.array(v)
        print(f"| {k} | {np.median(a[:, 0]):.4f} | {np.quantile(a[:, 0], .95):.4f} | "
              f"{np.median(a[:, 1]):.4f} | {np.quantile(a[:, 1], .95):.4f} |")

    # 3. Nilai ST60 yang tidak fisiologis (artefak satu sadapan), EKG status ok, tanpa label.
    cu = ci.set_index("ecg_med_record").loc[[r for r in ut.ecg_med_record if r in ok]]
    mx = cu.filter(like="st60_").abs().max(axis=1)
    print(f"\n|ST60| maksimum per EKG (status ok, n = {len(cu)}):\n")
    print("| Ambang | n EKG dengan sadapan mana pun di atas ambang | % |")
    print("| --- | --- | --- |")
    for thr in [0.5, 1, 2, 5]:
        n = int((mx > thr).sum())
        print(f"| > {thr} mV | {n} | {100 * n / len(cu):.2f} |")

    rng = np.random.default_rng(20261115)
    calon = [r for r in ut.ecg_med_record if r in ok]
    pilih = sorted(rng.choice(calon, 30, replace=False))
    print(f"\nSampel titik J: 30 dari {len(calon)} EKG status ok (benih 20261115): " + ", ".join(pilih) + ".\n")
    warna = plt.cm.tab20(np.linspace(0, 1, 12))
    for hal in range(2):
        fig, ax = plt.subplots(5, 3, figsize=(15, 17))
        for k, rec in enumerate(pilih[hal * 15:(hal + 1) * 15]):
            x = baca_med(AKAR / "med/med_data" / rec)
            _, awal, j = deteksi(x)
            pr = x[:, awal - 15:awal - 5].mean(axis=1, keepdims=True)
            a = ax.flat[k]
            t = np.arange(x.shape[1]) * 1000 / FS
            for s in range(12):
                a.plot(t, (x[s] - pr[s]) / 1000, color=warna[s], lw=0.8, label=SADAPAN[s])
            a.axvspan((awal - 15) * 2, (awal - 5) * 2, color="0.85")
            for idx, gaya, nama in [(awal, "--", "awal QRS"), (j, "-", "J"), (j + 30, ":", "J+60")]:
                a.axvline(idx * 1000 / FS, color="k", ls=gaya, lw=1)
            a.axhline(0, color="0.5", lw=0.5)
            a.set_xlim((awal - 60) * 2, (j + 120) * 2)
            a.set_title(f"{hal * 15 + k + 1}. {rec}  QRS {(j - awal) * 2} ms", fontsize=10)
            a.set_ylabel("mV")
        ax.flat[0].legend(ncol=4, fontsize=6)
        fig.suptitle("12 sadapan ditumpuk; abu = jendela PR; -- awal QRS, — titik J, ··· J+60 ms", fontsize=12)
        fig.tight_layout()
        fig.savefig(keluar / f"titik_j_{hal + 1}.png", dpi=90)
        plt.close(fig)
    print(f"Gambar: titik_j_1.png, titik_j_2.png di {keluar} (tidak masuk repo).")


if __name__ == "__main__":
    main(sys.argv[1])
