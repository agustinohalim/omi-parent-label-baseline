# Hasil OMI 6 — fase B, uji konstruk (12 November 2026)

> Pra-daftar `Prareg_OMI_B.md` (terkunci b56d323); skrip `omi_konstruk.py` (komit 51e8004), B = 2.000. Run penuh
> 12 Nov dihentikan Claude Code karena memori sistem menipis **sesudah K1 selesai dan selama K2**; K1 di bawah utuh
> dari log `$OMI_DATA/konstruk_B2000.log`. K2–K5 dijalankan ulang 13 Nov atas izin pengguna dengan
> `--butir K2,K3,K4,K5` (benih bootstrap per butir, jadi hasil sama dengan run tunggal; satu percobaan 12 Nov juga
> dihentikan karena memori sebelum mencetak angka), log `$OMI_DATA/konstruk_B2000_K2-5.log`.
> Semua butir eksploratif terhadap pra-daftar 7 Nov; prediksi kohort penuh, tanpa latih ulang.

## Bacaan K1 menurut aturan yang ditetapkan sebelum run

- **Sinyal oklusi di luar infark ada, tetapi lemah.** Di dalam AMI = 1 (K1a), AUROC M3a 0,643 [0,622; 0,663]:
  batas bawah > 0,5, besarnya < 0,70 ("lemah" menurut aturan baca). M2 0,631; ciri ST (M1) 0,522; usia dan jenis
  kelamin 0,480.
- **M3a tidak terbukti lebih baik dari M2 dalam mendeteksi oklusi di dalam infark:** selisih 0,012 [−0,003; 0,028]
  memuat 0. Di dalam STEMI selisih −0,007 [−0,032; 0,018]; di dalam NSTEMI 0,030 [0,006; 0,056]; di semua
  bukan-STEMI 0,025 [0,009; 0,040].
- **Akibat bagi naskah (aturan K1):** judul, abstrak, dan simpulan tidak menyebut deteksi oklusi koroner akut
  sebagai kemampuan model; AUROC 0,888 dilaporkan sebagai gabungan pengenalan infark dan oklusi.
- Rujukan: label `AMI` sendiri sebagai skor OMI memberi AUROC 0,954 (Se 1,000, Sp 0,908), di atas semua model.
  Skor OMI M3a membedakan AMI dengan AUROC 0,862 (untuk OMI 0,888).
- Di dalam NSTEMI, prediksi kohort penuh M3a (0,655 [0,623; 0,685]) sama dengan model yang dilatih ulang di NSTEMI
  (0,653, `Hasil_OMI_3.md`).
- Kalibrasi di dalam subhimpunan buruk untuk semua model (slope M3a 0,26–0,40 di K1a–K1c); di bukan-STEMI slope M3a
  0,931. Wajar: prevalensi subhimpunan jauh dari prevalensi latih, dan model dilatih pada semua EKG.

## Bacaan K2–K5

- **K2, aturan STEMI otomatis (Fourth UDMI di titik J).** Positif pada 2.111 dari 17.622 EKG (12,0 %); 125 EKG
  dengan deteksi gagal atau di luar batas P1 dihitung negatif. Untuk OMI: Se 0,218 [0,195; 0,243], Sp 0,887
  [0,882; 0,892]. Pada spesifisitas yang sama, M3a Se 0,698 [0,668; 0,727] dan M2 0,654 [0,628; 0,682]. Di dalam
  AMI = 1: aturan Se 0,218, Sp 0,854; M3a 0,259 [0,219; 0,297], M2 0,286 [0,245; 0,316] pada Sp aturan, jadi di
  dalam infark model hampir tidak melampaui aturan (selisih berpasangan tidak dihitung; CI tumpang tindih). Di dalam
  NSTEMI: aturan Se 0,086, Sp 0,898; M3a 0,211, M2 0,191.
- **K3, EKG dekat angiografi.** Di dalam AMI, AUROC M3a per kuartil 0,657 / 0,634 / 0,628 / 0,617 dan M2
  0,643 / 0,636 / 0,604 / 0,603; M1 0,506–0,574. Sinyal oklusi di dalam infark tetap lemah (< 0,70) bahkan pada EKG
  ≤ 440 menit sebelum angiografi. Di Q1 (4.408 EKG, 533 OMI, 12,1 %), sasaran utama: M3a 0,875 [0,860; 0,889],
  M2 0,851, ciri ST (M1) 0,585, di bawah usia dan jenis kelamin (0,600). Batas kuartil tercetak 3.935 menit
  (naskah lama 3.936: pembulatan cetak `pd.qcut`; n per kuartil tidak berubah).
- **K4, koreksi bobot kelas M2.** M2 terkoreksi: Brier 0,050 [0,048; 0,053] (mentah 0,120), intercept 0,121
  [0,039; 0,201], slope tetap 0,571 [0,540; 0,604]; M3a Brier 0,048, slope 1,061. Jadi selisih Brier dan intercept
  pada naskah lama berasal dari bobot kelas; selisih slope (M2 terlalu menyebar) bertahan. Net benefit M3a − M2
  terkoreksi 0,0030–0,0035 pada 1–10 %, semua CI di atas 0: kecil tetapi konsisten.
- **K5, net benefit di NSTEMI dan AMI (prediksi kohort penuh).** Di NSTEMI, M3a di bawah "obati semua" pada setiap
  ambang 1–30 %; baru di 40 % (saat "obati semua" sudah negatif, −0,097) M3a 0,009 [−0,000; 0,019] dan M2 terkoreksi
  0,020 [0,007; 0,034]. Di AMI pola sama: M2 terkoreksi melampaui "obati semua" hanya di 40 % (0,067 vs 0,047),
  M3a tidak (0,045). Prediksi kohort penuh **meremehkan** risiko di subhimpunan ini: dari 90 EKG NSTEMI yang diberi
  M3a risiko < 1 %, 17 (19 %) OMI; < 5 %: 457 EKG, 94 OMI (21 %); di AMI < 1 %: 103 EKG, 19 OMI (18 %).
  Hasil "tanpa manfaat bersih" di naskah lama (model dilatih ulang di NSTEMI) jadi bukan hanya akibat prevalensi
  terhadap ambang: EKG yang dinilai berisiko rendah tetap berisi sekitar satu OMI dari lima.

## Catatan sumber: label pra-latih ECGFounder

`tasks.txt` di repositori resmi (github.com/NickLJLee/ECGFounder, komit 67367071, 5 Agu 2025, salinan lokal
`$ECGFOUNDER_CODE`) memuat 150 label. Yang terkait infark atau ST: `ACUTE MI / STEMI`; lima
pola *injury* (`LATERAL`, `INFERIOR`, `ANTERIOR`, `INFEROLATERAL`, `ANTEROLATERAL INJURY PATTERN`); sembilan label
yang menyebut *infarct* (septal, anterior, lateral, anteroseptal, anterolateral, inferior, inferior-posterior,
posterior, dan `CONSIDER RIGHT VENTRICULAR INVOLVEMENT IN ACUTE INFERIOR INFARCT`); dua label elevasi ST
(`ST ELEVATION NOW PRESENT IN`, `ST ELEVATION HAS REPLACED ST DEPRESSION IN`). Abstrak PubMed 40771651 (Li dkk.,
2025): 10.771.552 EKG, 1.818.247 subjek, 150 kategori label anotasi kardiolog dari Harvard-Emory ECG Database.
Dibaca 13 Nov 2026.

## Keluaran K1 (salinan log)

## K1. Oklusi di luar infark (prediksi kohort penuh, tanpa latih ulang)

### K1a AMI=1: n EKG 2646, OMI 1133 (42.8 %), pasien 2608

| Model | AUROC | AUPRC | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- |
| M0 | 0.480 [0.459, 0.503] | 0.411 [0.387, 0.438] | 0.080 [0.061, 0.101] | -0.022 [-0.221, 0.183] | 2.292 [2.205, 2.376] |
| M1 | 0.522 [0.501, 0.543] | 0.459 [0.432, 0.488] | 0.130 [0.105, 0.156] | 2.786 [-3.511, 9.538] | 2.386 [2.303, 2.464] |
| M2 | 0.631 [0.612, 0.650] | 0.547 [0.518, 0.576] | 0.217 [0.190, 0.240] | 0.178 [0.147, 0.208] | -1.200 [-1.339, -1.058] |
| M3a | 0.643 [0.622, 0.663] | 0.540 [0.510, 0.571] | 0.187 [0.154, 0.218] | 0.370 [0.310, 0.427] | 1.408 [1.298, 1.520] |

Selisih AUROC M3a − M2: 0.012 [-0.003, 0.028] (replikat 2000).

### K1b STEMI=1: n EKG 1423, OMI 715 (50.2 %), pasien 1419

| Model | AUROC | AUPRC | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- |
| M0 | 0.480 [0.450, 0.510] | 0.487 [0.453, 0.524] | 0.081 [0.056, 0.109] | 0.048 [-0.236, 0.339] | 2.594 [2.480, 2.709] |
| M1 | 0.517 [0.489, 0.546] | 0.535 [0.498, 0.575] | 0.136 [0.106, 0.174] | 1.669 [-7.147, 11.699] | 2.686 [2.578, 2.792] |
| M2 | 0.591 [0.567, 0.616] | 0.597 [0.562, 0.634] | 0.207 [0.173, 0.239] | 0.140 [0.094, 0.193] | -1.447 [-1.609, -1.274] |
| M3a | 0.584 [0.556, 0.614] | 0.572 [0.535, 0.613] | 0.168 [0.136, 0.207] | 0.263 [0.177, 0.351] | 1.220 [1.083, 1.360] |

Selisih AUROC M3a − M2: -0.007 [-0.032, 0.018] (replikat 2000).

### K1c NSTEMI=1: n EKG 1221, OMI 417 (34.2 %), pasien 1200

| Model | AUROC | AUPRC | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- |
| M0 | 0.484 [0.451, 0.518] | 0.329 [0.297, 0.368] | 0.084 [0.056, 0.117] | -0.145 [-0.460, 0.168] | 1.921 [1.790, 2.046] |
| M1 | 0.564 [0.531, 0.594] | 0.389 [0.350, 0.436] | 0.122 [0.087, 0.178] | 14.079 [1.562, 30.306] | 2.018 [1.891, 2.139] |
| M2 | 0.625 [0.595, 0.652] | 0.442 [0.400, 0.489] | 0.186 [0.150, 0.233] | 0.157 [0.118, 0.199] | -0.812 [-1.036, -0.604] |
| M3a | 0.655 [0.623, 0.685] | 0.458 [0.415, 0.509] | 0.207 [0.145, 0.256] | 0.403 [0.304, 0.506] | 1.665 [1.505, 1.817] |

Selisih AUROC M3a − M2: 0.030 [0.006, 0.056] (replikat 2000).

### K1d STEMI=0: n EKG 16199, OMI 418 (2.6 %), pasien 15402

| Model | AUROC | AUPRC | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- |
| M0 | 0.604 [0.580, 0.629] | 0.036 [0.031, 0.042] | 0.160 [0.127, 0.193] | 0.892 [0.658, 1.169] | -0.946 [-1.047, -0.854] |
| M1 | 0.702 [0.676, 0.726] | 0.058 [0.050, 0.068] | 0.300 [0.259, 0.340] | 0.688 [0.415, 2.165] | -0.956 [-1.057, -0.865] |
| M2 | 0.818 [0.799, 0.836] | 0.133 [0.112, 0.160] | 0.505 [0.465, 0.545] | 0.452 [0.410, 0.496] | -3.222 [-3.346, -3.101] |
| M3a | 0.843 [0.824, 0.861] | 0.130 [0.110, 0.156] | 0.540 [0.492, 0.588] | 0.931 [0.860, 1.004] | -0.652 [-0.758, -0.547] |

Selisih AUROC M3a − M2: 0.025 [0.009, 0.040] (replikat 2000).

### Skor OMI tiap model untuk sasaran AMI (semua EKG analisis utama)

n EKG 17622, AMI 2646.

| Model | AUROC skor OMI untuk AMI | AUROC skor OMI untuk OMI |
| --- | --- | --- |
| M0 | 0.615 | 0.594 |
| M1 | 0.616 | 0.615 |
| M2 | 0.843 | 0.867 |
| M3a | 0.862 | 0.888 |

### Rujukan label klinis (tidak tersedia saat EKG dibaca)

| Skor | Himpunan | Se untuk OMI | Sp untuk OMI | AUROC |
| --- | --- | --- | --- | --- |
| AMI | analisis utama | 1.000 | 0.908 | 0.954 |
| STEMI | analisis utama | 0.631 | 0.957 | 0.794 |
| STEMI | AMI=1 | 0.631 | 0.532 | 0.582 |

## Keluaran K2–K5 (salinan log)

## K2. Aturan kriteria STEMI otomatis (Fourth UDMI, titik J, denyut median)

Deteksi gagal atau di luar batas P1 (dihitung negatif): 125 dari 17622 EKG. Aturan positif: 2111 (12.0 %).

| Himpunan | n EKG / OMI | Aturan Se | Aturan Sp | M2 Se pada Sp aturan | M3a Se pada Sp aturan |
| --- | --- | --- | --- | --- | --- |
| analisis utama | 17622 / 1133 | 0.218 [0.195, 0.243] | 0.887 [0.882, 0.892] | 0.654 [0.628, 0.682] | 0.698 [0.668, 0.727] |
| AMI=1 | 2646 / 1133 | 0.218 [0.195, 0.242] | 0.854 [0.835, 0.871] | 0.286 [0.245, 0.316] | 0.259 [0.219, 0.297] |
| NSTEMI=1 | 1221 / 417 | 0.086 [0.060, 0.115] | 0.898 [0.877, 0.919] | 0.191 [0.145, 0.247] | 0.211 [0.137, 0.280] |

## K3. Kuartil Time_Interval (batas P4)

Batas kuartil (menit): 5, 440, 1612, 3935, 10079.

### AUROC di dalam AMI=1 per kuartil

| Kuartil | n EKG AMI / OMI | M1 | M2 | M3a |
| --- | --- | --- | --- | --- |
| Q1 | 1147 / 533 | 0.506 [0.473, 0.538] | 0.643 [0.615, 0.672] | 0.657 [0.625, 0.688] |
| Q2 | 701 / 275 | 0.531 [0.488, 0.573] | 0.636 [0.595, 0.673] | 0.634 [0.590, 0.674] |
| Q3 | 439 / 185 | 0.520 [0.468, 0.570] | 0.604 [0.556, 0.651] | 0.628 [0.577, 0.678] |
| Q4 | 359 / 140 | 0.574 [0.517, 0.631] | 0.603 [0.549, 0.655] | 0.617 [0.560, 0.669] |

### Kuartil terpendek Q1, sasaran utama: n EKG 4408, OMI 533 (12.1 %)

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 0.600 [0.576, 0.624] | 0.156 [0.138, 0.177] | 0.108 [0.099, 0.116] | 0.151 [0.120, 0.180] | 1.015 [0.781, 1.257] | 0.688 [0.591, 0.778] |
| M1 | 0.585 [0.558, 0.614] | 0.191 [0.167, 0.220] | 0.109 [0.101, 0.118] | 0.225 [0.191, 0.259] | 24.409 [10.873, 36.959] | 0.694 [0.595, 0.783] |
| M2 | 0.851 [0.835, 0.866] | 0.460 [0.420, 0.504] | 0.150 [0.143, 0.158] | 0.553 [0.515, 0.601] | 0.524 [0.478, 0.577] | -2.109 [-2.244, -1.981] |
| M3a | 0.875 [0.860, 0.889] | 0.465 [0.424, 0.511] | 0.083 [0.077, 0.089] | 0.602 [0.555, 0.647] | 0.991 [0.917, 1.075] | 0.482 [0.370, 0.586] |

## K4. M2 dengan koreksi bobot kelas

| Model | AUROC | Brier | slope | intercept | NB1 | NB2 | NB5 | NB10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M2 mentah | 0.867 [0.857, 0.876] | 0.120 [0.117, 0.123] | 0.570 [0.539, 0.604] | -2.557 [-2.638, -2.477] | 0.056 [0.053, 0.060] | 0.051 [0.047, 0.054] | 0.038 [0.034, 0.041] | 0.020 [0.017, 0.024] |
| M2 terkoreksi | 0.867 [0.857, 0.876] | 0.050 [0.048, 0.053] | 0.571 [0.540, 0.604] | 0.121 [0.039, 0.201] | 0.054 [0.050, 0.057] | 0.049 [0.046, 0.053] | 0.041 [0.038, 0.044] | 0.031 [0.028, 0.034] |
| M3a | 0.888 [0.879, 0.896] | 0.048 [0.046, 0.051] | 1.061 [1.014, 1.112] | 0.007 [-0.061, 0.072] | 0.057 [0.053, 0.061] | 0.053 [0.049, 0.056] | 0.044 [0.041, 0.048] | 0.034 [0.031, 0.037] |

| Ambang | Obati semua | NB M3a − M2 terkoreksi |
| --- | --- | --- |
| 1 % | 0.0548 | 0.0031 [0.0021, 0.0041] |
| 2 % | 0.0452 | 0.0032 [0.0021, 0.0043] |
| 5 % | 0.0150 | 0.0035 [0.0022, 0.0047] |
| 10 % | -0.0397 | 0.0030 [0.0015, 0.0045] |

## K5. Net benefit 1–40 % di NSTEMI=1 dan AMI=1 (prediksi kohort penuh)

### NSTEMI=1: n EKG 1221, OMI 417 (34.2 %)

| Ambang | Obati semua | M2 terkoreksi NB | M3a NB | M3a: EKG di bawah ambang (OMI di antaranya) |
| --- | --- | --- | --- | --- |
| 1 % | 0.335 | 0.267 [0.243, 0.291] | 0.321 [0.295, 0.349] | 90 (17) |
| 2 % | 0.328 | 0.244 [0.220, 0.267] | 0.303 [0.277, 0.330] | 183 (33) |
| 5 % | 0.307 | 0.199 [0.177, 0.222] | 0.246 [0.220, 0.272] | 457 (94) |
| 10 % | 0.268 | 0.153 [0.133, 0.173] | 0.166 [0.144, 0.190] | 733 (185) |
| 15 % | 0.225 | 0.117 [0.099, 0.136] | 0.110 [0.091, 0.131] | 880 (252) |
| 20 % | 0.177 | 0.087 [0.070, 0.105] | 0.076 [0.059, 0.093] | 982 (295) |
| 30 % | 0.059 | 0.044 [0.030, 0.060] | 0.029 [0.017, 0.043] | 1106 (358) |
| 40 % | -0.097 | 0.020 [0.007, 0.034] | 0.009 [-0.000, 0.019] | 1167 (389) |

### AMI=1: n EKG 2646, OMI 1133 (42.8 %)

| Ambang | Obati semua | M2 terkoreksi NB | M3a NB | M3a: EKG di bawah ambang (OMI di antaranya) |
| --- | --- | --- | --- | --- |
| 1 % | 0.422 | 0.375 [0.358, 0.392] | 0.415 [0.397, 0.433] | 103 (19) |
| 2 % | 0.417 | 0.354 [0.337, 0.371] | 0.401 [0.382, 0.419] | 223 (45) |
| 5 % | 0.398 | 0.315 [0.298, 0.332] | 0.357 [0.339, 0.375] | 589 (133) |
| 10 % | 0.365 | 0.264 [0.247, 0.281] | 0.284 [0.265, 0.302] | 1025 (294) |
| 15 % | 0.327 | 0.220 [0.204, 0.236] | 0.224 [0.206, 0.241] | 1320 (431) |
| 20 % | 0.285 | 0.182 [0.165, 0.197] | 0.174 [0.158, 0.191] | 1561 (547) |
| 30 % | 0.183 | 0.114 [0.099, 0.128] | 0.092 [0.078, 0.106] | 1973 (760) |
| 40 % | 0.047 | 0.067 [0.054, 0.080] | 0.045 [0.033, 0.057] | 2246 (902) |
