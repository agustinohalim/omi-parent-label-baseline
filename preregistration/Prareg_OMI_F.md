# Pra-daftar OMI fase F — nol permutasi, waktu ke angiografi, CTO lawan OMI, ragam benih CNN (13 November 2026)

> **TERKUNCI 13 November 2026** atas pilihan pengguna "Phase F limited + back to JE": hanya pemeriksaan murah pada data
> yang sudah ada di disk, klaim naskah diturunkan, sasaran kembali ke *J Electrocardiology*, lalu panel 6. Isi di atas
> bagian "Penyimpangan" tidak disunting lagi; perubahan masuk sebagai penyimpangan bertanggal sebelum run yang
> terdampak.

## Mengapa ada fase F

Panel 5 (`Telaah/2026-11-13-OMI-PMEA`, *Physiological Measurement*, NOT READY, Reject in current form; editor
desk_reject). Mayor yang bisa diuji tanpa data baru: (a) selisih +0,042 di dalam infark tidak dibandingkan dengan
nol yang sepadan (struktur pelatihan bisa menghasilkannya sendiri); (b) selisih itu bisa berasal dari jarak EKG ke
angiografi; (c) uji CTO tidak membandingkan oklusi kronis dengan oklusi akut secara langsung; (d) CI bootstrap tidak
memuat ragam pelatihan, benih CNN tidak dilaporkan, selisih per penetapan lipatan tidak diberikan.

Ditulis **sesudah** hasil fase A–E (`Hasil_OMI_0.md` sampai `Hasil_OMI_9.md`) dan panel 5. Belum dihitung: semua
butir di bawah. Semua butir **eksploratif**. Tidak ada unduhan baru. Keluaran `Hasil_OMI_10.md`; skrip
`omi_fase_f.py` dikomit sebelum dijalankan.

## Ukuran bersama

Analisis utama Chongqing (tanpa Paced, 17.622 EKG). "(c)" = OMI lawan AMI tanpa OMI (1.133 / 2.646). CI 95 % =
bootstrap 2.000 bergugus pasien. *Probe* = regresi logistik L2 pada *embedding* ECGFounder dengan C = 0,001 (nilai
yang terpilih di setiap lipatan dan analisis fase A–D). Benih bootstrap: F1 20261130, F2 20261131, F3 20261132,
F4 20261133.

## F1. Nol permutasi untuk label oklusi di dalam infark

Di antara 2.646 EKG ber-AMI, label OMI diacak ulang (permutasi tingkat EKG, jumlah 1.133 tetap), EKG tanpa AMI tetap
negatif. *Probe* dilatih pada label teracak itu dengan penetapan lipatan 20261107 (lipatan dari `lipatan` atas label
teracak), C = 0,001, lalu AUROC (c) dihitung terhadap label OMI **asli**. 100 permutasi (benih 1–100). Rujukan
sepadan: *probe* yang sama (penetapan 20261107, C = 0,001) pada label asli.

Aturan baca: bila AUROC (c) label asli melebihi persentil ke-95 sebaran nol, label oklusi membawa informasi di dalam
infark di atas yang dihasilkan struktur pelatihan; naskah melaporkan selisih terhadap rerata nol. Bila tidak, selisih
+0,04 dilaporkan sebagai tidak terbedakan dari struktur pelatihan dan klaim "the occlusion label adds information
within infarction" dihapus.

## F2. Selisih label per kuartil jarak EKG ke angiografi

Selisih AUROC berpasangan *probe*-OMI − *probe*-AMI dan CNN-OMI − CNN-AMI (prediksi tersimpan, tiga penetapan) untuk
(c) dan untuk OMI lawan semua, per kuartil `Time_Interval` (kuartil per EKG atas analisis utama, seperti D1/E3).

Aturan baca: bila batas bawah CI selisih (c) *probe* > 0 di Q1 dan di Q4, selisih tidak terbatas pada EKG dekat
angiografi; bila tidak, naskah menyebut kuartil mana yang tidak menunjukkannya. Selebihnya deskriptif.

## F3. Oklusi kronis lawan oklusi akut

Untuk *probe*-OMI dan *probe*-AMI (prediksi kohort penuh tersimpan): (i) AUROC OMI lawan CTO langsung (1.133 / 946);
(ii) AUROC OMI lawan tanpa AMI non-CTO dan AUROC CTO lawan tanpa AMI non-CTO pada rujukan yang sama (14.030), dengan
selisih berpasangan dan CI; (iii) CTO lawan tanpa AMI non-CTO, dipisah menurut `Prior_PCI`.

Aturan baca: naskah hanya menyatakan skor lebih tinggi pada oklusi akut daripada oklusi kronis bila batas bawah CI
(i) ≥ 0,70. Kalimat "evidence that the score separates acute abnormality from chronic occlusion" (aturan E2) tidak
dipakai lagi dalam keadaan apa pun, karena E2 tidak membandingkan oklusi akut dengan kronis; ini penyimpangan dari
cara E2 dilaporkan di draf 5, dicatat di naskah.

## F4. Ragam pelatihan

(a) Selisih AUROC per penetapan lipatan (tiga nilai) untuk setiap baris Tabel 3, *probe* dan CNN, dari prediksi
tersimpan. (b) CNN M2 (resep `omi_m2.py` apa adanya) dilatih ulang dengan lima benih inisialisasi (20261140–44) pada
penetapan lipatan 20261107, untuk label OMI dan label AMI (10 latihan, `venv-gpu`); lipatan dari `lipatan` atas
masing-masing label seperti sebelumnya. Dilaporkan: AUROC (c) per benih untuk kedua label, selisih per pasangan
benih, rerata dan rentang, serta selisih AUROC prediksi rerata lima benih dengan CI bootstrap.

Aturan baca: naskah menyatakan CNN berlabel oklusi lebih baik di dalam infark hanya bila sedikitnya 4 dari 5 selisih
per pasangan benih > 0 dan batas bawah CI selisih prediksi rerata > 0.

## Aturan tulis naskah (tanpa analisis)

- "Equal overall": hanya bila CI selisih untuk OMI lawan semua berada seluruhnya di dalam ±0,03 (batas 0,03 yang
  dipakai sejak D2, sekarang dibaca dua arah). Selain itu ditulis sebagai selisih dengan CI.
- STAFF III: tanpa batas kesetaraan yang ditetapkan sebelumnya, "as much" diganti selisih terstandar dengan CI; abstrak
  memuat juga selisih dari baseline (−0,123 [−0,218; −0,027]).
- "Tracks acute ischaemia and infarction", "small", dan "a little" tidak dipakai di judul, abstrak, dan simpulan.
- Judul memuat satu pesan.

## Tidak dikerjakan di fase F

Pengukur ST tervalidasi, kontrol hanyut STAFF III di dalam rekaman baseline (butuh unduhan), jaringan disetel di
dalam infark, model fondasi kedua, dataset kedua.

## Penyimpangan

(belum ada)
