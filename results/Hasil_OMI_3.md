# Hasil OMI 3 — M3a (ECGFounder beku + probe L2) dan perbandingan utama, split latih (11 November 2026)

> Satu-satunya sumber angka M3a dan perbandingan utama. Skrip `omi_m3_ecgfounder.py` (komit 3d04aed; perbaikan
> pemuatan bobot b691329 dan dua komit sesudahnya, tanpa mengubah pra-proses atau probe) dan `omi_banding.py`
> (komit 7eff480), dikomit sebelum hasil keluar; rancangan = Penyimpangan P3. Bobot `12_lead_ECGFounder.pth`
> (SHA-256 ee199f37…aca7997) dimuat `weights_only` dengan dua global numpy diizinkan; 0 kunci hilang, 0 kunci lebih.
> Kode Net1D dijalankan atas izin pengguna 11 Nov. Embedding 17.960 × 1.024 di GPU (11,4 menit), probe di CPU
> (47,7 menit). `test.csv` belum disentuh. ECG-FM belum dijalankan ⬜ (keputusan pengguna soal `fairseq-signals`).
> Tabel disalin apa adanya dari log (scratchpad sesi, `m3a_probe.log`, `banding.log`).

## 1. M3a


### Utama — OMI lawan bukan-OMI, tanpa Paced

n EKG = 17622, pasien = 16703, OMI = 1133 (6.43 %). C terpilih: [0.001].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M3a | 0.888 [0.879, 0.897] | 0.365 [0.339, 0.394] | 0.048 [0.046, 0.051] | 0.661 [0.629, 0.692] | 1.061 [1.012, 1.114] | 0.007 [-0.062, 0.075] |

Replikat bootstrap dengan slope tak terhitung (P2): M3a 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M3a | 0.0569 [0.0532, 0.0607] | 0.0525 [0.0489, 0.0562] | 0.0442 [0.0406, 0.0477] | 0.0337 [0.0306, 0.0370] |
| Rawat semua | 0.0548 | 0.0452 | 0.0150 | -0.0397 |

Per benih (AUROC): M3a 0.888, 0.887, 0.889.

### Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced

n EKG = 1221, pasien = 1200, OMI = 417 (34.15 %). C terpilih: [0.001].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M3a | 0.653 [0.621, 0.684] | 0.480 [0.437, 0.532] | 0.211 [0.201, 0.221] | 0.247 [0.188, 0.289] | 0.902 [0.697, 1.127] | 0.014 [-0.107, 0.137] |

Replikat bootstrap dengan slope tak terhitung (P2): M3a 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M3a | 0.3349 [0.3082, 0.3617] | 0.3281 [0.3011, 0.3551] | 0.3069 [0.2791, 0.3348] | 0.2671 [0.2379, 0.2965] |
| Rawat semua | 0.3349 | 0.3281 | 0.3069 | 0.2684 |

Per benih (AUROC): M3a 0.651, 0.658, 0.650.

### Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)

n EKG = 901 (LAD 344, LCX 207, RCA 350); di antaranya NSTEMI-OMI 299.

**semua OMI satu teritori** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M3a | 0.891 [0.867, 0.912] | 0.755 [0.717, 0.793] | 0.837 [0.810, 0.863] | 0.827 [0.805, 0.849] |

**NSTEMI-OMI (eksploratif)** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M3a | 0.780 [0.722, 0.834] | 0.689 [0.627, 0.749] | 0.703 [0.641, 0.760] | 0.724 [0.680, 0.767] |


### Kepekaan — utama dengan Paced

n EKG = 17960, pasien = 17018, OMI = 1151 (6.41 %). C terpilih: [0.001].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M3a | 0.888 [0.879, 0.897] | 0.363 [0.337, 0.393] | 0.048 [0.046, 0.051] | 0.661 [0.631, 0.689] | 1.065 [1.018, 1.115] | 0.005 [-0.063, 0.071] |

Replikat bootstrap dengan slope tak terhitung (P2): M3a 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M3a | 0.0568 [0.0532, 0.0604] | 0.0523 [0.0488, 0.0560] | 0.0437 [0.0403, 0.0473] | 0.0336 [0.0305, 0.0367] |
| Rawat semua | 0.0546 | 0.0450 | 0.0148 | -0.0399 |

Per benih (AUROC): M3a 0.887, 0.888, 0.889.

Waktu jalan: 47.7 menit.

## 2. Perbandingan utama (Prareg_OMI.md bagian 4)


n EKG = 17622, OMI = 1133. AUROC rata-rata benih: M1 0.615; M2 0.867; M3a 0.888. M3 terbaik: M3a.

| Perbandingan | Benih | Selisih AUROC | SE DeLong | p DeLong |
| --- | --- | --- | --- | --- |
| M3a − M2 | 20261107 | 0.021 | 0.0046 | 7.7e-06 |
| M3a − M2 | 20261108 | 0.019 | 0.0046 | 2.7e-05 |
| M3a − M2 | 20261109 | 0.023 | 0.0045 | 3.1e-07 |
| M3a − M1 | 20261107 | 0.280 | 0.0105 | 2.5e-156 |
| M3a − M1 | 20261108 | 0.264 | 0.0103 | 1.5e-145 |
| M3a − M1 | 20261109 | 0.273 | 0.0104 | 7.5e-152 |
| M2 − M1 | 20261107 | 0.259 | 0.0101 | 4.8e-145 |
| M2 − M1 | 20261108 | 0.245 | 0.0106 | 6e-117 |
| M2 − M1 | 20261109 | 0.251 | 0.0110 | 9e-115 |

| Perbandingan | Selisih AUROC (rata-rata benih) | CI 95 % bootstrap bergugus pasien |
| --- | --- | --- |
| M3a − M2 | 0.021 | [0.013, 0.029] |
| M3a − M1 | 0.272 | [0.253, 0.291] |
| M2 − M1 | 0.251 | [0.232, 0.271] |

Replikat bootstrap terpakai: 2000 dari 2000.

## 3. Catatan baca

- **Perbandingan utama terjawab**: M3a (ECGFounder beku) di atas M2 (CNN dilatih penuh) sebesar 0,021 AUROC
  [0,013, 0,029] (bootstrap bergugus pasien; DeLong p < 10⁻⁴ di tiap benih), dan di atas M1 sebesar 0,272. M3a adalah
  satu-satunya M3 yang dijalankan, jadi tidak ada optimisme pemilihan antar-M3. DeLong menganggap EKG saling bebas;
  CI bootstrap bergugus pasien adalah ukuran yang dipakai di naskah.
- **Kalibrasi M3a baik** tanpa rekalibrasi (slope 1,061, intercept 0,007, Brier 0,048) — probe dilatih tanpa bobot
  kelas, berbeda dengan M2.
- **NSTEMI-OMI**: 0,653 [0,621, 0,684], di atas M2 0,570 dan M1 0,541, tetapi net benefit tetap ≈ rawat semua.
- **Teritori**: makro 0,827 (LAD 0,891, LCX 0,755, RCA 0,837); NSTEMI-OMI 0,724.
- **C di batas kisi**: C terpilih 0,001 di semua lipatan dan analisis — ujung bawah kisi terkunci. Probe mungkin
  masih kurang diregularisasi; AUROC M3a bisa sedikit di bawah potensinya. Memperluas kisi = Penyimpangan bertanggal,
  dilaporkan di luar pra-daftar.
- **Kepekaan dengan Paced** tidak mengubah apa pun (0,888).
- **Masih ⬜ sebelum naskah**: analisis per strata Time_Interval (Penyimpangan dulu); server penilai sekali di akhir
  (ambang Sp 90 % dari out-of-fold); ECG-FM.
