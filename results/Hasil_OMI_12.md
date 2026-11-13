# Hasil OMI 12 — fase H: pembanding berlabel STEMI, label kontrol-negatif, jarak ke angiografi (13 November 2026)

> Pra-daftar `Prareg_OMI_H.md` (terkunci 1a15fd4; penyimpangan P1 3181816 menambah H3, P2 a33673e menambah H4, P3 15d4379 menambah H5–H6, masing-masing
> sebelum dijalankan); skrip
> `omi_fase_h.py`. 13 Nov: latih H1 (*probe*-STEMI, CV dalam, tiga penetapan lipatan) 17,0 menit, H2 1,4 menit; H1+H2 bootstrap 6,5 menit;
> H3 2,0 menit, H4 10,6 menit, H5–H6 2,2 menit. Log `$OMI_DATA/fase_h_latih.log`, `fase_h_H1H2_B2000.log`,
> `fase_h_H3_B2000.log`, `fase_h_H4_B2000.log`, `fase_h_H5H6_B2000.log` (keluaran analisis disalin di bawah). Tidak ada unduhan. Semua butir eksploratif.

## Bacaan menurut aturan yang dikunci

- **H1 — label oklusi melampaui label STEMI di dalam infark.** *Probe* berlabel STEMI (C = 0,001 di setiap lipatan;
  AUROC untuk STEMI sendiri 0,932) memberi AUROC (c) 0,611 untuk OMI, *probe* berlabel OMI 0,643: selisih **0,032
  [0,022; 0,042]**. OMI lawan semua 0,888 lawan 0,878, selisih 0,010 [0,005; 0,015]; di dalam NSTEMI 0,655 lawan 0,614,
  0,041 [0,024; 0,058]; di dalam STEMI (deskriptif) 0,584 lawan 0,537, 0,047 [0,031; 0,064]. Aturan: batas bawah (c)
  > 0 → **ya**: naskah boleh menyatakan label oklusi mengajarkan sesuatu di luar pola STEMI. Catatan: batas bawah
  0,022 di bawah 0,03, jadi besarnya terhadap margin ±0,03 belum terselesaikan.
- **H2 — tak satu pun label kontrol menyamai label oklusi.** *Probe* berlabel OMI asli pada lipatan ini 0,6431 (sama
  dengan F1). Label kontrol (AMI dan …): PCI 0,606, selisih 0,037 [0,027; 0,047]; VF/VT 0,602, 0,041 [0,027; 0,056];
  usia ≥ median 0,593, 0,050 [0,037; 0,065]; laki-laki 0,597, 0,046 [0,035; 0,058]; dekat angiografi 0,594, 0,049
  [0,037; 0,060]; STEMI 0,610, 0,033 [0,023; 0,042]. Hanya kontrol STEMI di atas persentil ke-95 nol berlapis
  (0,609). Aturan: setiap batas bawah > 0 → **ya**: naskah boleh menyatakan keunggulan khas label oklusi di antara
  subset klinis yang diuji. Kontrol STEMI (satu lipatan, C tetap) dan *probe*-STEMI H1 (tiga lipatan, C dari CV
  dalam) memberi angka yang hampir sama (0,610 dan 0,611).
- **H3 (P1) — jarak EKG ke angiografi tidak menjelaskan keunggulan.** Jarak saja memisahkan OMI dari infark tanpa
  oklusi dengan AUROC 0,544 [0,521; 0,565]. Dengan log(1 + jarak) ditambahkan ke *embedding*, *probe* berlabel OMI
  0,648 dan berlabel AMI 0,606; selisih 0,041 [0,032; 0,051], tanpa jarak pada lipatan yang sama 0,042 [0,033; 0,051].
  Aturan: batas bawah > 0 → **ya**: naskah boleh menyatakan keunggulan tidak dijelaskan oleh jarak ke angiografi;
  tahap penyakit dan reperfusi tetap disebut di keterbatasan (awitan gejala tidak ada di data).

## Penyimpangan P2 dan P3 (sesudah panel 8)

- **H4(i) (P2) — *probe* berlabel infark pada lipatan yang sama dengan nol: 0,6010**, persentil ke-53 nol berlapis
  (p95 0,6092) dan ke-82 nol tanpa lapis (p95 0,6048). Aturan ≤ p95 berlapis → **ya**: naskah boleh menyebutnya "no
  more than a random infarction subset with the same STEMI share".
- **H4(ii) (P2) — Q4 − Q1 *probe* −0,023 [−0,053; 0,006]**, CNN 0,008 [−0,032; 0,054]. Aturan CI di dalam ±0,03 →
  **tidak**: Gambar 2 diberi judul deskriptif; naskah menyatakan keunggulan yang lebih kecil di kuartil terjauh tidak
  tersingkirkan; "did not depend on the interval" dibuang.
- **H4(iii) (P2) — AUROC berlapis kuartil jarak:** selisih label *probe* 0,044 [0,034; 0,054], CNN 0,041 [0,028; 0,054].
  Aturan batas bawah *probe* > 0 → **ya**: "held within quartiles of the ECG-to-angiography delay".
- **H4(iv) (P2) — perubahan keunggulan dengan jarak dimasukkan: −0,001 [−0,002; 0,001].** Aturan di dalam ±0,03 →
  **ya**: "unchanged".
- **H5 (P3) — pasangan bersarang kedua.** STEMI lawan NSTEMI di dalam AMI (1.423 / 2.644): *probe* berlabel STEMI
  0,830, berlabel AMI 0,769; selisih **0,061 [0,053; 0,069]**. Deskriptif: label bersarang yang ditentukan dari EKG dan
  diagnosis menaikkan AUROC di dalam induk 0,061, dari titik awal 0,769; label oklusi menaikkan 0,042 dari titik awal
  0,601.
- **H6 (P3) — titik-balik tinjauan label.** Dari label acak berlapis (k = 0: keunggulan +0,011), menukar k pasangan
  menurut skor *probe* berlabel AMI menaikkan AUROC kedua *probe* bersama (k = 400, 30,2 % EKG infark berubah: 0,904
  lawan 0,917) tetapi keunggulan tidak pernah mencapai 0,042 (+0,004, +0,003, −0,000, −0,010, −0,013 untuk k = 25–400).
  Bacaan sesuai pra-daftar: tidak ada k sampai 400 (30 % EKG infark) yang menghasilkan keunggulan sebesar yang diamati.
  Batasnya: pertukaran mengikuti skor *probe* infark sebagai wakil "tampak di EKG"; tinjauan yang mengikuti ciri yang
  tidak terbaca *probe* infark (misalnya ciri khas oklusi) tidak diuji oleh simulasi ini.

## Keluaran

Salinan `fase_h_H1H2_B2000.log`:

### H1. Label oklusi lawan label STEMI (probe)

| Sasaran | n OMI / n | probe-OMI | probe-STEMI | selisih OMI − STEMI |
| --- | --- | --- | --- | --- |
| OMI lawan semua | 1133 / 17622 | 0.888 | 0.878 | 0.010 [0.005, 0.015] |
| (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.643 | 0.611 | 0.032 [0.022, 0.042] |
| di dalam NSTEMI | 417 / 1221 | 0.655 | 0.614 | 0.041 [0.024, 0.058] |
| di dalam STEMI (deskriptif) | 715 / 1423 | 0.584 | 0.537 | 0.047 [0.031, 0.064] |

AUROC probe-STEMI untuk sasaran latihnya sendiri (STEMI lawan semua): 0.932.
Aturan: batas bawah selisih (c) > 0: **ya**.

### H2. Label kontrol-negatif di dalam infark (probe, C = 0,001, lipatan 20261107)

Probe berlabel OMI asli pada lipatan ini: AUROC (c) 0.6431 (F1: 0.6431).

| Label kontrol (AMI dan …) | n positif | AUROC (c) untuk OMI | > p95 nol berlapis (0,609) | selisih asli − kontrol |
| --- | --- | --- | --- | --- |
| PCI | 1404 | 0.606 | tidak | 0.037 [0.027, 0.047] |
| VF/VT | 146 | 0.602 | tidak | 0.041 [0.027, 0.056] |
| usia >= median AMI | 1373 | 0.593 | tidak | 0.050 [0.037, 0.065] |
| laki-laki | 2065 | 0.597 | tidak | 0.046 [0.035, 0.058] |
| dekat angiografi (<= median AMI) | 1323 | 0.594 | tidak | 0.049 [0.037, 0.060] |
| STEMI | 1423 | 0.610 | ya | 0.033 [0.023, 0.042] |

Aturan: batas bawah selisih asli − kontrol > 0 untuk setiap kontrol: **ya**.

Waktu jalan: 6.5 menit.

Salinan `fase_h_H3_B2000.log`:

### H3. Jarak EKG ke angiografi (penyimpangan P1)

(i) AUROC jarak saja (skor = −Time_Interval) untuk (c): 0.544 [0.521, 0.565].

Latih empat *probe*: 0.9 menit.

| *Probe* | AUROC (c) |
| --- | --- |
| OMI, tanpa jarak | 0.643 |
| AMI, tanpa jarak | 0.601 |
| OMI, dengan jarak | 0.648 |
| AMI, dengan jarak | 0.606 |

(ii) Selisih label oklusi − label infark, (c), tanpa jarak: 0.042 [0.033, 0.051].

(ii) Selisih label oklusi − label infark, (c), dengan jarak: 0.041 [0.032, 0.051].

Aturan: batas bawah selisih dengan jarak > 0: **ya**.

Waktu jalan: 2.0 menit.

Salinan `fase_h_H4_B2000.log`:

### H4. Penyimpangan P2

(i) *Probe* berlabel AMI, lipatan 20261107, C 0,001: AUROC (c) 0.6010. Nol tanpa lapis: 82 % di bawahnya (p95 0.6048); nol berlapis: 53 % di bawahnya (p95 0.6092). Aturan ≤ p95 berlapis: **ya**.

probe: (ii) Q4 − Q1 -0.023 [-0.053, 0.006]; (iii) selisih AUROC berlapis kuartil 0.044 [0.034, 0.054].
CNN: (ii) Q4 − Q1 0.008 [-0.032, 0.054]; (iii) selisih AUROC berlapis kuartil 0.041 [0.028, 0.054].

Aturan (ii) CI Q4 − Q1 *probe* di dalam ±0,03: **tidak**. Aturan (iii) batas bawah *probe* > 0: **ya**.

(iv) (keunggulan dengan jarak) − (keunggulan tanpa jarak): -0.001 [-0.002, 0.001]. Aturan CI di dalam ±0,03: **ya**.

Waktu jalan: 10.6 menit.

Salinan `fase_h_H5H6_B2000.log`:

### H5. Pasangan bersarang kedua: STEMI di dalam infark (penyimpangan P3)

STEMI lawan NSTEMI di dalam AMI (1423 / 2644): *probe* berlabel STEMI 0.830, berlabel AMI 0.769; selisih 0.061 [0.053, 0.069].

### H6. Titik-balik tinjauan label (penyimpangan P3)

| k pasangan ditukar | % EKG infark berubah label | AUROC (c) *probe* label tertukar | AUROC (c) *probe*-AMI | keunggulan |
| --- | --- | --- | --- | --- |
| 0 | 0.0 | 0.553 | 0.542 | +0.011 |
| 25 | 1.9 | 0.583 | 0.579 | +0.004 |
| 50 | 3.8 | 0.617 | 0.614 | +0.003 |
| 100 | 7.6 | 0.676 | 0.677 | -0.000 |
| 200 | 15.1 | 0.771 | 0.781 | -0.010 |
| 400 | 30.2 | 0.904 | 0.917 | -0.013 |

Waktu jalan: 2.2 menit.
