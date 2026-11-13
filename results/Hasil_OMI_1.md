# Hasil OMI 1 — garis dasar M0 (usia, jenis kelamin) dan M1 (ciri ST), split latih (11 November 2026)

> Satu-satunya sumber angka M0/M1. Skrip `omi_ciri_st.py` dan `omi_m01.py` (komit ed9be34, perbaikan lipatan 5efbe61),
> dikomit sebelum dijalankan; rancangan mengikuti `Prareg_OMI.md` + Penyimpangan P1. Data: Chongqing ACS (Sci Data
> 13:1009, figshare 29925314, CC0), hanya `train.csv`; `test.csv` belum disentuh. Waktu jalan 28,0 menit (run ulang P2: 59,3 menit). Log asli di
> scratchpad sesi; tabel bagian 2–5 disalin apa adanya dari log. Bagian 6 di luar pra-daftar (skrip
> `omi_diagnostik_st.py`, komit d7b31db), deskriptif, tanpa model.

## 1. Ekstraksi ciri ST (`omi_ciri_st.py`)

| Status | EKG |
| --- | --- |
| ok | 17825 |
| QRS di luar 50–200 ms | 104 |
| gagal deteksi | 31 |

QRS median 84 ms (p5–p95 72–110). Di analisis utama, 125 dari 17622 EKG tanpa ciri ST yang sah; diisi median lipatan
latih (P1).

## 2. Utama — OMI lawan bukan-OMI, tanpa Paced

n EKG = 17622, pasien = 16703, OMI = 1133 (6.43 %). C terpilih (semua lipatan dan benih): M0 [1.0]; M1 [0.001]; M0+M1 [0.001, 0.01].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 0.594 [0.579, 0.608] | 0.082 [0.076, 0.090] | 0.060 [0.056, 0.063] | 0.140 [0.122, 0.159] | 0.991 [0.839, 1.146] | 0.000 [-0.064, 0.062] |
| M1 | 0.615 [0.598, 0.633] | 0.106 [0.098, 0.117] | 0.060 [0.057, 0.063] | 0.235 [0.211, 0.259] | 0.534 [0.270, 2.056] | -0.002 [-0.066, 0.058] |
| M0+M1 | 0.613 [0.599, 0.627] | 0.093 [0.087, 0.102] | 0.060 [0.057, 0.063] | 0.158 [0.144, 0.172] | 1.160 [0.853, 1.552] | -0.003 [-0.067, 0.058] |

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M0 | 0.0548 [0.0510, 0.0586] | 0.0452 [0.0414, 0.0490] | 0.0211 [0.0178, 0.0247] | 0.0000 [0.0000, 0.0000] |
| M1 | 0.0548 [0.0510, 0.0586] | 0.0452 [0.0414, 0.0490] | 0.0151 [0.0111, 0.0190] | -0.0000 [-0.0001, -0.0000] |
| M0+M1 | 0.0548 [0.0510, 0.0586] | 0.0452 [0.0414, 0.0490] | 0.0172 [0.0136, 0.0209] | 0.0001 [-0.0000, 0.0002] |
| Rawat semua | 0.0548 | 0.0452 | 0.0150 | -0.0397 |

Selisih AUROC (deskriptif, bootstrap berpasangan): M1 − M0 = 0.022 [-0.001, 0.043]; M0+M1 − M1 = -0.002 [-0.020, 0.016].

Per benih (AUROC): M0 0.595, 0.593, 0.593; M1 0.608, 0.623, 0.615; M0+M1 0.614, 0.617, 0.609.

## 3. Sekunder 1 — NSTEMI-OMI lawan NSTEMI-bukan-OMI, tanpa Paced

n EKG = 1221, pasien = 1200, OMI = 417 (34.15 %). C terpilih (semua lipatan dan benih): M0 [1.0]; M1 [0.001, 0.01]; M0+M1 [0.001, 0.01].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 0.458 [0.432, 0.484] | 0.315 [0.287, 0.348] | 0.226 [0.218, 0.235] | 0.082 [0.061, 0.101] | -1.975 [-3.134, -0.854] | 0.001 [-0.120, 0.116] |
| M1 | 0.541 [0.511, 0.572] | 0.371 [0.337, 0.414] | 0.225 [0.216, 0.234] | 0.117 [0.086, 0.154] | 0.371 [-0.300, 1.446] | 0.001 [-0.122, 0.118] |
| M0+M1 | 0.531 [0.501, 0.562] | 0.363 [0.331, 0.404] | 0.225 [0.217, 0.234] | 0.110 [0.082, 0.145] | 0.343 [-0.368, 1.242] | 0.000 [-0.122, 0.117] |

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M0 | 0.3349 [0.3082, 0.3617] | 0.3281 [0.3011, 0.3551] | 0.3069 [0.2791, 0.3348] | 0.2684 [0.2390, 0.2978] |
| M1 | 0.3349 [0.3082, 0.3617] | 0.3281 [0.3011, 0.3551] | 0.3063 [0.2788, 0.3341] | 0.2679 [0.2389, 0.2973] |
| M0+M1 | 0.3349 [0.3082, 0.3617] | 0.3281 [0.3011, 0.3551] | 0.3066 [0.2790, 0.3344] | 0.2682 [0.2390, 0.2976] |
| Rawat semua | 0.3349 | 0.3281 | 0.3069 | 0.2684 |

Selisih AUROC (deskriptif, bootstrap berpasangan): M1 − M0 = 0.083 [0.040, 0.125]; M0+M1 − M1 = -0.010 [-0.018, -0.001].

Per benih (AUROC): M0 0.457, 0.470, 0.449; M1 0.537, 0.540, 0.545; M0+M1 0.534, 0.534, 0.525.

## 4. Sekunder 2 — teritori penyebab (satu teritori, LM dibuang)

n EKG = 901 (LAD 344, LCX 207, RCA 350); di antaranya NSTEMI-OMI 299 (LAD 87, LCX 105, RCA 107).

**semua OMI satu teritori** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M0 | 0.511 [0.474, 0.547] | 0.472 [0.438, 0.506] | 0.531 [0.496, 0.569] | 0.505 [0.481, 0.530] |
| M1 | 0.785 [0.756, 0.816] | 0.631 [0.589, 0.670] | 0.707 [0.674, 0.740] | 0.707 [0.684, 0.731] |

**NSTEMI-OMI (eksploratif)** (AUROC satu-lawan-sisanya)

| Model | LAD | LCX | RCA | makro |
| --- | --- | --- | --- | --- |
| M0 | 0.458 [0.389, 0.524] | 0.529 [0.472, 0.582] | 0.550 [0.481, 0.619] | 0.512 [0.468, 0.557] |
| M1 | 0.559 [0.492, 0.624] | 0.588 [0.522, 0.651] | 0.504 [0.437, 0.572] | 0.550 [0.507, 0.592] |

## 5. Kepekaan — utama dengan Paced

n EKG = 17960, pasien = 17018, OMI = 1151 (6.41 %). C terpilih (semua lipatan dan benih): M0 [1.0]; M1 [0.001]; M0+M1 [0.001, 0.01].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | 0.591 [0.576, 0.605] | 0.080 [0.074, 0.087] | 0.059 [0.056, 0.063] | 0.128 [0.111, 0.144] | 0.982 [0.826, 1.139] | 0.000 [-0.062, 0.061] |
| M1 | 0.615 [0.598, 0.632] | 0.105 [0.097, 0.116] | 0.060 [0.057, 0.063] | 0.233 [0.212, 0.258] | 0.414 [0.191, 1.347] | -0.002 [-0.063, 0.058] |
| M0+M1 | 0.613 [0.598, 0.628] | 0.090 [0.084, 0.098] | 0.060 [0.057, 0.063] | 0.144 [0.131, 0.159] | 1.295 [0.957, 1.670] | -0.003 [-0.065, 0.056] |

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M0 | 0.0546 [0.0510, 0.0584] | 0.0450 [0.0413, 0.0487] | 0.0208 [0.0174, 0.0242] | -0.0000 [-0.0000, 0.0000] |
| M1 | 0.0546 [0.0510, 0.0584] | 0.0450 [0.0413, 0.0488] | 0.0149 [0.0111, 0.0188] | -0.0001 [-0.0001, -0.0000] |
| M0+M1 | 0.0546 [0.0510, 0.0584] | 0.0450 [0.0413, 0.0488] | 0.0164 [0.0128, 0.0201] | -0.0000 [-0.0001, 0.0001] |
| Rawat semua | 0.0546 | 0.0450 | 0.0148 | -0.0399 |

Selisih AUROC (deskriptif, bootstrap berpasangan): M1 − M0 = 0.024 [0.001, 0.046]; M0+M1 − M1 = -0.002 [-0.021, 0.016].

Per benih (AUROC): M0 0.591, 0.594, 0.588; M1 0.617, 0.614, 0.613; M0+M1 0.613, 0.619, 0.607.

## 6. Diagnostik ciri ST (di luar pra-daftar, deskriptif)

Ditulis karena AUROC M1 rendah, untuk membedakan "ciri rusak" dari "sinyal memang lemah". Populasi: analisis utama
dengan status ciri ok, n EKG = 17497. ST60 maks = maksimum 11 sadapan tanpa aVR.

| Jenis | n | ST60 maks median (mV) | ST60 V2 median | ST60 II median | QRS median (ms) | ST60 maks > 0,1 mV |
| --- | --- | --- | --- | --- | --- | --- |
| STEMI | 1411 | 0.159 | 0.118 | 0.022 | 86 | 0.728 |
| NSTEMI | 1215 | 0.118 | 0.095 | -0.008 | 84 | 0.587 |
| UA | 6086 | 0.112 | 0.096 | 0.011 | 82 | 0.563 |
| bukan SKA | 8785 | 0.110 | 0.090 | 0.010 | 84 | 0.548 |

AUROC ST60 maks, STEMI lawan bukan SKA: 0.640
AUROC ST60 maks, OMI lawan bukan-OMI: 0.602

| Time_Interval (kuartil) | n | OMI % | AUROC ST60 maks (OMI) |
| --- | --- | --- | --- |
| (4.999, 438.0] | 4380 | 12.0 | 0.627 |
| (438.0, 1606.0] | 4372 | 6.3 | 0.572 |
| (1606.0, 3930.0] | 4373 | 4.2 | 0.560 |
| (3930.0, 10079.0] | 4372 | 3.2 | 0.586 |

## 7. Catatan baca

- **Sinyal ST lemah pada data ini, bukan ciri yang rusak (sejauh bisa diperiksa).** Urutan median ST60 maks
  STEMI > NSTEMI ≈ UA ≈ bukan SKA sesuai arah klinis, QRS median wajar, dan satu ciri tunggal (ST60 maks) sudah
  memberi 0,602 untuk OMI, dekat M1 0,615. Tetapi STEMI hanya 0,640 atas bukan SKA, dan 27 % EKG STEMI tidak punya
  elevasi > 0,1 mV di sadapan mana pun. Dugaan kerja: banyak EKG direkam jauh dari saat oklusi. Makalah data (Du dkk., Sci Data 13:1009,
  bagian *Data exclusion*, dibaca 11 Nov dari PDF yang diberikan pengguna): "Only pre-angiography ECGs were retained",
  EKG dalam 7 hari sebelum DSA, `Time_Interval` = selang EKG–angiografi "with the unit specified in minutes"; semua
  EKG dalam jendela itu disertakan. Jadi median 1607 menit ≈ 27 jam sebelum angiografi. AUROC tertinggi di kuartil Time_Interval
  terpendek (0,627) mendukung dugaan itu tetapi tidak membuktikannya. Belum diperiksa: ketepatan titik J terhadap
  anotasi manual pada sampel — ⬜ sebelum angka M1 masuk naskah.
- **M1 dan M0+M1 sangat teregularisasi** (C = 0,001 hampir di semua lipatan); slope kalibrasi M1 0,534 dengan CI
  lebar [0,270, 2,056]. Model mendekati prediktor prevalensi yang sedikit bergeser.
- **Selisih M1 − M0 utama tidak meyakinkan** (CI menyentuh 0); pada kepekaan dengan Paced CI tepat di atas 0. Keduanya
  deskriptif menurut pra-daftar.
- **Net benefit**: pada ambang 1 % dan 2 % semua model sama dengan rawat semua; pada 5 % M0 di atas M1 dan rawat
  semua; pada 10 % semua ≈ 0. Tidak ada manfaat keputusan dari ciri ST sederhana.
- **NSTEMI**: M0 di bawah 0,5 (0,458; slope negatif) — usia/jenis kelamin berlawanan arah di subkelompok ini; M1
  0,541 lemah. NB ≈ rawat semua karena prevalensi 34 %.
- **Teritori**: satu-satunya sinyal yang jelas (M1 makro 0,707; LAD 0,785). Pada NSTEMI-OMI hilang (0,550).
- **Kalibrasi, sesudah Penyimpangan P2** (komit 740b1e3): run pertama memberi 160 peringatan overflow dan batas
  bawah slope M0+M1 sekunder 1 −1336835,661 (artefak Newton tak teredam). Dijalankan ulang utuh dengan Newton teredam
  (59,3 menit): prediksi out-of-fold identik bita demi bita dengan run pertama, semua angka selain CI slope identik,
  0 replikat tak konvergen di keempat analisis, 0 peringatan. Empat sel CI slope di tabel atas sudah diganti dengan
  hasil run ulang.

## 8. Langkah berikutnya

M2/M3 (model EKG penuh) masih memuat butir "BELUM DITETAPKAN" di pra-daftar; ditetapkan lewat Penyimpangan bertanggal
sebelum pelatihan apa pun. Pemeriksaan titik J manual dan satuan Time_Interval didahulukan karena menentukan apakah
garis dasar ST ini adil.
