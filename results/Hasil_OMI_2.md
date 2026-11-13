# Hasil OMI 2 — M2, CNN 1D pada EKG mentah 10 s, split latih (11 November 2026)

> Satu-satunya sumber angka M2. Skrip `omi_m2.py` (komit 350bfb7, isi nol rekaman pendek 1 komit sesudahnya),
> dikomit sebelum dijalankan; resep = Penyimpangan P3 (pola Arrest). GPU RTX 5060 (venv-gpu, torch 2.14 cu130).
> Data: Chongqing ACS `train.csv` + `row_data/*.dat`; `test.csv` belum disentuh. Dua rekaman latih hanya 7 s
> (14262.dat, 03228.dat; keduanya bukan OMI, bukan Paced), diisi nol di ujung. Uji jalan (1 benih, 2 epoch) dibuang.
> Tabel di bawah disalin apa adanya dari log (scratchpad sesi, `m2_full.log`). Prediksi out-of-fold:
> `$OMI_DATA/oof_m2_{utama,nstemi,teritori,kepekaan}.npz`.



### Utama — OMI lawan bukan-OMI, tanpa Paced

n EKG = 17622, pasien = 16703, OMI = 1133 (6.43 %). Waktu latih: 21.9 menit.

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M2 | 0.867 [0.857, 0.877] | 0.354 [0.330, 0.382] | 0.120 [0.117, 0.124] | 0.615 [0.590, 0.642] | 0.570 [0.538, 0.606] | -2.557 [-2.639, -2.475] |

Replikat bootstrap dengan slope tak terhitung (P2): M2 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M2 | 0.0563 [0.0526, 0.0600] | 0.0506 [0.0469, 0.0543] | 0.0378 [0.0341, 0.0415] | 0.0202 [0.0164, 0.0239] |
| Rawat semua | 0.0548 | 0.0452 | 0.0150 | -0.0397 |

Per benih (AUROC): M2 0.867, 0.868, 0.866.

### Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced

n EKG = 1221, pasien = 1200, OMI = 417 (34.15 %). Waktu latih: 2.3 menit.

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M2 | 0.570 [0.544, 0.596] | 0.410 [0.374, 0.452] | 0.289 [0.274, 0.302] | 0.173 [0.137, 0.211] | 0.113 [0.069, 0.160] | -0.250 [-0.442, -0.049] |

Replikat bootstrap dengan slope tak terhitung (P2): M2 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M2 | 0.3232 [0.2971, 0.3490] | 0.3066 [0.2805, 0.3317] | 0.2665 [0.2407, 0.2914] | 0.2169 [0.1917, 0.2414] |
| Rawat semua | 0.3349 | 0.3281 | 0.3069 | 0.2684 |

Per benih (AUROC): M2 0.582, 0.554, 0.574.

### Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)

n EKG = 901 (LAD 344, LCX 207, RCA 350); di antaranya NSTEMI-OMI 299.

**semua OMI satu teritori** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M2 | 0.865 [0.843, 0.886] | 0.702 [0.668, 0.736] | 0.781 [0.752, 0.806] | 0.783 [0.762, 0.804] |

**NSTEMI-OMI (eksploratif)** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M2 | 0.736 [0.684, 0.787] | 0.655 [0.605, 0.702] | 0.653 [0.600, 0.705] | 0.681 [0.644, 0.720] |


### Kepekaan — utama dengan Paced

n EKG = 17960, pasien = 17018, OMI = 1151 (6.41 %). Waktu latih: 24.0 menit.

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M2 | 0.859 [0.849, 0.869] | 0.336 [0.311, 0.362] | 0.151 [0.147, 0.154] | 0.597 [0.572, 0.622] | 0.574 [0.539, 0.611] | -2.878 [-2.954, -2.806] |

Replikat bootstrap dengan slope tak terhitung (P2): M2 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M2 | 0.0556 [0.0521, 0.0592] | 0.0500 [0.0464, 0.0536] | 0.0354 [0.0319, 0.0390] | 0.0140 [0.0104, 0.0176] |
| Rawat semua | 0.0546 | 0.0450 | 0.0148 | -0.0399 |

Per benih (AUROC): M2 0.839, 0.874, 0.864.

Waktu jalan seluruhnya: 51,9 menit.

## Catatan baca

- **M2 jauh di atas M1 pada analisis utama**: AUROC 0,867 lawan 0,615 (`Hasil_OMI_1.md`), Se@Sp90 0,615 lawan 0,235,
  dan net benefit di atas rawat semua pada ambang 5 % dan 10 %. Selisih berpasangan M2 − M1 belum dihitung; masuk
  skrip pembanding bersama M3 (perbandingan utama pra-daftar).
- **Kalibrasi buruk menurut rancangan**: bobot kelas seimbang (P3) menggeser probabilitas ke atas — intercept −2,557,
  slope 0,570, Brier 0,120 (M0/M1 0,060). Tidak dikalibrasi ulang; bila dibutuhkan, rekalibrasi harus ditetapkan
  lewat Penyimpangan sebelum dipakai.
- **NSTEMI-OMI tetap sulit**: 0,570 [0,544, 0,596], hanya sedikit di atas M1 0,541; net benefit di bawah rawat semua
  pada semua ambang (prevalensi 34 %).
- **Teritori**: makro 0,783 (LAD 0,865); pada NSTEMI-OMI 0,681, jauh di atas M1 0,550.
- **Stabilitas**: kepekaan dengan Paced memberi AUROC per benih 0,839/0,874/0,864 (utama 0,866–0,868).
- **Arah waktu EKG (diselesaikan 11 Nov dari PDF makalah data yang diberikan pengguna)**: hanya EKG *sebelum*
  angiografi yang disimpan, dalam 7 hari sebelum DSA; `Time_Interval` dalam menit (Du dkk., Sci Data 13:1009, bagian
  *Data exclusion*). Jadi M2 tidak melihat EKG pasca-PCI. Yang masih terbuka ⬜: EKG yang direkam berhari-hari sebelum
  angiografi bisa mendahului oklusinya sendiri, dan EKG jalur darurat (STEMI, selang pendek) mungkin berbeda dari EKG
  rawat jalan dalam hal yang bukan tanda iskemia; analisis per strata Time_Interval perlu ditetapkan lewat
  Penyimpangan bertanggal sebelum dijalankan.
- **Pembanding penulis data** (uji tersembunyi, biner; `Kebaruan_OMI_2026-11-06.md`): CNN denyut median Se 0,697 pada
  Sp 0,873. Bukan pembanding langsung (split dan ambang berbeda), tetapi besarannya sejalan dengan M2.
