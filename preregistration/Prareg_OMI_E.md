# Pra-daftar OMI fase E — kontrol di dalam rekaman, kelainan kronis, dan CNN berlabel infark (13 November 2026)

> **TERKUNCI 13 November 2026** atas pilihan pengguna "Fase E, lalu panel 5 di PMEA" dan persetujuan unduhan STAFF III
> tambahan (~18 MB). Isi di atas bagian "Penyimpangan" tidak disunting lagi; perubahan masuk sebagai penyimpangan
> bertanggal sebelum run yang terdampak.

## Mengapa ada fase E

Panel 4 (`Telaah/2026-11-13-OMI-JE-3`, *J Electrocardiology*, NOT READY, Reject in current form, editor
send_to_review, signifikansi 2). Kritis konsensus: klaim "same signal" hampir dipaksa oleh label bersarang (semua OMI
adalah AMI), sedangkan satu-satunya pembanding yang informatif, OMI lawan AMI tanpa OMI, memberi *probe*-OMI +0,042
[0,033; 0,051] atas *probe*-AMI, di atas batas 0,03 yang dipakai D2. Mayor yang bisa diuji dengan data: (a) kenaikan
STAFF III tanpa kontrol di dalam rekaman yang sama; (b) kedua *probe* dibandingkan pada skala logit yang berbeda;
(c) tidak ada uji yang memisahkan kelainan akut dari kronis; (d) pemeriksaan waktu dan jenis kelamin hanya untuk
kelompok gabungan, bukan untuk NSTEMI tanpa PCI; (e) "models" digeneralisasi dari satu *probe* linear pada
*embedding* yang dilatih dengan label infark.

Ditulis **sesudah** hasil fase A–D diketahui (`Hasil_OMI_0.md` sampai `Hasil_OMI_8.md`) dan sesudah laporan panel 4.
Belum dihitung: skor STAFF III awal inflasi, AUROC subkelompok tanpa AMI, (b5) per kuartil dan jenis kelamin, CNN
berlabel AMI. Semua butir **eksploratif** terhadap pra-daftar 7 Nov. Sasaran panel 5: *Physiological Measurement*.

## Ukuran bersama

Seperti fase A–D: analisis utama Chongqing (tanpa Paced, 17.622 EKG); taksiran titik = rata-rata metrik per benih
lipatan (20261107–09); CI 95 % = bootstrap 2.000 bergugus pasien; satu benih bootstrap per butir. Skrip
`omi_fase_e.py` (CNN di `venv-gpu`); keluaran `Hasil_OMI_9.md`. Skor *probe*-OMI = prediksi kohort penuh M3a yang
tersimpan; skor *probe*-AMI = `oof_m3a_ami.npz` (D2).

## E1. STAFF III: kontrol di dalam rekaman inflasi (utama fase E)

**Data tambahan.** Untuk 98 pasien D3, satu potongan 10 s dari rekaman inflasi pertama (`BI1`) yang dimulai 1 s
sesudah penanda `balloon inflation` di berkas `.event` (penanda terdekat ke D0 spreadsheet; bila tidak ada: D0).
Pemeriksaan mutu dan pra-proses sama dengan D3. Pasien dibuang bila potongan awal gagal mutu atau di luar batas; jumlah
dilaporkan.

**Model.** *Probe*-OMI dan *probe*-AMI akhir persis seperti D3 (dilatih ulang dengan prosedur yang sama, C dari
`pilih_C` benih 20261107).

**Ukuran** (logit; CI bootstrap 2.000 atas pasien, benih 20261126): rerata perubahan dan bagian pasien naik untuk
(i) akhir inflasi − awal inflasi (rekaman sama), (ii) awal inflasi − baseline (rekaman berbeda, iskemia minimal),
(iii) akhir inflasi − baseline (= D3, dihitung ulang pada pasien yang sama). Untuk membandingkan kedua *probe* pada
skala yang sama, perubahan juga dibagi simpangan baku logit masing-masing *probe* pada EKG Chongqing tanpa AMI (skor
model akhir pada EKG latihnya), dengan selisih berpasangan *probe*-OMI − *probe*-AMI dan CI.

Aturan baca, ditetapkan sekarang (*probe*-OMI):
- Bila batas bawah CI (i) > 0 dan batas bawah CI bagian naik (i) > 0,5: kenaikan terjadi di dalam rekaman yang sama,
  jadi tidak dapat dijelaskan oleh perbedaan rekaman; naskah menyatakan skor naik selama oklusi balon di dalam rekaman.
- Bila tidak: kenaikan D3 tidak dapat dipisahkan dari perbedaan rekaman; klaim "responds to acute ischaemia" turun
  menjadi "rose between baseline and inflation recordings", dan bagian STAFF III di abstrak dibatasi sesuai itu.
- (ii) deskriptif: bila rerata (ii) lebih dari separuh rerata (iii), naskah menyebut bahwa sebagian besar kenaikan
  sudah ada dalam 11 s pertama atau berasal dari perbedaan rekaman.
- Perbandingan *probe* terstandar deskriptif; kata "as much" hanya dipakai bila CI selisih terstandar memuat 0.

## E2. Kelainan kronis di kelompok tanpa AMI

Di 14.976 EKG tanpa AMI, AUROC skor *probe*-OMI dan *probe*-AMI untuk tiap subkelompok lawan sisa kelompok tanpa AMI:
`CTO = 1` (oklusi total kronis), `Prior_PCI = 1`, `UA = 1`, `VF_VT = 1`. n tiap sel disebut. Benih bootstrap 20261127.

Aturan baca: bila batas bawah CI AUROC *probe*-OMI untuk CTO **≥ 0,70**, skor juga tinggi pada oklusi kronis tanpa
infark akut, dan naskah tidak menyebut sinyalnya "acute" tanpa kualifikasi. Bila < 0,70, uji ini dilaporkan sebagai
bukti bahwa skor membedakan kelainan akut dari oklusi kronis. Subkelompok lain deskriptif.

## E3. NSTEMI tanpa PCI per kuartil dan jenis kelamin

AUROC (b5) AMI tanpa OMI dengan `NSTEMI = 1` dan `PCI = 0` lawan tanpa AMI, per kuartil `Time_Interval` (batas P4,
kuartil per EKG seperti D1) dan per jenis kelamin, untuk M2 dan M3a. Juga OMI dengan `NSTEMI = 1` lawan AMI tanpa OMI
dengan `NSTEMI = 1` (sudah di Tabel 4 sebagai "OMI within NSTEMI") per kuartil dan jenis kelamin. Deskriptif; n
disebut. Benih bootstrap 20261128.

## E4. CNN dengan label AMI

CNN M2 (resep `omi_m2.py` apa adanya: arsitektur, 20 epoch, bobot kelas (1 − p)/p, 250 Hz, benih 20261107–09) dilatih
dengan sasaran `AMI` pada analisis utama, lipatan dari `lipatan` atas label AMI (sama dengan D2). Dinilai untuk OMI
lawan semua, (c) OMI lawan AMI tanpa OMI, dan AMI lawan tanpa AMI; selisih AUROC berpasangan CNN-OMI (M2 tersimpan) −
CNN-AMI dengan CI. Benih bootstrap 20261129.

Aturan baca, ditetapkan sekarang, untuk *probe* (D2, angka sudah diketahui: dinyatakan terbuka) dan CNN (belum
diketahui): label OMI dinyatakan "menambah sedikit di dalam infark" bila batas bawah CI selisih untuk (c) > 0; "hampir
tidak menambah" hanya dipakai untuk pembanding yang batas atas CI-nya < 0,03. Judul dan simpulan tidak lagi memakai
"learn largely the same signal"; keduanya melaporkan kedua pembanding berdampingan.

## Tidak dikerjakan di fase E

Kontrol iskemia tanpa oklusi (tidak ada di data), CNN disetel di dalam infark, pembaca titik J manusia, model fondasi
kedua, segmen STAFF III lain di luar awal inflasi.

## Penyimpangan

(belum ada)
