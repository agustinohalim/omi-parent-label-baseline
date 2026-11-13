# Hasil OMI 8 — fase D, kelompok pembanding, label latih, dan uji eksternal STAFF III (13 November 2026)

> Pra-daftar `Prareg_OMI_D.md` (terkunci 86a4542); skrip `omi_fase_d.py` (komit 3f4d288, perbaikan pipa 93cfb91 dan
> 26b8a3b: pasien tanpa BC1 terbaca NaN; rencana segmen ditulis saat unduh agar venv-gpu tidak butuh `wfdb`; tidak
> ada perubahan analisis). B = 2.000, satu run penuh per bagian 13 Nov: D1+D2 (62,5 menit), D3 (3,3 menit). Log
> `$OMI_DATA/fase_d_D1D2_B2000.log` dan `fase_d_D3_B2000.log` (disalin di bawah). STAFF III (PhysioNet
> `staffiii` 1.0.0, ODC-By 1.0) diunduh selektif atas izin pengguna: metadata 1 MB, 196 potongan 10 s lewat
> byte-range, total 35 MB di `$STAFF3_DATA/`. Semua butir eksploratif terhadap pra-daftar 7 Nov.

## Bacaan menurut aturan yang ditetapkan sebelum run

- **D1 — bacaan "mengenali infark" bertahan, juga pada NSTEMI tanpa revaskularisasi.** M3a, kelompok uji lawan tanpa
  AMI (14.976): (b1) AMI tanpa OMI dengan STEMI (708) **0,911 [0,900; 0,921]**; (b2) dengan NSTEMI (804) **0,749
  [0,731; 0,765]**; (b3) PCI = 1 (765) 0,844; (b4) PCI = 0 (748) 0,805; (b5) NSTEMI dan PCI = 0 (412) **0,730
  [0,705; 0,752]**. Batas bawah (b2) dan (b5) ≥ 0,70: aturan pertama terpenuhi. M2: 0,894 / 0,731 / 0,830 / 0,786 /
  0,710. Ciri ST (M1) dan usia–jenis kelamin (M0) 0,56–0,65 di semua sel. Sebagian besar 0,825 datang dari STEMI tanpa
  label OMI (0,911, sama dengan OMI lawan tanpa AMI 0,912); pada NSTEMI skornya lebih rendah tetapi tetap di atas
  0,70.
- **D1 — tidak bergantung waktu atau jenis kelamin.** (b) M3a per kuartil Q1–Q4: 0,819 / 0,829 / 0,816 / 0,830
  (Q1 − Q4 = −0,011, di bawah 0,05). (a) 0,893–0,920; (c) 0,617–0,657. Laki-laki (b) 0,808, perempuan 0,846; (c)
  0,650 dan 0,621.
- **D2 — label OMI hampir tidak menambah di atas label infark.** *Probe* dilatih dengan sasaran AMI (C 10⁻³ di semua
  lipatan): OMI lawan semua **0,889 [0,881; 0,898]** lawan *probe*-OMI 0,888; selisih *probe*-OMI − *probe*-AMI
  **−0,002 [−0,005; 0,002]** (batas atas < 0,03: aturan terpenuhi). Untuk (c) OMI lawan AMI tanpa OMI *probe*-OMI lebih
  baik: 0,643 lawan 0,601, selisih +0,042 [0,033; 0,051]. Untuk AMI lawan tanpa AMI *probe*-AMI 0,879 lawan 0,862.
- **D3 — skor naik saat arteri disumbat balon (data eksternal, tanpa infark).** 98 pasien STAFF III (6 dibuang
  sebelum segmen: 5 sadapan bermasalah, 1 tanpa BC1; 0 dibuang karena mutu; penanda deflasi dari `.event` pada
  semua, selisih dari D0 + D1 0 s). *Probe*-OMI akhir (C 10⁻³): logit median baseline −3,381, akhir inflasi −1,860;
  rerata perubahan **+1,500 [1,198; 1,815]**; bagian pasien naik **0,867 [0,796; 0,929]**; AUROC akhir inflasi lawan
  baseline 0,762 [0,713; 0,811]; Wilcoxon p 1,9 × 10⁻¹³. Peluang: median 0,033 → 0,135, rerata perubahan +0,139.
  Batas bawah rerata perubahan > 0 dan bagian naik > 0,5: **aturan pertama terpenuhi** — judul dan simpulan tidak lagi
  menyatakan model "terutama mengenali infark"; klaim diperluas ke "membawa sinyal oklusi akut pada data eksternal".
- **D3 — sinyalnya tidak khas oklusi.** *Probe*-AMI naik serupa: +1,665 [1,346; 2,004], bagian naik 0,847, AUROC
  0,767. Selisih perubahan logit *probe*-OMI − *probe*-AMI −0,166 [−0,290; −0,043] (deskriptif): *probe* infark naik
  sedikit lebih banyak. Bacaan (aturan deskriptif): sinyal iskemia/cedera umum, bukan khas oklusi.
- **D3 deskriptif.** Per arteri (perubahan logit *probe*-OMI; bagian naik): LAD 32 pasien 1,643; 0,94 — RCA 44
  1,709; 0,89 — sirkumfleks 20 1,068; 0,80 — lainnya 2 −1,082; 0,00. Tanpa infark lama (65) 1,679; 0,91; dengan
  infark lama (33) 1,146; 0,79. Letak terhadap Chongqing (skor model akhir pada EKG latihnya): median baseline STAFF
  III di persentil 70,5 kelompok tanpa AMI, akhir inflasi di persentil 94,0; median Chongqing tanpa AMI −4,159, AMI
  tanpa OMI −2,127, OMI −1,087. Akhir inflasi STAFF III (−1,860) jatuh di antara AMI tanpa OMI dan OMI Chongqing.

## Metadata STAFF III (dibaca sebelum sinyal mana pun dinilai; juga di `Prareg_OMI_D.md`)

Laman PhysioNet `staffiii` 1.0.0: 104 pasien yang menjalani PTCA elektif dengan satu inflasi balon berkepanjangan,
Charleston Area Medical Center, 1995–96; 9 sadapan (V1–V6, I, II, III), 1.000 Hz; lisensi ODC-By 1.0. Spreadsheet
anotasi: 104 pasien dengan inflasi pertama, 103 dengan rekaman baseline cath lab; durasi inflasi pertama 69–595 s,
median 296 s; arteri RCA 47, LAD 32, sirkumfleks 21, diagonal 2, *main* 2; infark lama tercatat pada 35. Dari 98 yang
dianalisis: LAD 32, RCA 44, sirkumfleks 20, lainnya 2; infark lama 33.

## Batas yang perlu disebut

- Baseline (BC1) dan akhir inflasi berasal dari rekaman berbeda pada sesi yang sama (pasien telentang di cath lab,
  elektroda sama). Pra-daftar tidak memuat kontrol negatif (dua segmen tanpa iskemia dari rekaman berbeda), jadi
  sebagian kenaikan bisa berasal dari kondisi rekaman (kateter terpasang, kontras), bukan iskemia. Dukungan tidak
  langsung: kenaikan lebih kecil pada sirkumfleks (wilayah yang dikenal "diam" di EKG 12 sadapan) dan pada infark
  lama — pola yang sesuai dengan iskemia, tetapi deskriptif.
- Perangkat, filter, dan populasi STAFF III berbeda (1995–96, AS, PTCA elektif); baseline sudah di persentil 70
  kelompok tanpa AMI Chongqing, jadi kalibrasi mutlak tidak dibaca. Sadapan ekstremitas turunan dari I dan II.
- CNN M2 tidak dinilai di STAFF III (model akhir tidak disimpan).

## Keluaran (salinan log)

## D1. Kelompok pembanding dipecah (skor OMI kohort penuh)

Pembanding: tanpa AMI (n = 14976).

| Kelompok uji | n EKG uji | M0 | M1 | M2 | M3a |
| --- | --- | --- | --- | --- | --- |
| (b1) AMI tanpa OMI, STEMI | 708 | 0.618 [0.600, 0.637] | 0.561 [0.539, 0.583] | 0.894 [0.884, 0.905] | 0.911 [0.900, 0.921] |
| (b2) AMI tanpa OMI, NSTEMI | 804 | 0.625 [0.606, 0.643] | 0.652 [0.633, 0.672] | 0.731 [0.713, 0.747] | 0.749 [0.731, 0.765] |
| (b3) AMI tanpa OMI, PCI = 1 | 765 | 0.638 [0.620, 0.656] | 0.618 [0.597, 0.638] | 0.830 [0.815, 0.844] | 0.844 [0.829, 0.858] |
| (b4) AMI tanpa OMI, PCI = 0 | 748 | 0.605 [0.585, 0.623] | 0.600 [0.580, 0.621] | 0.786 [0.769, 0.802] | 0.805 [0.788, 0.821] |
| (b5) AMI tanpa OMI, NSTEMI dan PCI = 0 | 412 | 0.604 [0.577, 0.629] | 0.634 [0.608, 0.660] | 0.710 [0.686, 0.733] | 0.730 [0.705, 0.752] |
| (b) AMI tanpa OMI, semua | 1513 | 0.622 [0.608, 0.635] | 0.609 [0.594, 0.625] | 0.808 [0.795, 0.818] | 0.825 [0.813, 0.835] |

Per kuartil Time_Interval (batas P4) dan jenis kelamin, M2 dan M3a:

| Lapis | Pasangan | n pos / n neg | M2 | M3a |
| --- | --- | --- | --- | --- |
| kuartil Q1 | (a) OMI lawan tanpa AMI | 533 / 3261 | 0.890 [0.876, 0.903] | 0.916 [0.903, 0.928] |
| kuartil Q1 | (b) AMI tanpa OMI lawan tanpa AMI | 614 / 3261 | 0.804 [0.786, 0.821] | 0.819 [0.802, 0.837] |
| kuartil Q1 | (c) OMI lawan AMI tanpa OMI | 533 / 614 | 0.643 [0.617, 0.672] | 0.657 [0.627, 0.687] |
| kuartil Q2 | (a) OMI lawan tanpa AMI | 275 / 3702 | 0.890 [0.871, 0.908] | 0.893 [0.872, 0.914] |
| kuartil Q2 | (b) AMI tanpa OMI lawan tanpa AMI | 426 / 3702 | 0.801 [0.780, 0.822] | 0.829 [0.808, 0.850] |
| kuartil Q2 | (c) OMI lawan AMI tanpa OMI | 275 / 426 | 0.636 [0.599, 0.673] | 0.634 [0.591, 0.676] |
| kuartil Q3 | (a) OMI lawan tanpa AMI | 185 / 3966 | 0.884 [0.859, 0.906] | 0.917 [0.899, 0.935] |
| kuartil Q3 | (b) AMI tanpa OMI lawan tanpa AMI | 254 / 3966 | 0.801 [0.771, 0.830] | 0.816 [0.785, 0.844] |
| kuartil Q3 | (c) OMI lawan AMI tanpa OMI | 185 / 254 | 0.604 [0.559, 0.652] | 0.628 [0.580, 0.680] |
| kuartil Q4 | (a) OMI lawan tanpa AMI | 140 / 4047 | 0.886 [0.860, 0.910] | 0.920 [0.897, 0.940] |
| kuartil Q4 | (b) AMI tanpa OMI lawan tanpa AMI | 219 / 4047 | 0.825 [0.800, 0.851] | 0.830 [0.803, 0.858] |
| kuartil Q4 | (c) OMI lawan AMI tanpa OMI | 140 / 219 | 0.603 [0.549, 0.658] | 0.617 [0.561, 0.672] |
| laki-laki | (a) OMI lawan tanpa AMI | 886 / 8580 | 0.878 [0.868, 0.889] | 0.901 [0.891, 0.912] |
| laki-laki | (b) AMI tanpa OMI lawan tanpa AMI | 1179 / 8580 | 0.787 [0.774, 0.800] | 0.808 [0.794, 0.820] |
| laki-laki | (c) OMI lawan AMI tanpa OMI | 886 / 1179 | 0.635 [0.614, 0.657] | 0.650 [0.628, 0.675] |
| perempuan | (a) OMI lawan tanpa AMI | 247 / 6396 | 0.899 [0.880, 0.919] | 0.927 [0.912, 0.941] |
| perempuan | (b) AMI tanpa OMI lawan tanpa AMI | 334 / 6396 | 0.827 [0.804, 0.850] | 0.846 [0.825, 0.867] |
| perempuan | (c) OMI lawan AMI tanpa OMI | 247 / 334 | 0.618 [0.576, 0.659] | 0.621 [0.575, 0.664] |

## D2. Probe ECGFounder dengan sasaran AMI (prosedur fase A)

Latih: 15.6 menit. C terpilih: [0.001].

| Sasaran | n pos / n | probe-OMI | probe-AMI | selisih OMI − AMI |
| --- | --- | --- | --- | --- |
| OMI lawan semua | 1133 / 17622 | 0.888 [0.878, 0.896] | 0.889 [0.881, 0.898] | -0.002 [-0.005, 0.002] |
| (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.643 [0.623, 0.663] | 0.601 [0.580, 0.622] | 0.042 [0.033, 0.051] |
| AMI lawan tanpa AMI | 2646 / 17622 | 0.862 [0.855, 0.870] | 0.879 [0.872, 0.887] | -0.017 [-0.020, -0.014] |

Per benih AUROC probe-AMI untuk OMI lawan semua: 0.889, 0.889, 0.890.

Waktu jalan: 62.5 menit.

## D3. STAFF III: baseline cath lab lawan akhir inflasi balon

Pasangan tersegmen: 98. Mutu tidak ok (nilai konstan > 1 s): 0 pasien [], dibuang.

Sumber penanda deflasi: event: 98. Selisih event dari D0 + D1 terbesar: 0.0 s.

| Model | sasaran latih | C | n latih |
| --- | --- | --- | --- |
| probe-OMI | OMI | 0.001 | 17622 |
| probe-AMI | AMI | 0.001 | 17622 |

| Model | skala | median baseline | median akhir inflasi | rerata perubahan | bagian naik | AUROC akhir inflasi lawan baseline | Wilcoxon p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| probe-OMI | logit | -3.381 | -1.860 | 1.500 [1.198, 1.815] | 0.867 [0.796, 0.929] | 0.762 [0.713, 0.811] | 1.9e-13 |
| probe-OMI | peluang | 0.033 | 0.135 | 0.139 [0.102, 0.178] | 0.867 [0.796, 0.929] | 0.762 [0.713, 0.811] | 6.5e-12 |
| probe-AMI | logit | -2.087 | -0.486 | 1.665 [1.346, 2.004] | 0.847 [0.776, 0.918] | 0.767 [0.717, 0.817] | 4.7e-14 |
| probe-AMI | peluang | 0.110 | 0.381 | 0.236 [0.183, 0.288] | 0.847 [0.776, 0.918] | 0.767 [0.717, 0.817] | 1.4e-12 |

Selisih rerata perubahan logit probe-OMI − probe-AMI (berpasangan, deskriptif): -0.166 [-0.290, -0.043].

Deskriptif per arteri dan infark lama (logit, rerata perubahan; bagian naik):

| Lapis | n | probe-OMI | probe-AMI |
| --- | --- | --- | --- |
| arteri LAD | 32 | 1.643; 0.94 | 1.823; 0.88 |
| arteri RCA | 44 | 1.709; 0.89 | 1.830; 0.86 |
| arteri sirkumfleks | 20 | 1.068; 0.80 | 1.286; 0.85 |
| arteri lainnya | 2 | -1.082; 0.00 | -0.693; 0.00 |
| tanpa infark lama | 65 | 1.679; 0.91 | 1.800; 0.91 |
| dengan infark lama | 33 | 1.146; 0.79 | 1.399; 0.73 |

Letak skor STAFF III terhadap Chongqing (skor model akhir pada EKG latihnya sendiri, persentil di kelompok tanpa AMI; median kelompok Chongqing sebagai rujukan):

| Model | median STAFF baseline | median STAFF akhir inflasi | median CQ tanpa AMI | median CQ AMI tanpa OMI | median CQ OMI | persentil baseline | persentil akhir inflasi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| probe-OMI | -3.381 | -1.860 | -4.159 | -2.127 | -1.087 | 70.5 | 94.0 |
| probe-AMI | -2.087 | -0.486 | -3.028 | -0.458 | 0.077 | 74.9 | 95.4 |

Waktu jalan: 3.3 menit.
