# Pra-daftar OMI fase B — uji konstruk (12 November 2026)

> **TERKUNCI 12 November 2026** atas jawaban "go" pengguna terhadap usulan "bingkai ulang", yang menyebut bahwa
> pra-daftar tambahan ditulis dan dikunci sebelum analisis dijalankan. Isi di atas bagian "Penyimpangan" tidak
> disunting lagi; perubahan masuk sebagai penyimpangan bertanggal sebelum run yang terdampak.

## Mengapa ada fase B

Panel 1 (`Telaah/2026-11-12-OMI-JE`, *J Electrocardiology*, NOT READY) menilai kritis bahwa AUROC utama mungkin
mengukur ada tidaknya infark miokard, bukan oklusi: di analisis utama (tanpa Paced) semua 1.133 EKG OMI berlabel
`AMI = 1`, sedangkan bukan-OMI berisi 1.513 EKG `AMI = 1` dan 14.976 EKG `AMI = 0`. Skor yang hanya sama dengan
`AMI` sudah memberi AUROC ≈ 0,954 untuk OMI. Panel juga menilai bahwa keunggulan kalibrasi M3a atas M2 berasal dari
bobot kelas M2, dan bahwa hasil NSTEMI "tanpa manfaat bersih" sebagian besar ditentukan oleh prevalensi 34 %
terhadap ambang 1–10 %.

Ditulis **sesudah** hasil utama dan sekunder diketahui (`Hasil_OMI_1.md` sampai `Hasil_OMI_5.md`) dan sesudah
membaca hitungan label per kolom (`AMI`, `STEMI`, `NSTEMI`, `UA` terhadap `OMI`), yang juga ada di Tabel 1 naskah.
Belum ada prediksi model yang dinilai di dalam AMI, di dalam STEMI, atau dengan koreksi bobot kelas. Semua analisis
fase B **eksploratif terhadap pra-daftar 7 Nov**; hasil pra-daftar asli tetap dilaporkan apa adanya.

Prinsip pembingkaian, ditetapkan sekarang agar tidak bergantung pada hasil: naskah dibingkai ulang sebagai
"apa yang diukur sasaran OMI pada data terbuka ini", **apa pun hasil K1**. Tidak ada model baru yang dilatih;
semua dari prediksi out-of-fold yang tersimpan (M0, M1, M2, M3a; lipatan, benih 20261107–09) dan dari denyut median.

## Ukuran bersama

Seperti pra-daftar asli dan P1/P2: taksiran titik = rata-rata metrik per benih; CI 95 % = bootstrap 2.000 bergugus
pasien, tiap ulangan menghitung metrik per benih pada pasien yang sama lalu merata-ratakannya (`ringkas` di
`omi_m01.py`); kalibrasi dengan Newton teredam P2. Subhimpunan diambil dari analisis utama (tanpa Paced, 17.622 EKG)
**tanpa latih ulang**: prediksi model kohort penuh dinilai di dalam subhimpunan. Skrip `omi_konstruk.py`, satu benih
bootstrap per butir (di bawah). Keluaran `Hasil_OMI_6.md`.

## K1. Oklusi di luar infark (utama fase B)

Subhimpunan (sasaran = `OMI`):

| Kode | Subhimpunan | Perkiraan n EKG / OMI |
|---|---|---|
| K1a | `AMI = 1` | 2.646 / 1.133 |
| K1b | `STEMI = 1` | 1.423 / 715 |
| K1c | `NSTEMI = 1` | 1.221 / 417 |
| K1d | `STEMI = 0` (semua bukan-STEMI) | 16.199 / 418 |

Per subhimpunan dan model (M0, M1, M2, M3a): AUROC, AUPRC, Se@Sp90, slope, intercept, dan prevalensi; selisih AUROC
M3a − M2 dengan CI bootstrap. Juga AUROC skor OMI tiap model untuk sasaran `AMI` pada semua EKG (seberapa jauh skor
itu pendeteksi infark). Benih bootstrap 20261115.

Titik rujukan tanpa model (label klinis yang **tidak** tersedia saat EKG dibaca; disebut rujukan, bukan pembanding):
`AMI` dan `STEMI` (diagnosis pulang) sebagai skor biner untuk `OMI` — sensitivitas, spesifisitas, AUROC — pada semua
EKG dan, untuk `STEMI`, di dalam `AMI = 1`.

Aturan baca, ditetapkan sekarang:
- "Sinyal oklusi di luar infark" ada bila batas bawah CI AUROC M3a di K1a > 0,5. Besarnya dibaca deskriptif:
  ≥ 0,70 sedang, < 0,70 lemah.
- Klaim bahwa M3a lebih baik dari M2 dalam mendeteksi oklusi hanya bila CI selisih K1a tidak memuat 0.
- Bila K1a lemah, judul, abstrak, dan simpulan tidak menyebut "detecting acute coronary occlusion" sebagai
  kemampuan model; AUROC 0,888 dilaporkan sebagai gabungan infark dan oklusi.

## K2. Aturan kriteria STEMI otomatis dari denyut median

Amplitudo ST **di titik J** relatif terhadap garis PR, dengan deteksi J dan garis PR P1 apa adanya (fungsi
`deteksi` di `omi_ciri_st.py`), 12 sadapan. Aturan Fourth Universal Definition of Myocardial Infarction (Thygesen
dkk., 2018; rujukan dicek ke Crossref sebelum dikutip): elevasi ST di titik J pada ≥ 2 sadapan bersebelahan,
≥ 0,1 mV di semua sadapan kecuali V2–V3; di V2–V3 ≥ 0,2 mV untuk laki-laki ≥ 40 tahun, ≥ 0,25 mV laki-laki < 40
tahun, ≥ 0,15 mV perempuan (`gender = 1` dibaca laki-laki, seperti `Hasil_OMI_0.md`). Pasangan bersebelahan:
dua sadapan mana pun di dalam {II, III, aVF}, pasangan {I, aVL}, dan (V*k*, V*k*+1) untuk *k* = 1–5. Kata "baru"
dan kriteria depresi ST tidak dinilai (tanpa EKG pembanding). EKG dengan deteksi gagal (status P1 ≠ ok) dihitung
negatif dan jumlahnya dilaporkan.

Ukuran: sensitivitas dan spesifisitas aturan untuk `OMI` pada analisis utama, di K1a, dan di K1c; lalu
sensitivitas M2 dan M3a pada spesifisitas yang sama dengan aturan di himpunan yang sama (ambang = kuantil skor
bukan-OMI per benih). Benih bootstrap 20261116.

## K3. EKG dekat angiografi

Kuartil `Time_Interval` sama dengan P4 butir 2 (`pd.qcut` atas analisis utama yang punya nilai). Per kuartil:
AUROC M1, M2, M3a di dalam `AMI = 1` (K1a per kuartil), dengan n EKG dan n OMI. Untuk kuartil terpendek (Q1):
semua ukuran bagian "Ukuran bersama" untuk sasaran utama. Benih bootstrap 20261117. Deskriptif, tanpa uji
heterogenitas.

## K4. M2 dengan koreksi bobot kelas

M2 dilatih dengan `pos_weight = (1 − p)/p`, *p* = prevalensi lipatan latih. Koreksi analitik tanpa pencocokan pada
data uji: logit terkoreksi = logit(*p*̂) − log((1 − *p*)/*p*), *p* dari lipatan latih tiap EKG (lipatan dibangun
ulang dengan `lipatan` dan benih yang sama). Dilaporkan untuk M2 mentah, M2 terkoreksi, dan M3a: Brier, slope,
intercept, net benefit pada 1, 2, 5, 10 %, dan selisih net benefit M3a − M2 terkoreksi dengan CI bootstrap
(benih 20261118). AUROC tidak berubah oleh koreksi ini dan hanya dicetak sebagai pemeriksaan.

## K5. Manfaat bersih di NSTEMI dan di AMI, rentang ambang penuh

Prediksi kohort penuh (bukan model yang dilatih ulang di NSTEMI) di K1c dan K1a: net benefit M2 terkoreksi dan M3a
pada ambang 1, 2, 5, 10, 15, 20, 30, 40 %, net benefit "obati semua", jumlah EKG dengan prediksi di bawah tiap
ambang dan jumlah OMI di antaranya. Benih bootstrap 20261119. Dibaca: pada ambang mana model mulai melampaui
"obati semua"; tidak ada ambang yang dipilih sebagai ambang klinis.

## Tidak dikerjakan di fase B

Pelatihan ulang M2 dengan banyak benih per lipatan atau tanpa bobot kelas (butuh GPU), ECG-FM, dan model yang
dilatih untuk `AMI` lalu dinilai untuk `OMI`. Dapat ditambahkan lewat penyimpangan bertanggal sebelum dijalankan.

## Penyimpangan

(belum ada)
