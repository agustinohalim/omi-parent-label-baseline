# Hasil OMI 4 — eksploratif P4 (strata Time_Interval, kisi C lebar) dan berkas server penilai (11 November 2026)

> Satu-satunya sumber angka bagian ini. Semua dijalankan sesudah hasil utama diketahui, menurut Penyimpangan P4
> (`Prareg_OMI.md`, komit 9db904f), dengan skrip yang dikomit sebelum dijalankan: `omi_waktu.py` dan
> `omi_m3_ecgfounder.py --kisi-lebar / --embed-uji / --server` (komit 9db904f). Butir 1–2 eksploratif dan tidak
> mengubah perbandingan utama (`Hasil_OMI_3.md`). ECG-FM tidak dijalankan (P4 butir 1, keputusan pengguna).
> Run pertama kisi lebar berhenti karena memori habis sesaat (`_ArrayMemoryError`, 88 MiB) sebelum hasil apa pun;
> diulang tanpa perubahan kode. Tabel disalin apa adanya dari log (scratchpad sesi: `waktu.log`,
> `m3a_kisilebar.log`, `m3a_embed_uji.log`, `m3a_server.log`).

## 1. Strata Time_Interval (P4 butir 2)

Time_Interval = menit dari EKG ke angiografi. AUROC rata-rata tiga benih dari prediksi out-of-fold yang sudah ada;
CI 95 % bootstrap bergugus pasien 2.000 di dalam kuartil (benih 20261113).

n EKG = 17622; tanpa Time_Interval 0 (dikeluarkan); Time_Interval < 0: 0. Batas kuartil (menit): 5, 440, 1612, 3935, 10079.

| Kuartil | Menit (rentang) | Jam (median) | n EKG | OMI (%) | M1 | M2 | M3a | M3a − M2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | 5–440 | 3.6 | 4408 | 533 (12.1) | 0.585 [0.557, 0.610] | 0.851 [0.835, 0.866] | 0.875 [0.861, 0.887] | 0.024 [0.012, 0.035] |
| Q2 | 441–1611 | 20.9 | 4403 | 275 (6.2) | 0.636 [0.600, 0.672] | 0.864 [0.844, 0.882] | 0.867 [0.843, 0.887] | 0.003 [-0.013, 0.019] |
| Q3 | 1612–3933 | 45.1 | 4405 | 185 (4.2) | 0.627 [0.584, 0.668] | 0.867 [0.841, 0.890] | 0.900 [0.880, 0.919] | 0.033 [0.015, 0.052] |
| Q4 | 3936–10079 | 93.6 | 4406 | 140 (3.2) | 0.665 [0.621, 0.709] | 0.871 [0.844, 0.897] | 0.904 [0.882, 0.926] | 0.033 [0.015, 0.051] |

Replikat terpakai 2.000 dari 2.000 di setiap kuartil.

Bacaan (deskriptif, tanpa uji heterogenitas). Prevalensi OMI turun dari 12,1 % pada EKG ≤ 7,3 jam sebelum
angiografi ke 3,2 % pada EKG 2,7–7,0 hari sebelumnya. M2 dan M3a stabil atau sedikit naik antarkuartil; M1 naik dari
0,585 ke 0,665. M3a di atas M2 di Q1, Q3, Q4; di Q2 selisihnya 0,003 dengan CI melewati nol. Penjelasan turunnya
prevalensi (misalnya pasien paling akut diangiografi lebih cepat) tidak dapat diuji dengan data ini.

## 2. Kisi C diperlebar (P4 butir 3, kepekaan)


### Utama — kisi lebar

n EKG = 17622, pasien = 16703, OMI = 1133 (6.43 %). C terpilih: [0.001].

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M3a | 0.888 [0.879, 0.897] | 0.365 [0.338, 0.396] | 0.048 [0.046, 0.051] | 0.661 [0.630, 0.691] | 1.061 [1.013, 1.113] | 0.007 [-0.056, 0.073] |

Replikat bootstrap dengan slope tak terhitung (P2): M3a 0 dari 2000.

| Model | NB 1 % | NB 2 % | NB 5 % | NB 10 % |
| --- | --- | --- | --- | --- |
| M3a | 0.0569 [0.0535, 0.0608] | 0.0525 [0.0491, 0.0563] | 0.0442 [0.0409, 0.0479] | 0.0337 [0.0306, 0.0370] |
| Rawat semua | 0.0548 | 0.0452 | 0.0150 | -0.0397 |

Per benih (AUROC): M3a 0.888, 0.887, 0.889.


Waktu jalan 37,0 menit. Dengan kisi diperlebar ke 10⁻⁶, C yang terpilih tetap 10⁻³ di semua lipatan dan benih, jadi
C di tepi kisi terkunci bukan pembatas; titik AUROC dan prediksi sama dengan `Hasil_OMI_3.md` (CI sedikit berbeda
karena benih bootstrap lain).

## 3. Berkas server penilai (P4 butir 4)

Embedding `test.csv` 1.995 × 1.024, 1,4 menit di GPU, 0 kunci bobot hilang/lebih.

C terpilih (semua EKG analisis utama, benih 20261107): 0.001. Ambang Sp90 OOF per benih: 0.1305, 0.1323, 0.1327; rata-rata 0.1319.
Prevalensi OMI latih analisis utama 6.43 %. Test: n EKG 1995, pasien 1891; prediksi positif 264 (13.23 %); median p 0.0211.
Berkas: kirim_server_m3a.csv (biner, untuk diunggah) dan kirim_server_m3a_prob.csv (tidak diunggah).

Prediksi positif 13,2 % sesuai yang diharapkan dari spesifisitas 90 % dan sensitivitas 0,66 pada prevalensi
latih 6,4 % (perkiraan kasar, prevalensi test tak diketahui). Berkas di `$OMI_DATA/` (di luar repo).
Unggah ke server penilai: belum ⬜ (dilakukan pengguna, sekali; hasilnya dicatat di sini apa adanya).
