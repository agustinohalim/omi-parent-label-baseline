# Pra-daftar OMI fase G — komposisi STEMI dan uji "differ only" (13 November 2026)

> **TERKUNCI 13 November 2026** atas pilihan pengguna "Phase G + lower-bar venue": hanya dua pemeriksaan kritis panel 6,
> data yang sudah ada di disk, lalu pemilihan jurnal baru. Isi di atas bagian "Penyimpangan" tidak disunting lagi;
> perubahan masuk sebagai penyimpangan bertanggal sebelum run yang terdampak.

## Mengapa ada fase G

Panel 6 (`Telaah/2026-11-13-OMI-JE-4`, *J Electrocardiology*, Reject in current form, signifikansi 2). Dua kritis:
(a) keunggulan label oklusi +0,04 di dalam infark bisa berasal dari komposisi STEMI (OMI 63,1 % STEMI, infark tanpa
oklusi 46,8 %); nol permutasi F1 mengacak di seluruh infark sehingga ikut memutus kaitan STEMI. (b) "Differ only among
patients with infarction" tidak diuji: Tabel 3 tidak memuat selisih berpasangan untuk OMI lawan tanpa infark, dan
selisih infark lawan tanpa infark −0,017 [−0,020; −0,014] berselang di luar 0.

Ditulis **sesudah** hasil fase A–F (`Hasil_OMI_0.md` sampai `Hasil_OMI_10.md`) dan panel 6. Belum dihitung: semua
butir di bawah (selisih per STEMI/NSTEMI dari prediksi tersimpan belum pernah dihitung untuk *probe*-AMI dan CNN-AMI).
Semua butir **eksploratif**. Tidak ada unduhan baru. Keluaran `Hasil_OMI_11.md`; skrip `omi_fase_g.py` dikomit sebelum
dijalankan.

## Ukuran bersama

Analisis utama Chongqing (17.622 EKG). Prediksi tersimpan tiga penetapan lipatan: *probe*-OMI (`oof_m3a.npz`),
*probe*-AMI (`oof_m3a_ami.npz`), CNN-OMI (`oof_m2_utama.npz`), CNN-AMI (`oof_m2_ami.npz`). CI 95 % = bootstrap 2.000
bergugus pasien; selisih berpasangan dengan `beda_auc`. Benih bootstrap: G1 20261150, G2 20261151.

## G1. Komposisi STEMI

(i) Selisih AUROC label oklusi − label infark, untuk *probe* dan CNN, di dalam STEMI (OMI 715 lawan STEMI tanpa OMI
708) dan di dalam NSTEMI (417 lawan 804).

(ii) Nol permutasi berlapis: seperti F1 (*probe*, C = 0,001, lipatan 20261107 atas label teracak, 100 permutasi),
tetapi label OMI diacak **di dalam** tiap lapis tipe infark (STEMI, NSTEMI, AMI tanpa tipe), jumlah OMI per lapis
tetap; benih permutasi 1001–1100. Dicatat AUROC (c) terhadap label asli dan AUROC di dalam STEMI dan di dalam NSTEMI.

Aturan baca:
- Naskah menyatakan label oklusi membawa informasi **di luar tipe infark** hanya bila AUROC (c) label asli (0,643,
  F1) melebihi persentil ke-95 nol berlapis. Bila tidak, keunggulan +0,04 dilaporkan sebagai tidak terbedakan dari
  komposisi STEMI dan klaim keunggulan di dalam infark dihapus dari judul, abstrak, dan simpulan.
- Naskah menyatakan keunggulan di dalam NSTEMI hanya bila batas bawah CI selisih (i) di dalam NSTEMI > 0 untuk
  *probe*; sama untuk STEMI. Selisih CNN dilaporkan berdampingan.

## G2. Uji "differ only"

Selisih AUROC berpasangan label oklusi − label infark untuk OMI lawan tanpa infark (1.133 / 14.976), *probe* dan CNN,
ditambah baris yang sudah ada (OMI lawan semua, (c), infark lawan tanpa infark) dihitung ulang dengan benih G2.

Aturan baca: kata "only" (dan "equal" untuk perbandingan dengan tanpa infark) hanya dipakai bila CI selisih untuk OMI
lawan tanpa infark **dan** untuk infark lawan tanpa infark keduanya berada di dalam ±0,03 dan memuat 0. Bila salah satu
tidak memuat 0, judul dan simpulan tidak memakai "only" dan melaporkan setiap selisih dengan CI.

## Tidak dikerjakan di fase G

Batas atas bias inkorporasi dari tinjauan label (data tidak menyebut berapa label berubah), pengukur ST tervalidasi,
kontrol hanyut STAFF III, jaringan disetel di dalam infark, model fondasi kedua.

## Penyimpangan

**P1 (13 November 2026, sesudah G1–G2 di `Hasil_OMI_11.md`, sebelum G3 dijalankan).** Ditambah butir G3 karena dua
kalimat Pembahasan 4.3 draf 6 tidak punya angka di Hasil (temuan panel 6 "Discussion 4.3 rests on comparisons the
Results do not report"). Prediksi tersimpan yang sama, benih bootstrap 20261152, B = 2.000.

(i) AUROC skor *probe*-AMI dan CNN-AMI untuk setiap baris pasangan kelompok Tabel 4 draf 6 (OMI lawan tanpa infark;
infark tanpa oklusi lawan tanpa infark, juga STEMI, NSTEMI, dengan PCI, tanpa PCI, NSTEMI tanpa PCI), dengan selisih
berpasangan label oklusi − label infark. Aturan baca: kalimat "the infarction-trained probe did the same" hanya untuk
baris yang CI selisih *probe*-nya berada di dalam ±0,03; baris lain dilaporkan dengan selisih dan CI.

(ii) Selisih AUROC berpasangan *probe*-OMI − CNN-OMI untuk OMI lawan semua, (c), di dalam STEMI, di dalam NSTEMI.
Aturan baca: anak kalimat "outperformed the CNN overall but not among patients with infarction" hanya dipakai bila CI
selisih (c) memuat 0; bila batas bawah > 0, anak kalimat dihapus dan selisih dilaporkan.
