# Pra-daftar OMI fase C — uji ukur dan latih ulang di dalam infark (13 November 2026)

> **TERKUNCI 13 November 2026** atas jawaban "go" pengguna terhadap usulan fase C (lima butir) sesudah panel 2.
> Isi di atas bagian "Penyimpangan" tidak disunting lagi; perubahan masuk sebagai penyimpangan bertanggal sebelum run
> yang terdampak.

## Mengapa ada fase C

Panel 2 (`Telaah/2026-11-13-OMI-JE`, *J Electrocardiology*, NOT READY) memberi satu temuan kritis konsensus (empat
peran): aturan kriteria STEMI otomatis K2 hanya positif pada 21,8 % EKG OMI padahal 63,1 % EKG OMI berdiagnosis STEMI
pulang, dan ciri ST di kuartil waktu terpendek kalah dari usia dan jenis kelamin; jadi pengukuran titik J/ST mungkin
gagal, bukan EKG-nya. Mayor konsensus lain: (a) klaim "model mengenali infark" belum diuji langsung (minta tiga AUROC
berpasangan); (b) AUROC di dalam AMI berasal dari model kohort penuh yang tidak pernah dilatih membedakan oklusi dari
infark tanpa oklusi; (c) "satu dari lima EKG berisiko rendah adalah OMI" memakai prediksi kohort penuh yang terkalibrasi
pada prevalensi 6,4 %; (d) Tabel 1 memuat EKG Paced dan tidak dipecah menurut kelompok.

Ditulis **sesudah** hasil fase A dan B diketahui (`Hasil_OMI_0.md` sampai `Hasil_OMI_6.md`) dan sesudah membaca
laporan panel 2. Belum ada yang dihitung untuk butir di bawah: kesepakatan aturan K2 dengan diagnosis STEMI, AUROC
berpasangan, model yang dilatih di dalam AMI atau STEMI, jumlah EKG di bawah ambang untuk model NSTEMI yang dilatih
ulang, dan karakteristik per kelompok. Semua butir **eksploratif** terhadap pra-daftar 7 Nov.

Tidak ada pembacaan EKG oleh manusia di fase C (pengguna belum menyediakan pembaca); butir C1 hanya menguji apakah
aturan otomatis mereproduksi diagnosis klinis, bukan apakah titik J benar.

## Ukuran bersama

Seperti fase A dan B: analisis utama (tanpa Paced, 17.622 EKG); taksiran titik = rata-rata metrik per benih lipatan
(20261107–09); CI 95 % = bootstrap 2.000 bergugus pasien (`ringkas`, `metrik`, `beda_auc` dari `omi_m01.py` dan
`omi_konstruk.py`); satu benih bootstrap per butir. Skrip `omi_fase_c.py`; keluaran `Hasil_OMI_7.md`.

## C1. Apakah aturan otomatis mereproduksi diagnosis STEMI? (utama fase C)

Aturan K2 dihitung ulang persis (fungsi yang sama; jumlah positif harus 2.111, diperiksa `assert`). Ukuran:
- sensitivitas dan spesifisitas aturan untuk label `STEMI` (diagnosis pulang) pada analisis utama;
- sensitivitas aturan untuk `STEMI` per kuartil `Time_Interval` (batas P4), dengan n;
- varian titik ukur: aturan yang sama dengan amplitudo J + 60 ms (`st60_*` dari `ciri_st_train.csv`, ciri M1) di tempat
  titik J; sensitivitas dan spesifisitas untuk `STEMI` dan untuk `OMI`;
- sebaran, di EKG `STEMI = 1` dengan deteksi ok, "elevasi pasangan terbesar" = maksimum atas pasangan bersebelahan dari
  minimum elevasi kedua sadapan dikurangi ambangnya (mV): median dan IQR, dan bagian yang ≥ 0.

Tanpa bootstrap (deskriptif; n disebut).

Aturan baca, ditetapkan sekarang:
- Bila sensitivitas aturan untuk `STEMI` di kuartil Q1 **≥ 0,60**, perbandingan dengan kriteria STEMI (Tabel 5,
  *highlight* 4) tetap sebagai hasil, dengan angka C1 dilaporkan di sampingnya.
- Bila **< 0,60**, aturan otomatis dinyatakan tidak mereproduksi diagnosis klinis: angka 21,8 % dan perbandingan model
  dengan kriteria dikeluarkan dari *highlights*, abstrak, dan simpulan; di Hasil dilaporkan sebagai uji pipa ukur
  (kesepakatan dengan diagnosis STEMI) dan di Pembahasan disebut bahwa perbandingan dengan kriteria STEMI tidak dapat
  dibuat dengan pipa ini. Klaim tentang lemahnya ciri ST (model M1) dibatasi ke "implementasi ini" dengan alasan C1.

## C2. Tiga AUROC berpasangan

Kelompok: OMI (1.133), AMI tanpa OMI (`AMI = 1`, `OMI = 0`; 1.513), tanpa AMI (`AMI = 0`; 14.976). Untuk skor OMI tiap
model (M0, M1, M2, M3a; prediksi kohort penuh): AUROC (a) OMI lawan tanpa AMI, (b) AMI tanpa OMI lawan tanpa AMI,
(c) OMI lawan AMI tanpa OMI (= K1a). Benih bootstrap 20261120.

Aturan baca: model dibaca "memberi skor tinggi pada infark tanpa oklusi" bila batas bawah CI (b) untuk M3a ≥ 0,70.
Perbandingan (a) dan (c) deskriptif.

## C3. Latih ulang di dalam AMI dan di dalam STEMI

Di subhimpunan `AMI = 1` dan `STEMI = 1` (sasaran `OMI`), dilatih ulang dengan prosedur fase A apa adanya
(`lipatan`, `oof`, `pilih_C` dari `omi_m01.py`; benih lipatan 20261107–09): usia–jenis kelamin (C = 1), ciri ST
(24 ciri, C dipilih), dan *probe* ECGFounder (*embedding* tersimpan, C dipilih). CNN tidak dilatih ulang (butuh GPU).
Ukuran: AUROC, AUPRC, Brier, Se@Sp90, slope, intercept (`metrik`); selisih AUROC *probe* latih ulang − *probe* kohort
penuh dan *probe* latih ulang − ciri ST latih ulang. Benih bootstrap 20261121.

Aturan baca: bila batas bawah CI AUROC *probe* latih ulang di dalam AMI ≥ 0,70, abstrak menyebut sinyal oklusi di dalam
infark "sedang bila model dilatih di dalam infark"; bila tidak, bacaan "lemah" tetap.

## C4. Model NSTEMI yang dilatih ulang (pra-daftar asli): EKG di bawah ambang

Prediksi M3a yang dilatih ulang di NSTEMI (`oof_m3a.npz`, kunci `nstemi_*`; tanpa bobot kelas). Pada ambang 1, 2, 5,
10, 15, 20, 30, 40 %: net benefit, "obati semua", selisih M3a − obati semua dengan CI, jumlah EKG di bawah ambang dan
OMI di antaranya (rata-rata tiga benih, dibulatkan). Juga, tanpa CI, rentang ambang 1–60 % (langkah 1 %) tempat net
benefit rata-rata benih melampaui "obati semua" dan nol. Benih bootstrap 20261122. M2 dan M1 tidak (M1 tidak disimpan;
M2 dilatih dengan bobot kelas dan lipatan NSTEMI-nya tidak dibangun ulang di fase C).

## C5. Karakteristik per kelompok (Tabel 1 baru)

Analisis utama per kelompok OMI / AMI tanpa OMI / tanpa AMI: n EKG, n pasien, usia median (IQR), laki-laki (`gender = 1`)
%, `Time_Interval` median (IQR), jumlah `STEMI`, `NSTEMI`, `UA`, `Prior_PCI`, `VF_VT`, `PCI`, `CTO`; juga jumlah EKG
`AMI = 1` tanpa `STEMI` maupun `NSTEMI` dan EKG dengan keduanya. Deskriptif, tanpa uji.

## Tidak dikerjakan di fase C

Pembacaan titik J oleh manusia, CNN dilatih ulang atau disetel, model fondasi kedua, label OMI versi paradigma luas
(tidak tersedia di berkas).

## Penyimpangan

(belum ada)
