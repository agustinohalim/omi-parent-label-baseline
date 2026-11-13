# Hasil OMI 10 — fase F: nol permutasi, waktu ke angiografi, CTO lawan OMI, ragam benih CNN (13 November 2026)

> Pra-daftar `Prareg_OMI_F.md` (terkunci e9c7062); skrip `omi_fase_f.py` (0e0bed2), dikomit sebelum dijalankan. Run
> 13 Nov: F1 100 permutasi *probe* (CPU, 20,7 menit), CNN 5 benih × 2 label (`venv-gpu`, 33,9 menit), F2–F3
> (26,8 menit), F4 (2,5 menit). Log `$OMI_DATA/fase_f_perm.log`, `fase_f_cnn.log`, `fase_f_F1.log`,
> `fase_f_F2F3_B2000.log`, `fase_f_F4_B2000.log` (keluaran analisis disalin di bawah). Tidak ada unduhan. Semua butir
> eksploratif. Penyimpangan: tidak ada.

## Bacaan menurut aturan yang dikunci

- **F1 — label oklusi membawa informasi di dalam infark di atas struktur pelatihan.** *Probe* berlabel asli (C =
  0,001, lipatan 20261107): AUROC (c) **0,643**; 100 *probe* berlabel OMI teracak di antara EKG ber-AMI: rerata
  **0,596** (SB 0,006; persentil ke-95 0,605; maksimum 0,608). Label asli di atas persentil ke-95 (0 dari 100
  permutasi ≥ label asli, p = 0,010). Selisih terhadap rerata nol **+0,047**. Rerata nol 0,596 hampir sama dengan
  *probe*-AMI (0,601): struktur pelatihan sendiri tidak menghasilkan keunggulan.
- **F2 — selisih tidak terbatas pada EKG dekat angiografi, tetapi Q4 tidak menunjukkannya untuk *probe*.** Selisih (c)
  *probe*: Q1 +0,044 [0,030; 0,057], Q2 +0,054, Q3 +0,036 [0,014; 0,059], Q4 +0,021 [−0,006; 0,047]. CNN: Q1 +0,041,
  Q2 +0,051, Q3 +0,012 [−0,021; 0,044], Q4 +0,049 [0,013; 0,086]. Aturan: batas bawah Q1 > 0 ya, Q4 tidak → naskah
  menyebut Q4 (*probe*) dan Q3 (CNN) tidak menunjukkannya. OMI lawan semua per kuartil: *probe* −0,008 sampai +0,004.
- **F3 — skor lebih tinggi pada oklusi akut daripada oklusi kronis.** OMI lawan CTO langsung: *probe*-OMI **0,803
  [0,783; 0,821]** (≥ 0,70: aturan terpenuhi); *probe*-AMI 0,816. Pada rujukan sama (14.030 tanpa AMI non-CTO): OMI
  0,920, CTO 0,686, selisih 0,234 [0,214; 0,254]; *probe*-AMI 0,925 / 0,695. CTO menurut Prior_PCI: ya 0,674 (129),
  tidak 0,687 (817). Kalimat aturan E2 ("evidence that the score separates acute abnormality from chronic occlusion")
  tidak dipakai lagi; diganti hasil (i).
- **F4 — ragam pelatihan tidak mengubah bacaan.** Per penetapan lipatan, selisih (c): *probe* 0,042 / 0,039 / 0,045,
  CNN 0,037 / 0,039 / 0,042. OMI lawan semua: *probe* −0,002 / −0,002 / −0,001; CNN −0,015 / +0,015 / +0,010. CNN lima
  benih inisialisasi (lipatan 20261107): (c) selisih per pasangan +0,055, +0,037, +0,022, +0,048, +0,038 (5 dari 5 >
  0), prediksi rerata **+0,048 [0,034; 0,061]** → aturan terpenuhi. OMI lawan semua: −0,000 rerata (rentang −0,015
  sampai +0,025); prediksi rerata −0,007 [−0,013; −0,000]. AUROC CNN per benih untuk OMI berkisar 0,857–0,883.

## Aturan tulis (Prareg F) yang sekarang berlaku

- "Equal overall": CI selisih OMI lawan semua *probe* [−0,005; 0,002] dan CNN tiga penetapan [−0,003; 0,010] di
  dalam ±0,03 → boleh. CNN lima benih [−0,013; −0,000] juga di dalam ±0,03.
- Klaim di dalam infark: angka dan nol permutasi, tanpa "small" / "a little".

## Batasan

- F1 hanya untuk *probe* (C tetap, satu penetapan lipatan); CNN tidak dipermutasi.
- F3: CTO tidak memuat usia oklusi atau infark lama; *probe*-AMI memisahkan OMI dari CTO sama baiknya.
- F2: kuartil per EKG; Q4 berisi 140 OMI.

---

Salinan `fase_f_F1.log`:

### Fase F OMI — keluaran omi_fase_f.py (B = 2000, butir F1)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## F1. Nol permutasi label oklusi di dalam infark (probe, C = 0,001, lipatan 20261107)

Permutasi selesai: 100. AUROC (c) label asli 0.6431; OMI lawan semua 0.8878.
Sebaran nol AUROC (c): rerata 0.5959, SB 0.0056, persentil 2,5/50/95/97,5 0.5835 / 0.5964 / 0.6048 / 0.6056, maksimum 0.6080.
Label asli − rerata nol: 0.0472; permutasi ≥ label asli: 0 dari 100 (p = 0.010).
Sebaran nol AUROC OMI lawan semua: rerata 0.8784, rentang 0.8719–0.8822.
Aturan: label asli > persentil ke-95 nol: **ya**.

Waktu jalan: 0.0 menit.

---

Salinan `fase_f_F2F3_B2000.log`:

### Fase F OMI — keluaran omi_fase_f.py (B = 2000, butir F2,F3)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## F2. Selisih label per kuartil jarak EKG ke angiografi

| Kuartil | Sasaran | n pos / n | probe-OMI − probe-AMI | CNN-OMI − CNN-AMI |
| --- | --- | --- | --- | --- |
| Q1 | (c) OMI lawan AMI tanpa OMI | 533 / 1147 | 0.044 [0.030, 0.057] | 0.041 [0.021, 0.060] |
| Q1 | OMI lawan semua | 533 / 4408 | 0.004 [-0.002, 0.010] | 0.001 [-0.010, 0.012] |
| Q2 | (c) OMI lawan AMI tanpa OMI | 275 / 701 | 0.054 [0.036, 0.072] | 0.051 [0.026, 0.075] |
| Q2 | OMI lawan semua | 275 / 4403 | 0.003 [-0.005, 0.011] | 0.017 [0.004, 0.030] |
| Q3 | (c) OMI lawan AMI tanpa OMI | 185 / 439 | 0.036 [0.014, 0.059] | 0.012 [-0.021, 0.044] |
| Q3 | OMI lawan semua | 185 / 4405 | -0.008 [-0.016, 0.000] | -0.004 [-0.022, 0.014] |
| Q4 | (c) OMI lawan AMI tanpa OMI | 140 / 359 | 0.021 [-0.006, 0.047] | 0.049 [0.013, 0.086] |
| Q4 | OMI lawan semua | 140 / 4406 | -0.006 [-0.015, 0.004] | 0.007 [-0.010, 0.025] |

## F3. Oklusi kronis lawan oklusi akut

(i) OMI lawan CTO langsung (1133 / 946): probe-OMI 0.803 [0.783, 0.821]; probe-AMI 0.816 [0.798, 0.834].

(ii) Rujukan sama: tanpa AMI non-CTO (14030).

| Model | OMI lawan rujukan | CTO lawan rujukan | selisih |
| --- | --- | --- | --- |
| probe-OMI | 0.920 [0.911, 0.928] | 0.686 [0.667, 0.705] | 0.234 [0.214, 0.254] |
| probe-AMI | 0.925 [0.918, 0.933] | 0.695 [0.677, 0.712] | 0.231 [0.212, 0.250] |

(iii) CTO lawan rujukan, menurut Prior_PCI:

| Prior_PCI | n CTO / n rujukan | probe-OMI | probe-AMI |
| --- | --- | --- | --- |
| ya | 129 / 14030 | 0.674 [0.622, 0.723] | 0.681 [0.631, 0.730] |
| tidak | 817 / 14030 | 0.687 [0.668, 0.708] | 0.697 [0.678, 0.716] |

Waktu jalan: 26.8 menit.

---

Salinan `fase_f_F4_B2000.log`:

### Fase F OMI — keluaran omi_fase_f.py (B = 2000, butir F4)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## F4. Ragam pelatihan

(a) Selisih AUROC label oklusi − label infark per penetapan lipatan (prediksi tersimpan):

| Sasaran | Model | 20261107 | 20261108 | 20261109 |
| --- | --- | --- | --- | --- |
| OMI lawan semua | probe | -0.002 | -0.002 | -0.001 |
| OMI lawan semua | CNN | -0.015 | 0.015 | 0.010 |
| (c) OMI lawan AMI tanpa OMI | probe | 0.042 | 0.039 | 0.045 |
| (c) OMI lawan AMI tanpa OMI | CNN | 0.037 | 0.039 | 0.042 |
| AMI lawan tanpa AMI | probe | -0.017 | -0.016 | -0.018 |
| AMI lawan tanpa AMI | CNN | -0.028 | 0.002 | -0.004 |

(b) CNN, lima benih inisialisasi, penetapan lipatan 20261107:

- OMI lawan semua: AUROC label OMI per benih 0.866, 0.862, 0.871, 0.863, 0.857; label AMI 0.862, 0.877, 0.883, 0.838, 0.862; selisih per pasangan +0.004, -0.015, -0.012, +0.025, -0.005 (rerata -0.000, rentang -0.015 sampai +0.025, > 0: 2 dari 5); prediksi rerata lima benih: -0.007 [-0.013, -0.000].
- (c) OMI lawan AMI tanpa OMI: AUROC label OMI per benih 0.640, 0.631, 0.627, 0.634, 0.618; label AMI 0.584, 0.594, 0.605, 0.586, 0.580; selisih per pasangan +0.055, +0.037, +0.022, +0.048, +0.038 (rerata +0.040, rentang +0.022 sampai +0.055, > 0: 5 dari 5); prediksi rerata lima benih: 0.048 [0.034, 0.061].
- AMI lawan tanpa AMI: AUROC label OMI per benih 0.840, 0.838, 0.849, 0.836, 0.835; label AMI 0.857, 0.871, 0.877, 0.828, 0.858; selisih per pasangan -0.018, -0.033, -0.027, +0.008, -0.023 (rerata -0.019, rentang -0.033 sampai +0.008, > 0: 1 dari 5); prediksi rerata lima benih: -0.026 [-0.031, -0.020].

Waktu jalan: 2.5 menit.

