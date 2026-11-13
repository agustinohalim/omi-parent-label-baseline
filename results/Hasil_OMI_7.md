# Hasil OMI 7 — fase C, uji ukur dan latih ulang di dalam infark (13 November 2026)

> Pra-daftar `Prareg_OMI_C.md` (terkunci 49dd00e); skrip `omi_fase_c.py` (komit c2cf651), B = 2.000, satu run
> penuh 13 Nov; log `$OMI_DATA/fase_c_B2000.log` (disalin di bawah). Uji jalan B = 5 (C5, C2, C4)
> sebelumnya, angkanya tidak dipakai. Semua butir eksploratif terhadap pra-daftar 7 Nov.

## Bacaan menurut aturan yang ditetapkan sebelum run

- **C1 — aturan otomatis tidak mereproduksi diagnosis STEMI.** Aturan K2 (titik J; 2.111 positif, sama dengan K2)
  menangkap 24,6 % EKG berdiagnosis STEMI pulang (Sp 0,891); di kuartil Q1 (≤ 440 menit) **0,309 < 0,60**. Varian
  J + 60 ms: STEMI 0,363, Q1 0,420. Di 1.411 EKG STEMI dengan deteksi ok, elevasi pasangan terbesar di atas ambang
  bermedian −0,052 mV (IQR −0,083 sampai −0,000); hanya 24,8 % ≥ 0. **Akibat (aturan C1):** angka 21,8 % dan
  perbandingan model dengan kriteria STEMI keluar dari *highlights*, abstrak, dan simpulan; di Hasil dilaporkan sebagai
  uji pipa ukur; Pembahasan menyebut perbandingan dengan kriteria STEMI tidak dapat dibuat dengan pipa ini; klaim
  lemahnya ciri ST dibatasi ke "implementasi ini". Data tidak membedakan apakah EKG direkam di luar fase elevasi ST
  atau pengukuran gagal; keduanya mungkin.
- **C2 — skor OMI tinggi pada infark tanpa oklusi.** M3a: (a) OMI lawan tanpa AMI 0,912 [0,904; 0,920]; (b) AMI tanpa
  OMI lawan tanpa AMI **0,825 [0,813; 0,836]** (batas bawah ≥ 0,70, aturan terpenuhi); (c) OMI lawan AMI tanpa OMI
  0,643 [0,622; 0,664]. M2: 0,891 / 0,808 / 0,631. M1: 0,625 / 0,609 / 0,522. M0: 0,605 / 0,622 / 0,480.
- **C3 — dilatih di dalam infark tetap lemah.** *Probe* dilatih ulang di AMI: AUROC **0,657 [0,636; 0,678]** (batas
  bawah < 0,70: bacaan "lemah" tetap), +0,014 [−0,001; 0,028] atas *probe* kohort penuh; kalibrasi membaik (slope
  0,805, intercept 0,007). Ciri ST dilatih ulang 0,536, usia–jenis kelamin 0,513. Di STEMI: *probe* 0,621 [0,594;
  0,649], +0,037 [0,007; 0,066] atas kohort penuh; ciri ST 0,544. C terpilih *probe* dan ciri ST di AMI 10⁻³ di semua
  lipatan (tepi kisi; di STEMI ciri ST 10⁻³ sampai 1).
- **C4 — model NSTEMI dilatih ulang (pra-daftar asli).** Tidak ada EKG NSTEMI yang diberi risiko < 5 % (rata-rata
  benih 0 EKG), jadi net benefit = obati semua pada 1–5 % secara mekanis. Di bawah 10 %: 3 EKG (2 OMI); 15 %: 49 (6);
  20 %: 167 (33, 20 %). Selisih atas obati semua dengan CI di atas 0 hanya pada 30 % (0,037 [0,015; 0,059]) dan
  40 % (0,153 [0,119; 0,187]); titik rata-rata benih di atas obati semua dan nol pada 15–16 % dan 19–59 %. Kalimat
  naskah "about 25 % to 60 %" (satu benih, Gambar 2b) diganti.
- **C5 — Tabel 1 baru.** OMI 1.133 EKG (1.122 pasien), AMI tanpa OMI 1.513 (1.497), tanpa AMI 14.976 (14.303).
  Laki-laki 78,2 / 77,9 / 57,3 %. `Time_Interval` median 475 / 632 / 1.779 menit. Tanpa AMI: UA 41,0 %, CTO 6,3 %.
  Dua EKG `AMI = 1` tanpa `STEMI` maupun `NSTEMI` (satu OMI), jadi AMI 2.646 = STEMI 1.423 + NSTEMI 1.221 + 2.

## Keluaran (salinan log)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## C5. Karakteristik per kelompok (analisis utama)

| Ciri | OMI | AMI tanpa OMI | tanpa AMI |
| --- | --- | --- | --- |
| n EKG | 1133 | 1513 | 14976 |
| n pasien | 1122 | 1497 | 14303 |
| usia, median (IQR) | 66 (56–73) | 67 (57–75) | 65 (57–72) |
| laki-laki (gender = 1), % | 78.2 | 77.9 | 57.3 |
| Time_Interval menit, median (IQR) | 475 (221–1789) | 632 (283–1977) | 1779 (577–4111) |
| STEMI, n (%) | 715 (63.1) | 708 (46.8) | 0 (0.0) |
| NSTEMI, n (%) | 417 (36.8) | 804 (53.1) | 0 (0.0) |
| UA, n (%) | 0 (0.0) | 0 (0.0) | 6135 (41.0) |
| Prior_PCI, n (%) | 78 (6.9) | 104 (6.9) | 1122 (7.5) |
| VF_VT, n (%) | 72 (6.4) | 74 (4.9) | 673 (4.5) |
| PCI, n (%) | 639 (56.4) | 765 (50.6) | 3088 (20.6) |
| CTO, n (%) | 0 (0.0) | 0 (0.0) | 946 (6.3) |

AMI = 1 tanpa STEMI maupun NSTEMI: 2 EKG (OMI 1). STEMI = 1 dan NSTEMI = 1 bersamaan: 0. STEMI atau NSTEMI dengan AMI = 0: 0.

## C1. Aturan STEMI otomatis lawan diagnosis STEMI pulang

Aturan titik J positif: 2111 dari 17622; varian J + 60 ms positif: 3118.

| Aturan | Sasaran | n positif sasaran | Se | Sp |
| --- | --- | --- | --- | --- |
| titik J | STEMI | 1423 | 0.246 | 0.891 |
| titik J | OMI | 1133 | 0.218 | 0.887 |
| J + 60 ms | STEMI | 1423 | 0.363 | 0.839 |
| J + 60 ms | OMI | 1133 | 0.319 | 0.833 |

Sensitivitas untuk STEMI per kuartil Time_Interval (batas P4):

| Kuartil | n STEMI | Se titik J | Se J + 60 ms |
| --- | --- | --- | --- |
| Q1 | 653 | 0.309 | 0.420 |
| Q2 | 334 | 0.204 | 0.308 |
| Q3 | 226 | 0.208 | 0.354 |
| Q4 | 210 | 0.157 | 0.281 |

Elevasi pasangan terbesar di atas ambang (mV), STEMI dengan deteksi ok (n = 1411): median -0.052, IQR -0.083 sampai -0.000; bagian ≥ 0: 0.248.

## C2. Tiga AUROC berpasangan (skor OMI kohort penuh)

OMI 1133, AMI tanpa OMI 1513, tanpa AMI 14976.

| Pasangan | M0 | M1 | M2 | M3a |
| --- | --- | --- | --- | --- |
| (a) OMI lawan tanpa AMI | 0.605 [0.590, 0.620] | 0.625 [0.607, 0.641] | 0.891 [0.881, 0.899] | 0.912 [0.904, 0.920] |
| (b) AMI tanpa OMI lawan tanpa AMI | 0.622 [0.608, 0.636] | 0.609 [0.594, 0.625] | 0.808 [0.797, 0.818] | 0.825 [0.813, 0.836] |
| (c) OMI lawan AMI tanpa OMI | 0.480 [0.458, 0.502] | 0.522 [0.501, 0.543] | 0.631 [0.613, 0.650] | 0.643 [0.622, 0.664] |

## C4. M3a dilatih ulang di NSTEMI (pra-daftar asli): EKG di bawah ambang

n EKG 1221, OMI 417 (34.2 %).

| Ambang | Obati semua | M3a NB | M3a − obati semua | EKG di bawah ambang (OMI), rata-rata benih |
| --- | --- | --- | --- | --- |
| 1 % | 0.335 | 0.335 [0.308, 0.362] | 0.000 [-0.000, 0.000] | 0 (0) |
| 2 % | 0.328 | 0.328 [0.301, 0.356] | 0.000 [-0.000, 0.000] | 0 (0) |
| 5 % | 0.307 | 0.307 [0.279, 0.335] | 0.000 [-0.000, 0.000] | 0 (0) |
| 10 % | 0.268 | 0.267 [0.238, 0.297] | -0.001 [-0.003, 0.000] | 3 (2) |
| 15 % | 0.225 | 0.226 [0.196, 0.257] | 0.001 [-0.003, 0.005] | 49 (6) |
| 20 % | 0.177 | 0.178 [0.146, 0.209] | 0.001 [-0.009, 0.010] | 167 (33) |
| 30 % | 0.059 | 0.096 [0.066, 0.126] | 0.037 [0.015, 0.059] | 537 (129) |
| 40 % | -0.097 | 0.056 [0.031, 0.080] | 0.153 [0.119, 0.187] | 857 (231) |

Ambang 1–60 % (langkah 1 %) dengan NB rata-rata benih > obati semua dan > 0: 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59 %.

## C3. Latih ulang di dalam AMI=1 dan STEMI=1 (prosedur fase A)

### AMI=1: n EKG 2646, OMI 1133 (42.8 %), pasien 2608. C terpilih: M1 latih ulang [0.001]; M3a latih ulang [0.001]

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 latih ulang | 0.513 [0.491, 0.535] | 0.437 [0.411, 0.465] | 0.245 [0.242, 0.248] | 0.098 [0.079, 0.118] | 0.418 [-0.434, 1.283] | 0.000 [-0.079, 0.079] |
| M1 latih ulang | 0.536 [0.515, 0.558] | 0.476 [0.450, 0.507] | 0.244 [0.241, 0.247] | 0.152 [0.125, 0.180] | 0.866 [0.308, 1.556] | 0.001 [-0.078, 0.079] |
| M3a latih ulang | 0.657 [0.636, 0.678] | 0.558 [0.530, 0.591] | 0.229 [0.223, 0.234] | 0.212 [0.177, 0.248] | 0.805 [0.685, 0.938] | 0.007 [-0.077, 0.089] |
| M3a kohort penuh | 0.643 [0.622, 0.664] | 0.540 [0.512, 0.572] | 0.290 [0.278, 0.302] | 0.187 [0.154, 0.219] | 0.370 [0.310, 0.432] | 1.408 [1.298, 1.513] |

Selisih AUROC M3a latih ulang − M3a kohort penuh: 0.014 [-0.001, 0.028].

Selisih AUROC M3a latih ulang − M1 latih ulang: 0.121 [0.092, 0.150].

### STEMI=1: n EKG 1423, OMI 715 (50.2 %), pasien 1419. C terpilih: M1 latih ulang [0.001, 0.1, 1]; M3a latih ulang [0.001]

| Model | AUROC | AUPRC | Brier | Se@Sp90 | slope | intercept |
| --- | --- | --- | --- | --- | --- | --- |
| M0 latih ulang | 0.516 [0.487, 0.544] | 0.516 [0.482, 0.555] | 0.250 [0.249, 0.252] | 0.110 [0.079, 0.144] | 0.306 [-0.561, 1.186] | 0.000 [-0.101, 0.105] |
| M1 latih ulang | 0.544 [0.516, 0.570] | 0.554 [0.519, 0.591] | 0.250 [0.248, 0.252] | 0.153 [0.119, 0.194] | 0.354 [-0.061, 1.033] | 0.005 [-0.094, 0.110] |
| M3a latih ulang | 0.621 [0.594, 0.649] | 0.607 [0.570, 0.648] | 0.240 [0.234, 0.247] | 0.197 [0.157, 0.237] | 0.701 [0.512, 0.901] | 0.003 [-0.103, 0.110] |
| M3a kohort penuh | 0.584 [0.554, 0.613] | 0.572 [0.537, 0.614] | 0.310 [0.296, 0.325] | 0.168 [0.138, 0.206] | 0.263 [0.180, 0.350] | 1.220 [1.086, 1.353] |

Selisih AUROC M3a latih ulang − M3a kohort penuh: 0.037 [0.007, 0.066].

Selisih AUROC M3a latih ulang − M1 latih ulang: 0.077 [0.043, 0.112].
