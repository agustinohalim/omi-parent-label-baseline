# Hasil OMI 9 — fase E, kontrol di dalam rekaman, oklusi kronis, lapis NSTEMI, CNN berlabel AMI (13 November 2026)

> Pra-daftar `Prareg_OMI_E.md` (terkunci b19d4c1); skrip `omi_fase_e.py` (komit 6e58767), B = 2.000, satu run penuh
> per bagian 13 Nov: CNN berlabel AMI di GPU (11,0 menit), E1–E3 (24,6 menit), E4 (10,7 menit). Log
> `$OMI_DATA/fase_e_cnn_ami.log`, `fase_e_E1E3_B2000.log`, `fase_e_E4_B2000.log` (disalin di bawah). STAFF
> III: 98 potongan awal inflasi tambahan (17,6 MB, atas izin pengguna; total di `$STAFF3_DATA/` 53 MB). Semua
> butir eksploratif terhadap pra-daftar 7 Nov.

## Bacaan menurut aturan yang ditetapkan sebelum run

- **E1 — kenaikan terjadi di dalam rekaman yang sama.** *Probe*-OMI, akhir − awal inflasi (rekaman `BI1` yang sama,
  awal = 1–11 s sesudah penanda inflasi): rerata perubahan logit **+0,725 [0,463; 1,000]**, bagian naik **0,724
  [0,633; 0,816]** (98 pasien, semua potongan bermutu; penanda inflasi dari `.event` pada semua, selisih dari D0 0 s).
  Kedua batas bawah memenuhi aturan pertama: naskah menyatakan skor naik selama oklusi balon di dalam rekaman.
- **E1 — separuh kenaikan sudah ada di awal inflasi.** Awal inflasi − baseline +0,774 [0,530; 1,005] (bagian naik
  0,786), lebih dari separuh akhir − baseline +1,500 [1,208; 1,805]. Menurut aturan deskriptif: sebagian besar kenaikan
  sudah ada dalam 11 s pertama atau berasal dari perbedaan rekaman; data tidak memisahkan keduanya.
- **E1 — kedua *probe* pada skala yang sama.** Simpangan baku logit di Chongqing tanpa AMI: *probe*-OMI 1,288,
  *probe*-AMI 1,294. Selisih perubahan terstandar *probe*-OMI − *probe*-AMI: di dalam rekaman −0,026 [−0,116; 0,070]
  (memuat 0: "as much" boleh untuk perbandingan ini); awal − baseline −0,098 [−0,171; −0,022]; akhir − baseline −0,123
  [−0,218; −0,027] (tidak memuat 0: *probe*-AMI naik lebih banyak terhadap baseline). *Probe*-AMI di dalam rekaman
  +0,761 [0,489; 1,031], bagian naik 0,724.
- **E2 — oklusi kronis: batas bawah < 0,70.** Di 14.976 EKG tanpa AMI, CTO (946) lawan sisa: *probe*-OMI **0,686
  [0,666; 0,705]**, *probe*-AMI 0,695. Menurut aturan dilaporkan sebagai bukti bahwa skor membedakan kelainan akut dari
  oklusi kronis; catatan: 0,686 jauh di atas 0,5 dan di bawah (b) 0,825 dan OMI 0,912, jadi pemisahannya parsial.
  Deskriptif: Prior_PCI 0,585 / 0,589; UA 0,500 / 0,513; VF_VT 0,649 / 0,624.
- **E3 — NSTEMI tanpa PCI per lapis (M3a).** (b5) per kuartil Q1–Q4: 0,731 [0,695; 0,769] / 0,750 / 0,712 / 0,680
  [0,610; 0,749]; laki-laki 0,713, perempuan 0,744. M2: 0,726 / 0,704 / 0,692 / 0,667; 0,697 / 0,700. Q1 − Q4 (M3a)
  0,051. OMI lawan AMI tanpa OMI di dalam NSTEMI (M3a): semua 0,655, Q1 0,670, Q2 0,599, Q3 0,652, Q4 0,735;
  laki-laki 0,653, perempuan 0,667.
- **E4 — CNN berlabel AMI: pola sama dengan *probe*.** CNN-AMI untuk OMI lawan semua 0,863 [0,854; 0,872] lawan CNN-OMI
  0,867; selisih **+0,003 [−0,003; 0,010]** (batas atas < 0,03: "hampir tidak menambah" untuk pembanding ini). (c) OMI
  lawan AMI tanpa OMI: 0,631 lawan 0,591, selisih **+0,040 [0,027; 0,052]** (batas bawah > 0: "menambah sedikit di dalam
  infark"). AMI lawan tanpa AMI: CNN-AMI 0,853, CNN-OMI 0,843. AUROC per benih CNN-AMI untuk OMI 0,882 / 0,853 / 0,855.
- **E4 — *probe* (D2, angka sudah diketahui sebelum aturan ditulis):** OMI lawan semua −0,002 [−0,005; 0,002]
  ("hampir tidak menambah"); (c) +0,042 [0,033; 0,051] ("menambah sedikit di dalam infark"). Judul dan simpulan tidak
  lagi memakai "learn largely the same signal" (aturan E4).

## Batas yang perlu disebut

- Potongan awal inflasi (1–11 s) bukan bebas iskemia: perubahan EKG bisa muncul dalam detik pertama oklusi. Jadi (i)
  meremehkan kenaikan karena iskemia, dan (ii) mencampur iskemia awal dengan perbedaan rekaman.
- E2 memakai label CTO pada EKG tanpa AMI; usia oklusi kronis dan infark lama tidak tercatat.

## Keluaran (salinan log)

CNN berlabel AMI: 17622 EKG, AMI 2646, 20 epoch, 11.0 menit. AUROC AMI per benih: 0.874, 0.844, 0.843; OMI per benih: 0.882, 0.853, 0.855.

## E1. STAFF III: awal inflasi, akhir inflasi, baseline

Pasangan D3: 98 (mutu D3 tidak ok 0). Potongan awal: 98, mutu tidak ok 0. Sumber penanda inflasi: event: 98; selisih terbesar dari D0 0.0 s.

Pasien dengan ketiga potongan bermutu: 98.

probe-OMI: C 0.001; simpangan baku logit di Chongqing tanpa AMI 1.288.
probe-AMI: C 0.001; simpangan baku logit di Chongqing tanpa AMI 1.294.

| Model | Perbandingan | median dari → ke | rerata perubahan logit | bagian naik | rerata terstandar |
| --- | --- | --- | --- | --- | --- |
| probe-OMI | (i) akhir − awal inflasi (rekaman sama) | -2.451 → -1.860 | 0.725 [0.463, 1.000] | 0.724 [0.633, 0.816] | 0.563 [0.359, 0.776] |
| probe-OMI | (ii) awal inflasi − baseline | -3.381 → -2.451 | 0.774 [0.530, 1.005] | 0.786 [0.704, 0.867] | 0.601 [0.412, 0.780] |
| probe-OMI | (iii) akhir inflasi − baseline | -3.381 → -1.860 | 1.500 [1.208, 1.805] | 0.867 [0.796, 0.929] | 1.164 [0.937, 1.401] |
| probe-AMI | (i) akhir − awal inflasi (rekaman sama) | -1.282 → -0.486 | 0.761 [0.489, 1.031] | 0.724 [0.633, 0.806] | 0.589 [0.378, 0.797] |
| probe-AMI | (ii) awal inflasi − baseline | -2.087 → -1.282 | 0.904 [0.637, 1.155] | 0.796 [0.714, 0.867] | 0.699 [0.492, 0.893] |
| probe-AMI | (iii) akhir inflasi − baseline | -2.087 → -0.486 | 1.665 [1.354, 1.989] | 0.847 [0.765, 0.918] | 1.287 [1.047, 1.538] |

Selisih terstandar probe-OMI − probe-AMI (berpasangan):

- (i) akhir − awal inflasi (rekaman sama): -0.026 [-0.116, 0.070]
- (ii) awal inflasi − baseline: -0.098 [-0.171, -0.022]
- (iii) akhir inflasi − baseline: -0.123 [-0.218, -0.027]

## E2. Subkelompok di dalam tanpa AMI (skor kohort penuh)

| Subkelompok lawan sisa tanpa AMI | n subkelompok / n sisa | probe-OMI | probe-AMI |
| --- | --- | --- | --- |
| CTO | 946 / 14030 | 0.686 [0.666, 0.705] | 0.695 [0.675, 0.713] |
| Prior_PCI | 1122 / 13854 | 0.585 [0.567, 0.603] | 0.589 [0.571, 0.607] |
| UA | 6135 / 8841 | 0.500 [0.491, 0.510] | 0.513 [0.503, 0.523] |
| VF_VT | 673 / 14303 | 0.649 [0.630, 0.669] | 0.624 [0.604, 0.644] |

## E3. NSTEMI tanpa PCI dan OMI di dalam NSTEMI, per kuartil dan jenis kelamin

| Lapis | Pasangan | n pos / n neg | M2 | M3a |
| --- | --- | --- | --- | --- |
| semua | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 412 / 14976 | 0.710 [0.687, 0.733] | 0.730 [0.707, 0.752] |
| semua | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 417 / 804 | 0.625 [0.596, 0.654] | 0.655 [0.623, 0.686] |
| kuartil Q1 | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 176 / 3261 | 0.726 [0.692, 0.760] | 0.731 [0.695, 0.769] |
| kuartil Q1 | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 169 / 324 | 0.633 [0.584, 0.681] | 0.670 [0.620, 0.723] |
| kuartil Q2 | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 120 / 3702 | 0.704 [0.662, 0.744] | 0.750 [0.709, 0.787] |
| kuartil Q2 | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 122 / 244 | 0.631 [0.576, 0.685] | 0.599 [0.539, 0.661] |
| kuartil Q3 | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 68 / 3966 | 0.692 [0.627, 0.754] | 0.712 [0.646, 0.773] |
| kuartil Q3 | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 75 / 138 | 0.578 [0.505, 0.647] | 0.652 [0.577, 0.726] |
| kuartil Q4 | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 48 / 4047 | 0.667 [0.604, 0.732] | 0.680 [0.610, 0.749] |
| kuartil Q4 | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 51 / 98 | 0.657 [0.572, 0.735] | 0.735 [0.651, 0.812] |
| laki-laki | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 308 / 8580 | 0.697 [0.671, 0.723] | 0.713 [0.687, 0.741] |
| laki-laki | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 314 / 623 | 0.623 [0.589, 0.655] | 0.653 [0.614, 0.690] |
| perempuan | (b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI | 104 / 6396 | 0.700 [0.650, 0.747] | 0.744 [0.696, 0.787] |
| perempuan | OMI lawan AMI tanpa OMI, di dalam NSTEMI | 103 / 181 | 0.636 [0.574, 0.696] | 0.667 [0.604, 0.732] |

Waktu jalan: 24.6 menit.

## E4. CNN berlabel AMI lawan CNN berlabel OMI

| Sasaran | n pos / n | CNN-OMI | CNN-AMI | selisih CNN-OMI − CNN-AMI |
| --- | --- | --- | --- | --- |
| OMI lawan semua | 1133 / 17622 | 0.867 [0.857, 0.877] | 0.863 [0.854, 0.872] | 0.003 [-0.003, 0.010] |
| (c) OMI lawan AMI tanpa OMI | 1133 / 2646 | 0.631 [0.612, 0.650] | 0.591 [0.572, 0.610] | 0.040 [0.027, 0.052] |
| AMI lawan tanpa AMI | 2646 / 17622 | 0.843 [0.836, 0.851] | 0.853 [0.846, 0.860] | -0.010 [-0.015, -0.005] |

Waktu jalan: 10.7 menit.
