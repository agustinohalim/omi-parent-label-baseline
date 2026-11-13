# Hasil OMI 11 — fase G: komposisi STEMI dan uji "differ only" (13 November 2026)

> Pra-daftar `Prareg_OMI_G.md` (terkunci 901b8fe); skrip `omi_fase_g.py` (39ee850), dikomit sebelum dijalankan. Run
> 13 Nov: G1(ii) 100 permutasi berlapis *probe* (CPU, 19,2 menit), G2 (15,4 menit), G1 (2,3 menit), G3 (31,6 menit,
> penyimpangan P1 049bbcc). Log
> `$OMI_DATA/fase_g_perm.log`, `fase_g_G1_B2000.log`, `fase_g_G2_B2000.log` (keluaran analisis disalin di
> bawah), `fase_g_G3_B2000.log`. Tidak ada unduhan. Semua butir eksploratif. Penyimpangan: P1 (G3 ditambah).

## Bacaan menurut aturan yang dikunci

- **G1(ii) — label oklusi membawa informasi di luar tipe infark.** *Probe* berlabel asli: AUROC (c) **0,643** (F1).
  100 *probe* berlabel OMI teracak **di dalam** lapis STEMI / NSTEMI / lain (jumlah OMI per lapis tetap): rerata
  **0,601** (SB 0,005; persentil ke-95 0,609; maksimum 0,612). Label asli di atas persentil ke-95 (0 dari 100 ≥ label
  asli, p = 0,010) → **aturan terpenuhi**: klaim keunggulan di dalam infark bertahan. Selisih terhadap rerata nol
  berlapis **+0,043**, hampir sama dengan selisih terhadap nol tak berlapis F1 (+0,047; rerata F1 0,596): komposisi
  STEMI menjelaskan ±0,004 dari keunggulan. Nol berlapis di dalam STEMI rerata 0,528, di dalam NSTEMI 0,613.
- **G1(i) — keunggulan ada di dalam STEMI dan di dalam NSTEMI.** Selisih label oklusi − label infark: STEMI (715 / 708)
  *probe* **+0,052 [0,036; 0,068]**, CNN +0,041 [0,023; 0,061]; NSTEMI (417 / 804) *probe* **+0,043 [0,027; 0,058]**,
  CNN +0,044 [0,023; 0,066]. Batas bawah *probe* > 0 di kedua lapis → naskah boleh menyatakan keunggulan di dalam STEMI
  dan di dalam NSTEMI. AUROC absolut di dalam lapis rendah: *probe*-OMI 0,584 di STEMI, 0,655 di NSTEMI.
- **G2 — "only" tidak dipakai.** Selisih berpasangan (label oklusi − label infark): OMI lawan tanpa infark *probe*
  **−0,006 [−0,010; −0,003]**, CNN −0,000 [−0,006; 0,006]; infark lawan tanpa infark *probe* **−0,017 [−0,020;
  −0,014]**, CNN −0,010 [−0,015; −0,005]. Untuk *probe* kedua selang tidak memuat 0; untuk CNN selang infark lawan
  tanpa infark tidak memuat 0 → aturan: judul dan simpulan tidak memakai "only" (dan tidak "equal" untuk perbandingan
  dengan tanpa infark); setiap selisih dilaporkan dengan CI. Semua selisih di luar infark kecil (|selisih| ≤ 0,017) dan
  berlawanan arah dengan selisih di dalam infark (+0,040 sampai +0,042).

- **G3(i) (penyimpangan P1) — *probe* berlabel infark memisahkan infark tanpa oklusi dari tanpa infark lebih baik
  di setiap baris.** Selisih *probe* (label oklusi − label infark): infark tanpa oklusi −0,025 [−0,029; −0,021], STEMI
  −0,014, NSTEMI **−0,034 [−0,041; −0,028]**, dengan PCI −0,023, tanpa PCI −0,027 [−0,034; −0,021], NSTEMI tanpa PCI
  **−0,034 [−0,044; −0,025]**; OMI lawan tanpa infark −0,006 [−0,010; −0,002]. Aturan: "did the same" hanya untuk baris
  dengan CI di dalam ±0,03 (infark tanpa oklusi keseluruhan, STEMI, dengan PCI, OMI lawan tanpa infark); NSTEMI, tanpa
  PCI, dan NSTEMI tanpa PCI dilaporkan dengan selisih (*probe* berlabel infark lebih tinggi).
- **G3(ii) — *probe* lawan CNN.** OMI lawan semua +0,021 [0,014; 0,029]; (c) **+0,012 [−0,004; 0,026]**; di dalam
  STEMI −0,007 [−0,031; 0,018]; di dalam NSTEMI +0,030 [0,004; 0,054]. Aturan: CI (c) memuat 0 → anak kalimat "not
  among patients with infarction" boleh, dengan NSTEMI disebut.

## Aturan tulis yang sekarang berlaku

- Judul dan simpulan tidak memakai "only" atau "differ only". Rumusan yang didukung: model berlabel oklusi lebih baik
  memisahkan OMI dari infark tanpa oklusi (+0,04, juga di dalam STEMI dan di dalam NSTEMI, di atas nol berlapis tipe
  infark), dan sedikit lebih buruk memisahkan EKG tanpa infark (*probe* −0,006 untuk OMI, −0,017 untuk infark).
- Kata "small" tetap dilarang (Prareg F); besar selisih ditulis dengan angka dan CI.
- Kalimat "the +0.04 could reflect STEMI composition" diganti hasil G1: komposisi menjelaskan ±0,004.

## Batasan

Nol berlapis hanya untuk *probe* (C tetap 0,001), seperti F1; CNN tidak dilatih ulang pada label teracak. AUROC di
dalam STEMI 0,58 berarti model tetap lemah memisahkan oklusi di antara STEMI walau label oklusi lebih baik daripada
label infark. Batas bias inkorporasi dari tinjauan label tetap tidak dapat diukur (data tidak menyebut berapa label
berubah).

## G1. Keluaran
(i) Selisih label oklusi − label infark di dalam tipe infark (prediksi tersimpan, tiga penetapan):

| Lapis | n OMI / n tanpa OMI | probe-OMI | probe-AMI | selisih probe | CNN-OMI | CNN-AMI | selisih CNN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STEMI | 715 / 708 | 0.584 | 0.532 | 0.052 [0.036, 0.068] | 0.591 | 0.550 | 0.041 [0.023, 0.061] |
| NSTEMI | 417 / 804 | 0.655 | 0.612 | 0.043 [0.027, 0.058] | 0.625 | 0.581 | 0.044 [0.023, 0.066] |

(ii) Nol permutasi berlapis tipe infark (probe, C = 0,001, lipatan 20261107):

Permutasi selesai: 100. AUROC (c) label asli 0.6431 (F1).
Nol berlapis AUROC (c): rerata 0.6006, SB 0.0052, persentil 2,5/50/95/97,5 0.5917 / 0.6004 / 0.6092 / 0.6099, maksimum 0.6121.
Label asli − rerata nol berlapis: 0.0425; permutasi ≥ label asli: 0 dari 100 (p = 0.010).
Nol berlapis di dalam STEMI: rerata 0.5277 (rentang 0.5084–0.5440); di dalam NSTEMI: rerata 0.6128 (rentang 0.6007–0.6337).
Nol tak berlapis (F1) sebagai pembanding: rerata 0.5959.
Aturan: label asli > persentil ke-95 nol berlapis: **ya**.

## G2. Keluaran

| Sasaran | n pos / n | selisih probe | selisih CNN |
| --- | --- | --- | --- |
| OMI lawan semua | 1133 / 17622 | -0.002 [-0.005, 0.002] | 0.003 [-0.003, 0.010] |
| OMI lawan tanpa infark | 1133 / 16109 | -0.006 [-0.010, -0.003] | -0.000 [-0.006, 0.006] |
| (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.042 [0.033, 0.052] | 0.040 [0.027, 0.052] |
| AMI lawan tanpa AMI | 2646 / 17622 | -0.017 [-0.020, -0.014] | -0.010 [-0.015, -0.005] |

Aturan "only" (probe): OMI lawan tanpa infark di dalam ±0,03 dan memuat 0: tidak; infark lawan tanpa infark: tidak → **only tidak dipakai**.

Aturan "only" (CNN): OMI lawan tanpa infark di dalam ±0,03 dan memuat 0: ya; infark lawan tanpa infark: tidak → **only tidak dipakai**.

Waktu jalan: 15.4 menit.

## G3. Keluaran

(i) Skor OMI tiap model untuk pasangan kelompok (pos lawan neg):

| Pasangan | n pos / n neg | probe-OMI | probe-AMI | selisih probe | CNN-OMI | CNN-AMI | selisih CNN | ±0,03 probe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OMI lawan tanpa infark | 1133 / 14976 | 0.912 | 0.919 | -0.006 [-0.010, -0.002] | 0.891 | 0.891 | -0.000 [-0.007, 0.006] | ya |
| Infark tanpa oklusi lawan tanpa infark | 1513 / 14976 | 0.825 | 0.850 | -0.025 [-0.029, -0.021] | 0.808 | 0.825 | -0.017 [-0.025, -0.010] | ya |
|   STEMI | 708 / 14976 | 0.911 | 0.925 | -0.014 [-0.019, -0.010] | 0.894 | 0.902 | -0.007 [-0.016, 0.001] | ya |
|   NSTEMI | 804 / 14976 | 0.749 | 0.783 | -0.034 [-0.041, -0.028] | 0.731 | 0.758 | -0.026 [-0.038, -0.016] | tidak |
|   dengan PCI | 765 / 14976 | 0.844 | 0.867 | -0.023 [-0.028, -0.018] | 0.830 | 0.846 | -0.017 [-0.027, -0.007] | ya |
|   tanpa PCI | 748 / 14976 | 0.805 | 0.832 | -0.027 [-0.034, -0.021] | 0.786 | 0.804 | -0.018 [-0.029, -0.008] | tidak |
|   NSTEMI tanpa PCI | 412 / 14976 | 0.730 | 0.765 | -0.034 [-0.044, -0.025] | 0.710 | 0.735 | -0.025 [-0.041, -0.008] | tidak |

(ii) Selisih probe-OMI − CNN-OMI:

| Sasaran | n pos / n | probe-OMI | CNN-OMI | selisih |
| --- | --- | --- | --- | --- |
| OMI lawan semua | 1133 / 17622 | 0.888 | 0.867 | 0.021 [0.014, 0.029] |
| (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.643 | 0.631 | 0.012 [-0.004, 0.026] |
| di dalam STEMI | 715 / 1423 | 0.584 | 0.591 | -0.007 [-0.031, 0.018] |
| di dalam NSTEMI | 417 / 1221 | 0.655 | 0.625 | 0.030 [0.004, 0.054] |

Aturan: CI selisih (c) memuat 0: ya → anak kalimat boleh.
