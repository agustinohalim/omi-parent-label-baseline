# Hasil OMI 14 — fase H penyimpangan P5: skala label klinis, titik operasi, jarak tanpa penalti (13 November 2026)

> Pra-daftar `Prareg_OMI_H.md`, penyimpangan P5 (6b62cb2, dikomit sebelum dijalankan, sesudah panel 12
> `Telaah/2026-11-13-OMI-BPEX-6`); skrip `omi_fase_h.py --butir H8 --B 2000`, 2,5 menit CPU. Log
> `$OMI_DATA/fase_h_P5_B2000.log` (disalin di bawah tanpa baris FutureWarning sklearn soal `penalty=None`).
> Tidak ada unduhan, tidak ada pelatihan *embedding* atau CNN baru. Eksploratif.

## Bacaan menurut aturan yang dikunci

- **H8(i) — label oklusi di urutan ke-4 dari 7 label bersarang klinis; tiga label kontrol memperoleh lebih.** Masing-
  masing dinilai terhadap labelnya sendiri di antara 2.646 EKG infark, keunggulan *probe* berlabel itu atas *probe*
  berlabel AMI (lipatan 20261107, C 0,001): usia ≥ median **0,111** [0,099; 0,122] (rujukan 0,492), laki-laki **0,088**
  [0,079; 0,098] (0,536), STEMI (diagnosis pulang) **0,062** [0,054; 0,071] (0,768), **OMI 0,042** [0,032; 0,052]
  (0,601), VF/VT 0,036 [0,003; 0,069] (0,530), jarak ≤ median 0,014 [0,006; 0,022] (0,548), PCI 0,008 [0,000; 0,015]
  (0,527). Aturan: keunggulan oklusi **tidak** disebut "besar" (tiga label kontrol lebih besar); skala ini menjadi butir
  3 protokol; R17 disebut sebagai cek bahwa pelatihan ulang saja tak memberi keunggulan.
- **H8(ii) — titik operasi (deskriptif).** OMI lawan infark tanpa oklusi, tiga penetapan lipatan: spesifisitas 80 %,
  sensitivitas 0,329 lawan 0,276, selisih **0,053** [0,024; 0,081] = **23** [10; 35] EKG OMI tambahan per 1.000 EKG
  infark; spesifisitas 90 %, 0,187 lawan 0,140, selisih 0,047 [0,022; 0,072] = 20 [10; 31]. Prevalensi OMI di antara
  EKG infark 0,428.
- **H8(iii) — jarak tanpa penalti: aturan terpenuhi.** Tahap kedua tanpa penalti (logit skor + spline kubik
  log(1 + jarak), lima lipatan di dalam AMI): AUROC (c) 0,645 lawan 0,603, selisih **0,042** [0,033; 0,052]; batas
  bawah > 0: ya.

## Keluaran

```
# Fase H OMI — keluaran omi_fase_h.py (B = 2000, butir H8)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## H8. Skala label klinis, titik operasi, jarak tanpa penalti (penyimpangan P5)

### H8(i) Label bersarang klinis, masing-masing dinilai terhadap labelnya sendiri (lipatan 20261107, C 0,001)

| Label (AMI dan …) | positif / EKG AMI | AUROC *probe* berlabel itu | AUROC *probe*-AMI | keunggulan [95 % CI] |
| --- | --- | --- | --- | --- |
| PCI | 1404 / 2646 | 0.534 | 0.527 | 0.008 [0.000, 0.015] |
| VF/VT | 146 / 2646 | 0.566 | 0.530 | 0.036 [0.003, 0.069] |
| usia >= median AMI | 1373 / 2646 | 0.602 | 0.492 | 0.111 [0.099, 0.122] |
| laki-laki | 2065 / 2646 | 0.624 | 0.536 | 0.088 [0.079, 0.098] |
| dekat angiografi (<= median AMI) | 1323 / 2646 | 0.563 | 0.548 | 0.014 [0.006, 0.022] |
| STEMI | 1423 / 2646 | 0.831 | 0.768 | 0.062 [0.054, 0.071] |
| OMI (label oklusi) | 1133 / 2646 | 0.643 | 0.601 | 0.042 [0.032, 0.052] |

Urutan keunggulan: usia >= median AMI 0.111, laki-laki 0.088, STEMI 0.062, OMI (label oklusi) 0.042, VF/VT 0.036, dekat angiografi (<= median AMI) 0.014, PCI 0.008. Label oklusi di urutan 4 dari 7; label kontrol dengan keunggulan lebih besar: 3.

### H8(ii) Sensitivitas pada spesifisitas tetap, (c) OMI lawan infark tanpa oklusi (tiga penetapan lipatan)

| Spesifisitas | Se *probe*-OMI | Se *probe*-AMI | selisih [95 % CI] | tambahan OMI per 1.000 EKG infark [95 % CI] |
| --- | --- | --- | --- | --- |
| 80% | 0.329 | 0.276 | 0.053 [0.024, 0.081] | 23 [10, 35] |
| 90% | 0.187 | 0.140 | 0.047 [0.022, 0.072] | 20 [10, 31] |

Prevalensi OMI di antara EKG infark: 1133 / 2646 = 0.428.

### H8(iii) Jarak tanpa penalti: regresi tahap kedua di dalam AMI

AUROC (c) tahap kedua: label oklusi + spline jarak 0.645; label infark + spline jarak 0.603.
Selisih label oklusi − label infark, dengan jarak tanpa penalti: 0.042 [0.033, 0.052]. Aturan batas bawah > 0: **ya**.

Waktu jalan: 2.5 menit.
```
