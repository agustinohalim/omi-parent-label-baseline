# Hasil OMI 13 — fase H penyimpangan P4: interval rujukan induk dan sebaran keunggulan label teracak (13 November 2026)

> Pra-daftar `Prareg_OMI_H.md`, penyimpangan P4 (a7b806a, dikomit sebelum dijalankan, sesudah panel 11
> `Telaah/2026-11-13-OMI-BPEX-5`); skrip `omi_fase_h.py --butir H7 --B 2000`, 25,2 menit CPU. Log
> `$OMI_DATA/fase_h_P4_B2000.log` (disalin di bawah tanpa 100 baris kemajuan per label); keunggulan per label
> di `$OMI_DATA/perm_h7.csv`. Tidak ada unduhan. Eksploratif.

## Bacaan menurut aturan yang dikunci

- **H7(i) — interval rujukan induk (deskriptif, bootstrap 2.000 bergugus pasien, benih 20261169).** *Probe* berlabel
  AMI untuk (c) OMI lawan infark tanpa oklusi **0,601 [0,581; 0,622]**, CNN 0,591 [0,573; 0,610]; di dalam STEMI
  *probe* 0,532 [0,502; 0,560], CNN 0,550 [0,524; 0,575]; di dalam NSTEMI *probe* 0,612 [0,580; 0,645], CNN 0,581
  [0,554; 0,608]; *probe* berlabel STEMI (diagnosis pulang) untuk (c) 0,611 [0,590; 0,633]; pasangan kedua (STEMI lawan
  NSTEMI di dalam AMI) *probe* berlabel AMI 0,769 [0,751; 0,787]. Titik sama dengan tabel utama.
- **H7(ii) — sebaran keunggulan label teracak, aturan R17 terpenuhi.** Ke-100 label acak berlapis tipe infark G1
  dibangkitkan ulang dari benihnya; setiap *probe* yang dilatih ulang mereproduksi `auc_c` di `perm_g1.csv` (selisih
  < 10⁻⁹, tidak ada BERHENTI). Keunggulan *probe* berlabel-acak atas *probe* berlabel AMI, keduanya dinilai terhadap
  label acak sendiri: rerata **0,0013**, SB 0,0047, persentil 2,5/50/95/97,5 −0,0077 / 0,0020 / **0,0084** / 0,0089,
  maksimum 0,0116. Keunggulan label oklusi pada lipatan dan C yang sama: **0,0422** (0,6431 − 0,6010), di atas
  ke-100 (0 dari 100 ≥). Aturan > p95: **ya** — label oklusi memperoleh lebih dari yang diperoleh subset acak
  bersarang dengan komposisi sama terhadap labelnya sendiri.
- Catatan: satu label teracak H6 k = 0 (benih 20261168, +0,011) berada di ujung atas sebaran ini (sekitar maksimum);
  angka itu tidak dipakai lagi sebagai skala.

## Keluaran

```
# Fase H OMI — keluaran omi_fase_h.py (B = 2000, butir H7)

Analisis utama: 17622 EKG, OMI 1133, AMI 2646.

## H7. Interval rujukan dan sebaran keunggulan nol (penyimpangan P4)

### H7(i) Rujukan induk dengan interval (bootstrap bergugus pasien, benih 20261169)

| Rujukan | Sasaran | n pos / n | AUROC [95 % CI] |
| --- | --- | --- | --- |
| *probe* berlabel AMI | (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.601 [0.581, 0.622] |
| CNN berlabel AMI | (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.591 [0.573, 0.610] |
| *probe* berlabel AMI | di dalam STEMI | 715 / 1423 | 0.532 [0.502, 0.560] |
| CNN berlabel AMI | di dalam STEMI | 715 / 1423 | 0.550 [0.524, 0.575] |
| *probe* berlabel AMI | di dalam NSTEMI | 417 / 1221 | 0.612 [0.580, 0.645] |
| CNN berlabel AMI | di dalam NSTEMI | 417 / 1221 | 0.581 [0.554, 0.608] |
| *probe* berlabel STEMI | (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.611 [0.590, 0.633] |
| *probe* berlabel AMI | STEMI lawan NSTEMI di dalam AMI (pasangan kedua) | 1423 / 2644 | 0.769 [0.751, 0.787] |

### H7(ii) Keunggulan nol pada label acak sendiri (lipatan 20261107, C 0,001)

Label oklusi pada lipatan dan C yang sama: AUROC (c) 0.6431 − 0.6010 = keunggulan 0.0422.


Nol: 100 label. Keunggulan rerata 0.0013, SB 0.0047, persentil 2,5/50/95/97,5 -0.0077 / 0.0020 / 0.0084 / 0.0089, maksimum 0.0116. AUROC *probe* berlabel-acak terhadap labelnya sendiri: rerata 0.5431; *probe* berlabel AMI terhadap label acak: rerata 0.5417.
Keunggulan label oklusi 0.0422: persentil ke-100 (0 dari 100 ≥). Aturan > p95: **ya**.

Waktu jalan: 25.2 menit.
```
