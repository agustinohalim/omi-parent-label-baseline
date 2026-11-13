# Pra-daftar OMI fase D — kelompok pembanding, label latih, dan uji eksternal oklusi buatan (13 November 2026)

> **TERKUNCI 13 November 2026** atas pilihan pengguna "Fase D + STAFF III" dan persetujuan unduhan selektif STAFF III.
> Isi di atas bagian "Penyimpangan" tidak disunting lagi; perubahan masuk sebagai penyimpangan bertanggal sebelum run
> yang terdampak.

## Mengapa ada fase D

Panel 3 (`Telaah/2026-11-13-OMI-JE-2`, *J Electrocardiology*, NOT READY, editor *desk_reject*) memberi satu temuan
kritis konsensus: kelompok "infark tanpa OMI" memuat 708 EKG berdiagnosis STEMI (46,8 %) dan 765 EKG dengan PCI
(50,6 %), jadi AUROC 0,825 (C2 b) tidak bisa membedakan "model mengenali infark" dari "model mengenali oklusi yang
sudah reperfusi atau STEMI yang tak tercatat sebagai OMI". Mayor terkait: 0,825 tidak dipecah menurut waktu dan jenis
kelamin; tidak ada pembanding *probe* yang dilatih pada label infark; uji STAFF III baru diusulkan; signifikansi hanya
rekomendasi pelaporan.

Pengguna memilih "Fase D + STAFF III" (13 Nov) dan menyetujui unduhan selektif STAFF III (~40 MB).

Ditulis **sesudah** hasil fase A–C diketahui (`Hasil_OMI_0.md` sampai `Hasil_OMI_7.md`) dan sesudah membaca laporan
panel 3. Dari STAFF III baru dibaca metadata (header, berkas `.event`, spreadsheet anotasi: 104 pasien, 103 dengan
rekaman baseline cath lab, durasi inflasi pertama 69–595 s, median 296 s; arteri RCA 47, LAD 32, sirkumfleks 21,
diagonal 2, *main* 2; infark lama tercatat pada 35). Belum ada sinyal STAFF III yang diunduh atau dinilai model, dan
belum ada yang dihitung untuk D1 dan D2. Semua butir **eksploratif** terhadap pra-daftar 7 Nov.

## Ukuran bersama

Seperti fase A–C: analisis utama Chongqing (tanpa Paced, 17.622 EKG); taksiran titik = rata-rata metrik per benih
lipatan (20261107–09); CI 95 % = bootstrap 2.000 bergugus pasien (`ringkas`, `metrik`, `beda_auc` dari `omi_m01.py`
dan `omi_konstruk.py`); satu benih bootstrap per butir. Skrip `omi_fase_d.py`; keluaran `Hasil_OMI_8.md`. Skor OMI
model M0, M1, M2, M3a = prediksi kohort penuh yang sudah tersimpan (sama dengan C2).

## D1. Kelompok pembanding dipecah

Untuk M3a dan M2 (M0, M1 hanya baris pelengkap), AUROC dengan sasaran "kelompok uji lawan tanpa AMI" (14.976 EKG):
- (b1) AMI tanpa OMI dengan `STEMI = 1` (708) lawan tanpa AMI;
- (b2) AMI tanpa OMI dengan `NSTEMI = 1` (804) lawan tanpa AMI;
- (b3) AMI tanpa OMI dengan `PCI = 1` lawan tanpa AMI; (b4) AMI tanpa OMI dengan `PCI = 0` lawan tanpa AMI;
- (b5) AMI tanpa OMI dengan `NSTEMI = 1` dan `PCI = 0` lawan tanpa AMI;
- (a) OMI lawan tanpa AMI, (b) AMI tanpa OMI lawan tanpa AMI, (c) OMI lawan AMI tanpa OMI, masing-masing per kuartil
  `Time_Interval` (batas P4; kuartil ditentukan per EKG) dan per jenis kelamin (`gender`).

n tiap sel disebut. Benih bootstrap 20261123.

Aturan baca, ditetapkan sekarang (M3a):
- Bila batas bawah CI (b2) **≥ 0,70** dan (b5) **≥ 0,70**: bacaan "model memberi skor tinggi pada infark tanpa
  oklusi" bertahan, juga pada infark non-ST-elevasi tanpa revaskularisasi.
- Bila (b1) ≥ 0,70 tetapi (b2) < 0,70: bacaan diubah menjadi "skor tinggi pada STEMI tanpa label OMI" (kemungkinan
  oklusi yang sudah reperfusi atau label OMI yang terlewat); klaim "mengenali infark" dikeluarkan dari judul dan
  abstrak.
- Bila (b1) dan (b2) keduanya < 0,70: bacaan "mengenali infark" gugur.
- Per kuartil dan jenis kelamin deskriptif; bila (b) di Q1 dan Q4 berselisih > 0,05 hal itu dilaporkan sebagai
  ketergantungan pada waktu.

## D2. *Probe* yang dilatih pada label AMI

*Probe* M3a (embedding ECGFounder tersimpan, prosedur `oof` dengan `pilih=True`, benih lipatan 20261107–09, tanpa
bobot kelas) dilatih dengan sasaran `AMI` pada analisis utama. Skornya dinilai untuk: OMI lawan semua (sasaran utama
fase A), (c) OMI lawan AMI tanpa OMI, dan AMI lawan tanpa AMI. Selisih AUROC berpasangan *probe*-OMI − *probe*-AMI
untuk sasaran OMI lawan semua dan untuk (c). Benih bootstrap 20261124.

Aturan baca: bila batas atas CI selisih AUROC (*probe*-OMI − *probe*-AMI) untuk OMI lawan semua **< 0,03**, naskah
menyatakan bahwa melatih dengan label OMI hampir tidak menambah apa pun di atas melatih dengan label infark; bila tidak,
besar tambahannya dilaporkan dengan CI.

## D3. Uji eksternal STAFF III: apakah skor naik saat arteri disumbat balon? (utama fase D)

**Data.** STAFF III (PhysioNet, ODC-By 1.0): oklusi koroner terkendali oleh balon PTCA elektif, tanpa infark akut.
Satu pasang per pasien:
- *baseline*: 10 s dari rekaman baseline cath lab pertama (`BC1`), mulai di titik tengah rekaman (dibulatkan ke
  detik);
- *akhir inflasi*: 10 s dari rekaman inflasi pertama (`BI1`) yang berakhir 1 s sebelum penanda `balloon deflation`
  di berkas `.event` (bila tidak ada penanda: D0 + D1 dari spreadsheet).

Pasien dibuang bila: tanpa `BC1`; nomor 1, 4, 5, 6, 89 (spreadsheet: sadapan mungkin tertukar atau terbalik);
segmen mana pun tak terbaca, berisi nilai konstan > 1 s pada sadapan mana pun, atau di luar batas rekaman. Jumlah yang
dibuang dan alasannya dilaporkan.

**Pra-proses.** Sembilan sadapan (V1–V6, I, II, III; 1.000 Hz, 1.600 unit/mV). aVR = −(I + II)/2, aVL = I − II/2,
aVF = II − I/2. Urutan model I, II, III, aVR, aVL, aVF, V1–V6. Turun cuplik 1.000 → 500 Hz dengan
`scipy.signal.resample_poly(·, 1, 2)`, jadi 12 × 5.000, lalu `praproses` dan embedding ECGFounder persis seperti
`omi_m3_ecgfounder.py` (GPU environment).

**Model.** (i) *Probe*-OMI akhir: M3a dilatih pada semua EKG analisis utama dengan C dari `pilih_C` benih 20261107
(sama dengan model kiriman server, P4 butir 4). (ii) *Probe*-AMI akhir: sama, sasaran `AMI` (D2). CNN M2 tidak dinilai
(model akhir tidak disimpan).

**Ukuran** (per model, pada logit dan pada peluang): rerata perubahan berpasangan (akhir inflasi − *baseline*);
bagian pasien dengan skor naik; AUROC tak berpasangan (skor akhir inflasi lawan skor *baseline* sebagai dua
kelompok); median skor tiap keadaan. CI 95 % bootstrap 2.000 atas pasien, benih 20261125; uji Wilcoxon bertanda
sebagai pelengkap. Deskriptif: per arteri (LAD, RCA, sirkumfleks; lainnya digabung), tanpa dan dengan infark lama, dan
letak skor *baseline* STAFF III terhadap sebaran skor kelompok tanpa AMI Chongqing (persentil median).

Aturan baca, ditetapkan sekarang (*probe*-OMI, logit):
- Bila batas bawah CI rerata perubahan **> 0** dan batas bawah CI bagian pasien yang naik **> 0,5**: model membawa
  sinyal iskemia oklusi akut yang tidak bergantung pada infark. Judul dan simpulan tidak lagi menyatakan bahwa model
  "terutama mengenali infark"; klaim diperluas ke "membawa sinyal oklusi akut pada data eksternal" dengan besar
  efeknya.
- Bila tidak: tidak ada bukti sinyal oklusi akut pada data eksternal; bacaan "terutama mengenali infark" (atau
  bacaan D1 yang berlaku) bertahan, dan uji ini dilaporkan sebagai hasil negatif.
- Perbandingan *probe*-OMI lawan *probe*-AMI (selisih rerata perubahan logit, CI berpasangan) deskriptif: bila
  keduanya naik serupa, sinyalnya iskemia/cedera umum, bukan khas oklusi.

Batas yang diakui sebelum melihat hasil: perangkat dan filter STAFF III berbeda dari Chongqing (Mecg-300), jadi
kalibrasi mutlak tidak dibaca; hanya perubahan di dalam pasien. Sadapan ekstremitas turunan dari I dan II. Pasien
STAFF III menjalani PTCA elektif, bukan sindrom koroner akut.

## Tidak dikerjakan di fase D

Pembacaan titik J oleh manusia, CNN dilatih ulang di dalam infark, model fondasi kedua, segmen awal inflasi atau
pasca-inflasi STAFF III (di luar unduhan yang disetujui), label OMI versi paradigma luas.

## Penyimpangan

(belum ada)
