# Pra-daftar OMI fase H — pembanding berlabel STEMI dan label kontrol-negatif (13 November 2026)

> **TERKUNCI 13 November 2026** atas pilihan pengguna "Fase H + draf 8" sesudah panel 7. Isi di atas bagian
> "Penyimpangan" tidak disunting lagi; perubahan masuk sebagai penyimpangan bertanggal sebelum run yang terdampak.

## Mengapa ada fase H

Panel 7 (`Telaah/2026-11-13-OMI-BPEX`, *Biomedical Physics & Engineering Express*): NOT READY, Reject in current form,
editor send_to_review, signifikansi 3. Dua mayor yang hanya bisa dijawab dengan analisis:
(a) perbandingan yang diperdebatkan literatur OMI — label oklusi lawan model berlabel STEMI — belum dijalankan padahal
data memuat tanda STEMI; klaim "not the STEMI pattern under another name" hanya bersandar pada nol berlapis;
(b) nol permutasi hanya menyingkirkan "OMI adalah subset acak infark"; subset klinis lain yang berkaitan dengan
keparahan atau akuitas (PCI, VF/VT, usia, jarak ke angiografi) bisa juga mengalahkannya.

Ditulis **sesudah** fase A–G (`Hasil_OMI_0.md` sampai `Hasil_OMI_11.md`) dan panel 7. Belum dihitung: semua butir di
bawah. Semua butir **eksploratif**. Tidak ada unduhan baru. Keluaran `Hasil_OMI_12.md`; skrip `omi_fase_h.py` dikomit
sebelum dijalankan.

## H1. Pembanding berlabel STEMI

*Probe* ECGFounder dengan sasaran STEMI (tanda diagnosis pulang), prosedur yang sama dengan *probe*-AMI fase D
(`oof(E, y, g, benih, True)`: C dari CV dalam, tiga penetapan lipatan 20261107–09), disimpan `oof_m3a_stemi.npz`.
Skornya dinilai untuk OMI. Selisih AUROC berpasangan label oklusi − label STEMI (*probe*-OMI dari `oof_m3a.npz`)
untuk: OMI lawan semua; (c) OMI lawan infark tanpa oklusi; di dalam NSTEMI (OMI lawan NSTEMI tanpa OMI). Di dalam
STEMI label STEMI tetap, sehingga baris itu deskriptif saja. Bootstrap 2.000 bergugus pasien, benih 20261160.

Aturan baca: naskah menyatakan label oklusi mengajarkan sesuatu **di luar pola STEMI** hanya bila batas bawah CI
selisih (c) label oklusi − label STEMI > 0. Bila tidak, kalimat "not the STEMI pattern under another name" dihapus dan
naskah melaporkan bahwa di dalam infark label oklusi tidak terbedakan dari model berlabel STEMI.

## H2. Label kontrol-negatif di dalam infark

Seperti nol F1 (*probe*, C tetap 0,001, satu penetapan lipatan 20261107), tetapi label latih bukan OMI teracak
melainkan subset infark yang ditentukan secara klinis: label = 1 bila AMI dan syarat berikut, 0 selainnya (EKG tanpa
AMI selalu 0):

1. PCI = 1;
2. VF_VT = 1;
3. usia ≥ median usia EKG ber-AMI;
4. laki-laki (gender = 1);
5. Time_Interval ≤ median Time_Interval EKG ber-AMI (dekat angiografi; proksi akuitas);
6. STEMI = 1.

Setiap *probe* kontrol dinilai dengan AUROC (c) terhadap label OMI asli, dan dibandingkan dengan *probe* berlabel OMI
asli pada lipatan dan C yang sama (0,643, F1): selisih berpasangan asli − kontrol, bootstrap 2.000 bergugus pasien,
benih 20261161. Dicatat juga apakah AUROC kontrol melebihi persentil ke-95 nol berlapis G1 (0,609).

Aturan baca: naskah menyatakan keunggulan **khas label oklusi di antara subset klinis yang diuji** hanya bila batas
bawah CI selisih asli − kontrol > 0 untuk setiap kontrol. Kontrol yang tidak memenuhinya disebut namanya, dan klaim
dibatasi: nol permutasi tidak lagi disebut sebagai bukti informasi khas oklusi, hanya sebagai pemeriksaan bahwa label
bukan subset acak.

## Tidak dikerjakan di fase H

Definisi label dari laporan angiografi saja (berkas tidak memuat label sebelum tinjauan), kontrol hanyut STAFF III,
waktu awitan gejala (tidak ada di data), model fondasi kedua, CNN pada label kontrol.

## Penyimpangan

**P1 (13 November 2026, sebelum H3 dijalankan; H1 dan H2 belum keluar).** Ditambah butir H3 untuk mayor panel 7
"time course and reperfusion are an uncontrolled alternative explanation": jarak EKG ke angiografi (proksi tahap
penyakit; OMI median 7,9 jam, infark tanpa oklusi 10,5 jam) bisa menjelaskan sebagian keunggulan label oklusi.

- H3(i): AUROC jarak saja untuk (c) OMI lawan infark tanpa oklusi, skor = −Time_Interval (lebih dekat = lebih
  tinggi, arah ditetapkan di sini), bootstrap 2.000 bergugus pasien, benih 20261162. Deskriptif.
- H3(ii): *probe* berlabel OMI dan berlabel AMI dilatih ulang dengan fitur tambahan log(1 + Time_Interval) di samping
  *embedding* (pipa yang sama, C tetap 0,001, satu penetapan lipatan 20261107), skor dinilai untuk (c). Selisih
  berpasangan label oklusi − label infark, bootstrap 2.000, benih 20261163. Sebagai rujukan, pasangan yang sama tanpa
  fitur jarak pada lipatan dan C yang sama juga dilaporkan.

Aturan baca: naskah menyatakan keunggulan **tidak dijelaskan oleh jarak ke angiografi** hanya bila batas bawah CI
selisih H3(ii) > 0. Bila tidak, naskah menyatakan bahwa keunggulan tidak terbedakan sesudah jarak dimasukkan. Apa pun
hasilnya, tahap penyakit dan reperfusi tetap disebut di keterbatasan sebagai penjelasan pesaing yang tidak
disingkirkan desain (waktu awitan gejala tidak ada di data).

**P2 (13 November 2026, sesudah panel 8 `Telaah/2026-11-13-OMI-BPEX-2`, sebelum H4 dijalankan; H1–H3 sudah
keluar di `Hasil_OMI_12.md`).** Pengguna memilih "Draft 9 + panel 9". Ditambah butir H4, hitungan dari prediksi yang
sudah ada atau *probe* murah, untuk mayor konsensus panel 8:

- H4(i) — "no better than shuffled labels" dari dua titik pada lipatan berbeda. *Probe* berlabel AMI dilatih ulang
  pada lipatan dan C yang sama dengan nol (20261107, C 0,001); AUROC (c) dan persentilnya di dalam nol tanpa lapis
  (`perm_f1.csv`) dan nol berlapis (`perm_g1.csv`). Aturan: naskah menyebut *probe* berlabel infark "no more than a
  random infarction subset with the same STEMI share" hanya bila AUROC-nya ≤ persentil ke-95 nol berlapis; bila
  tidak, naskah menyebut ia melampaui nol itu.
- H4(ii) — Gambar 2 "did not depend on the interval" tanpa uji. Selisih keunggulan label Q4 − Q1 untuk (c), *probe* dan
  CNN, tiga penetapan lipatan, bootstrap 2.000 bergugus pasien, benih 20261164. Aturan: naskah menyatakan keunggulan
  tidak bergantung pada jarak hanya bila CI Q4 − Q1 *probe* di dalam ±0,03; bila tidak, Gambar 2 diberi judul
  deskriptif dan naskah menyatakan bahwa keunggulan yang lebih kecil di kuartil terjauh tidak tersingkirkan.
- H4(iii) — penyesuaian jarak yang lebih kuat dari satu fitur. AUROC (c) berlapis kuartil jarak (hanya pasangan
  OMI/non-OMI di kuartil yang sama; rerata AUROC per kuartil berbobot n₁·n₀), selisih label oklusi − label infark,
  *probe* dan CNN, tiga penetapan lipatan, bootstrap 2.000, benih 20261165. Aturan: "held within interval quartiles"
  hanya bila batas bawah *probe* > 0.
- H4(iv) — "unchanged" dengan jarak tanpa interval berpasangan. Selisih (keunggulan dengan jarak) − (keunggulan tanpa
  jarak), lipatan 20261107, C 0,001, bootstrap 2.000, benih 20261166. Aturan: "unchanged" hanya bila CI di dalam ±0,03.

Juga diputuskan di sini, tanpa hitungan baru: verdik R6, R10, R11, R12 dilaporkan terhadap 0 dan terhadap margin
0,03, dan naskah menyebut berapa estimat selisih label yang dihitung seluruhnya. Tidak dikerjakan: kontrol hanyut
STAFF III, uji pasangan bersarang kedua, analisis titik-balik pembalikan label.

**P3 (13 November 2026, sesudah panel 8, sebelum H5 dan H6 dijalankan; H4 sedang berjalan dan tidak diubah).** Dua
mayor panel 8 yang diajukan lebih dari satu peran (editor X6, devil's advocate X1 dan X3):

- H5 — pasangan bersarang kedua. Label STEMI bersarang di dalam infark seperti OMI. Untuk STEMI lawan NSTEMI di dalam
  AMI, AUROC *probe* berlabel STEMI (`oof_m3a_stemi.npz`, tiga penetapan lipatan) dan *probe* berlabel AMI
  (`oof_m3a_ami.npz`), selisih berpasangan, bootstrap 2.000, benih 20261167. Deskriptif: memberi skala bagi 0,042,
  yaitu berapa yang diajarkan label bersarang yang ditentukan dari EKG. Naskah melaporkan keduanya berdampingan dan
  tidak menyebut keunggulan label oklusi "besar" atau "kecil" tanpa skala ini.
- H6 — titik-balik tinjauan label. Mulai dari satu label acak berlapis tipe infark (benih 20261168, seperti G1), lalu
  tukar k pasangan: k EKG berlabel-acak negatif dengan skor *probe* berlabel AMI (lipatan 20261107, C 0,001, sama
  dengan H4(i)) tertinggi menjadi positif, dan k berlabel-acak positif dengan skor terendah menjadi negatif (jumlah
  positif tetap), di dalam tipe infark yang sama. *Probe* dilatih pada label tertukar (C 0,001, lipatan 20261107);
  keunggulan = AUROC (c) *probe* itu − AUROC (c) *probe* berlabel AMI, keduanya dinilai terhadap label tertukar.
  k ∈ {25, 50, 100, 200, 400}, dibagi ke tipe infark sebanding ukurannya, dengan k = 0 sebagai rujukan. Deskriptif: k terkecil yang memberi keunggulan ≥ 0,042 dilaporkan sebagai jumlah
  perubahan label berpola EKG yang cukup untuk menghasilkan keunggulan sebesar yang diamati; naskah menyebutnya di
  Pembahasan di samping 0,042, apa pun nilainya.

**P4 (13 November 2026, sesudah panel 11 `Telaah/2026-11-13-OMI-BPEX-5`, sebelum H7 dijalankan; H1–H6 sudah keluar di
`Hasil_OMI_12.md`).** Pengguna memilih "Small P4 analyses + draft 12". Dua mayor konsensus panel 11: rujukan induk
dilaporkan tanpa interval, dan "about 0.03 of the 0.042 exceeds what a random nested label gains" bersandar pada satu
label acak (H6, k = 0, +0,011) yang dikurangkan dari 0,042 melintasi rujukan dan sasaran yang berbeda. Ditambah
butir H7:

- H7(i) — interval rujukan. AUROC dengan interval bootstrap 2.000 bergugus pasien (benih 20261169) untuk setiap
  rujukan induk yang dipakai naskah: *probe* dan CNN berlabel AMI untuk (c), di dalam STEMI, dan di dalam NSTEMI
  (tiga penetapan lipatan, `oof_m3a_ami.npz`, `oof_m2_ami.npz`); *probe* berlabel STEMI untuk (c)
  (`oof_m3a_stemi.npz`); *probe* berlabel AMI untuk STEMI lawan NSTEMI di dalam AMI (pasangan kedua H5). Titik =
  rerata antarpenetapan lipatan, seperti tabel utama. Deskriptif.
- H7(ii) — sebaran keunggulan nol. Untuk tiap label acak berlapis tipe infark G1 (benih 1001–1100, dibangkitkan ulang
  dengan kode `omi_fase_g.permutasi` yang sama; prediksinya dulu tidak disimpan, jadi 100 *probe* dilatih ulang pada
  lipatan 20261107 dan C 0,001): keunggulan_k = AUROC (c) *probe* berlabel-acak − AUROC (c) *probe* berlabel AMI
  (lipatan dan C sama, H4(i)), **keduanya dinilai terhadap label acak k sendiri**. Pembanding yang setara: keunggulan
  label oklusi pada lipatan dan C yang sama (0,6431 − 0,6010). Sebelum melatih, label yang dibangkitkan ulang diperiksa
  ulang: AUROC (c) *probe* berlabel-acak terhadap OMI harus sama dengan `auc_c` di `perm_g1.csv` (selisih < 10⁻⁹);
  bila tidak, run berhenti dan tidak ada yang dilaporkan dari H7(ii). Keluaran per label ke
  `$OMI_DATA/perm_h7.csv` (bisa dilanjutkan).
  Aturan baca: naskah menyatakan label oklusi memperoleh **lebih dari yang diperoleh subset acak bersarang dengan
  komposisi sama terhadap labelnya sendiri** hanya bila keunggulan label oklusi > persentil ke-95 sebaran itu; bila
  tidak, naskah menyatakan keunggulan berada di dalam sebaran itu dan berhenti menyebut keunggulan sebagai lebih dari
  yang diberikan konstruksi. Apa pun hasilnya, rerata dan persentil ke-95 sebaran dilaporkan di samping 0,042, dan
  naskah tidak lagi mengurangkan satu angka nol dari 0,042. Persentil keunggulan label oklusi di dalam sebaran juga
  dilaporkan (deskriptif).

Tanpa hitungan baru: hasil kisi C diperlebar (`Hasil_OMI_4.md` bagian 2: C terpilih tetap 10⁻³) dikutip di naskah;
R13 ditandai sebagai aturan yang diubah sesudah hasil (deskriptif sejak draf 11).

**P5 (13 November 2026, sesudah panel 12 `Telaah/2026-11-13-OMI-BPEX-6`, sebelum H8 dijalankan; H1–H7 sudah keluar di
`Hasil_OMI_12.md` dan `Hasil_OMI_13.md`).** Pengguna memilih "Last P5 round + panel 13". Mayor panel 12: R17 hampir
pasti dari konstruksi dan bukan skala (label acak tak punya isi untuk dipelajari); enam *probe* label kontrol tak pernah
dinilai terhadap labelnya sendiri; keunggulan tak diterjemahkan ke titik operasi; jarak masuk di bawah penalti L2 yang
sama dengan *embedding*. Ditambah butir H8, tanpa melatih *embedding* atau CNN baru:

- H8(i) — skala dari label bersarang klinis. Untuk tiap label kontrol H2 (prediksi `kontrol_h2.npz`, lipatan 20261107,
  C 0,001): AUROC *probe* berlabel kontrol dan *probe* berlabel AMI (lipatan dan C sama, H4(i)), keduanya dinilai
  terhadap label kontrol itu di antara EKG ber-AMI (label lawan AMI tanpa label), dan selisihnya; bootstrap 2.000
  bergugus pasien, benih 20261170. Label oklusi pada lipatan dan C yang sama dilaporkan di baris yang sama.
  Aturan baca: naskah menyebut urutan 0,042 di antara tujuh keunggulan (enam kontrol + oklusi) beserta rujukan
  masing-masing, menyebut skala ini sebagai skala keunggulan (butir 3 protokol), dan menyebut R17 hanya sebagai cek
  bahwa pelatihan ulang saja tidak memberi keunggulan. Naskah tidak menyebut keunggulan oklusi "besar" bila ada label
  kontrol dengan keunggulan lebih besar.
- H8(ii) — titik operasi di dalam infark. Untuk (c) OMI lawan infark tanpa oklusi, sensitivitas *probe* berlabel OMI
  dan berlabel AMI pada spesifisitas 80 % dan 90 % (ambang dari EKG infark tanpa oklusi, dihitung ulang di tiap ulangan
  bootstrap), rerata tiga penetapan lipatan (`oof_m3a.npz`, `oof_m3a_ami.npz`); selisih berpasangan, bootstrap 2.000,
  benih 20261171; juga sebagai tambahan EKG OMI terdeteksi per 1.000 EKG infark (selisih × 1.133/2.646 × 1.000).
  Deskriptif.
- H8(iii) — jarak tanpa penalti. Di antara EKG ber-AMI, regresi logistik tahap kedua tanpa penalti pada logit skor
  *probe* (lipatan 20261107, C 0,001; berlabel OMI = `kontrol_h2.npz` OMI_asli, berlabel AMI = H4(i)) ditambah spline
  kubik log(1 + jarak) (`SplineTransformer`, 5 simpul), dilatih dengan lima lipatan bergugus pasien (`lipatan`, benih
  20261107) di dalam AMI, prediksi di luar lipatan. Selisih AUROC (c) tahap kedua label oklusi − label infark,
  bootstrap 2.000, benih 20261172. Aturan seperti R12: keunggulan "not explained by the delay" dengan penyesuaian tanpa
  penalti hanya bila batas bawah > 0; bila tidak, naskah menyatakan keunggulan tidak terbedakan sesudah jarak
  dimasukkan tanpa penalti, dan R12/R16 tidak lagi dipakai sebagai bukti.
