# Hasil OMI 0 — hitung ulang label data Chongqing (7 November 2026)

Sumber angka: keluaran `analysis/omi_hitung_label.py` atas `train.csv`/`test.csv` dari figshare
10.6084/m9.figshare.29925314 (CC0), diunduh 7 Nov 2026 ke `C:\Data\Chongqing_ACS\` (di luar repo;
ukuran `ECG_row_data.zip` 1.277.577.332 bita sama dengan API figshare; ketiga zip lolos `unzip -t`).
Tidak ada pemodelan. Teruskan tabel di bawah apa adanya; jangan diketik ulang.

## 0. Catatan pembacaan

- `gender = 1` dibaca sebagai laki-laki: 60,2 % di latih, cocok dengan "perempuan ±40 %" di makalah. ⬜
  kamus kolom resmi tidak ada di berkas.
- Hitungan agen 6 Nov (1.151 OMI; 727 STEMI-OMI; 423 NSTEMI-OMI; 139 multi-teritori; 96 tanpa segmen)
  **terkonfirmasi**. Selisih 1 yang dicatat agen = satu EKG OMI tanpa label STEMI/NSTEMI/UA (baris
  "bukan SKA" di bagian 3).
- AMI = 2.679, sedangkan STEMI + NSTEMI = 2.677 → 2 EKG AMI tanpa jenis SKA. ⬜ periksa barisnya.
- NSTEMI latih 1.235 di CSV vs 1.274 (teks) / 1.349 (Tabel 3) di makalah; STEMI 1.442 vs 1.437 (Tabel);
  UA 6.213 vs 5.592 (Tabel). Naskah memakai angka CSV dan mencatat selisihnya.
- 855 pasien punya > 1 EKG (maks 5) → validasi silang wajib dibagi per pasien.
- Teritori: LM; LAD = PLAD/MLAD/DLAD/DB; LCX = PLCX/MLCX/DLCX/OM; RCA = PRCA/MRCA/DRCA; hanya nilai 1
  (oklusi akut) yang dihitung, nilai 2 (CTO) tidak. Pengelompokan DB ke LAD dan OM ke LCX = keputusan
  asisten mengikuti anatomi standar, ⬜ dikonfirmasi pengguna.
- NSTEMI-OMI satu teritori: LAD 88, LCX 106, RCA 108, LM 1 → klaim pembuluh penyebab NSTEMI-OMI hanya
  ±100 per kelas; CI akan lebar (sesuai risiko 1 di `Kebaruan_OMI_2026-11-06.md`).

## 1. Ukuran berkas

| Berkas | EKG (baris) | Pasien unik | Kolom |
| --- | --- | --- | --- |
| train.csv | 17960 | 17018 | 28 |
| test.csv | 1995 | 1891 | 6 |

Pasien di latih dan uji sekaligus: 0. Rekaman `.dat` ganda di latih: 0.

## 2. Label biner di train.csv (nilai 1)

| Kolom | n = 1 | % EKG | nilai unik |
| --- | --- | --- | --- |
| AMI | 2679 | 14.92 | [0, 1] |
| OMI | 1151 | 6.41 | [0, 1] |
| STEMI | 1442 | 8.03 | [0, 1] |
| NSTEMI | 1235 | 6.88 | [0, 1] |
| UA | 6213 | 34.59 | [0, 1] |
| CTO | 957 | 5.33 | [0, 1] |
| PCI | 4541 | 25.28 | [0, 1] |
| VF_VT | 869 | 4.84 | [0, 1] |
| Paced | 338 | 1.88 | [0, 1] |
| Prior_PCI | 1323 | 7.37 | [0, 1] |

## 3. Silang OMI × jenis SKA (train.csv)

| Jenis | OMI = 0 | OMI = 1 | Jumlah |
| --- | --- | --- | --- |
| NSTEMI | 812 | 423 | 1235 |
| STEMI | 715 | 727 | 1442 |
| UA | 6213 | 0 | 6213 |
| bukan SKA | 9069 | 1 | 9070 |
| **Jumlah** | 16809 | 1151 | 17960 |

## 4. Pembuluh penyebab pada EKG OMI = 1 (train.csv)

Nilai segmen yang muncul: [0, 1, 2] (1 = oklusi akut, 2 = CTO menurut makalah).

| Kelompok | n EKG OMI |
| --- | --- |
| tanpa segmen akut | 96 |
| satu teritori | 916 |
| lebih dari satu teritori | 139 |
| satu teritori: LM | 5 |
| satu teritori: LAD | 347 |
| satu teritori: LCX | 209 |
| satu teritori: RCA | 355 |

Satu teritori, dipecah per jenis SKA:

| Jenis | LM | LAD | LCX | RCA |
| --- | --- | --- | --- | --- |
| STEMI | 4 | 258 | 103 | 247 |
| NSTEMI | 1 | 88 | 106 | 108 |
| UA | 0 | 0 | 0 | 0 |
| bukan SKA | 0 | 1 | 0 | 0 |

## 5. Demografi dan Time_Interval

| Berkas | usia median (IQR) | usia hilang | laki-laki (gender=1) % | Time_Interval median (IQR) |
| --- | --- | --- | --- | --- |
| train | 66 (57–73) | 0 | 60.21 | 1607 (438–3943) |
| test | 66 (58–73) | 0 | 60.35 | 1676 (492–3990) |

EKG per pasien (latih): maks 5, pasien dengan > 1 EKG: 855.
