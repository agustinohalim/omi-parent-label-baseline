# Pra-daftar OMI (7 November 2026)

> TERKUNCI 7 November 2026 (izin komit pengguna: "go"). Butir bertanda "BELUM DITETAPKAN" diputuskan
> lewat "Penyimpangan" bertanggal di akhir berkas **sebelum** model pertama dilatih; selain itu isi di atas
> bagian Penyimpangan tidak disunting.

Rencana: `Artikel_OMI_Rencana.md` (A/B disetujui 7 Nov 2026). Hitungan label: `Hasil_OMI_0.md`.

## 1. Sasaran

- Utama: OMI vs bukan-OMI pada semua EKG latih (1.151 / 16.809).
- Sekunder 1: NSTEMI-OMI vs NSTEMI-bukan-OMI di dalam NSTEMI (423 / 812).
- Sekunder 2: teritori penyebab satu teritori (LAD 347 / LCX 209 / RCA 355; LM 5 dibuang) pada EKG OMI;
  dilaporkan juga khusus NSTEMI-OMI (88 / 106 / 108) sebagai eksploratif karena kecil.

## 2. Pembagian

Validasi silang 5 lipatan **per pasien**, berstrata OMI, 3 benih (20261107, +1, +2) di dalam train.csv.
Server penilai (uji tersembunyi, hanya biner) dipakai sekali di akhir untuk model terbaik pada ambang
yang ditetapkan dari validasi silang; bukan untuk memilih model.

## 3. Model (berjenjang)

- M0: usia + jenis kelamin (regresi logistik).
- M1: ciri ST dari denyut median (`.med`): amplitudo J+60 ms dan J+80 ms per 12 sadapan, relatif
  terhadap garis PR; regresi logistik L2 (C dari CV bersarang).
- M2: CNN 1D (ResNet kecil) pada 10 s mentah, dilatih penuh; arsitektur dan hiperparameter BELUM
  DITETAPKAN (diambil dari pola kode Arrest).
- M3: model fondasi beku + probe linear (regresi logistik L2) — ECG-FM (MIT), ECGFounder (MIT); ECG-JEPA (MIT)
  bila bobotnya dapat diunduh — BELUM DITETAPKAN. HuBERT-ECG (CC BY-NC) opsional. Pra-proses mengikuti README tiap model.

## 4. Ukuran

AUROC, AUPRC, Brier, slope/intercept kalibrasi, sensitivitas pada spesifisitas 90 %, net benefit pada
ambang 1–10 %. CI bootstrap 2.000 kali bergugus pasien atas prediksi out-of-fold. Perbandingan utama:
M3 terbaik vs M2 dan vs M1 (DeLong berpasangan dan bootstrap); lainnya deskriptif.

## 5. Yang dikeluarkan

EKG Paced (338) dikeluarkan dari analisis utama, disertakan dalam analisis kepekaan. 2 EKG AMI tanpa
jenis SKA dan 1 OMI "bukan SKA" (`Hasil_OMI_0.md`) tetap di sasaran utama, keluar dari sekunder 1.

## Penyimpangan

**P1 (11 November 2026, sebelum model apa pun dilatih; tidak ada label dibaca untuk menetapkannya).** Rincian M0/M1
yang tidak tertulis di atas:

- Berkas `.med`: 12.000 bita = 500 sampel × 12 sadapan int16 little-endian, **berselang** (sampel demi sampel),
  urutan sadapan sama dengan `.hea` rekaman mentah (I, II, III, aVR, aVL, aVF, V1–V6), satuan µV (1000/mV seperti
  `.hea`). Diperiksa tanpa label: tata letak berselang memberi II − (I + III) = 0 tepat; tata letak blok tidak.
  Jendela 1 s, puncak R median di sampel ±233.
- Titik J dan garis PR, satu algoritme untuk semua EKG: kecepatan spasial = jumlah |selisih| 12 sadapan, dihaluskan
  rata-rata bergerak 5 sampel; R = puncak jumlah |deviasi dari median| pada sampel 150–350; ambang = 15 % maksimum
  kecepatan pada R − 150 ms … R + 200 ms; awal QRS = mundur dari R sampai 5 sampel berturut di bawah ambang; J = maju
  dari R sampai 5 sampel berturut di bawah ambang. Garis PR per sadapan = rata-rata 10 sampel (20 ms) yang berakhir
  5 sampel sebelum awal QRS. Ciri M1 = amplitudo pada J + 60 ms dan J + 80 ms dikurangi garis PR, dalam mV (24 ciri).
  Uji tanpa label pada 400 EKG (tiap EKG ke-50): 0 gagal, durasi QRS median 82 ms (persentil 5–95: 72–108 ms).
- Gagal deteksi atau QRS < 50 ms atau > 200 ms atau J + 80 ms di luar jendela → ciri kosong, diisi median lipatan
  latih; jumlahnya dilaporkan.
- M0: regresi logistik usia + jenis kelamin (usia distandarkan di lipatan latih), L2 dengan C = 1.
- M1: ciri ST distandarkan di lipatan latih; L2, C dipilih CV dalam 5 lipatan per pasien dari {10⁻³, 10⁻², 10⁻¹, 1,
  10, 100} dengan log-loss. M1 tidak memuat usia/jenis kelamin; M0 + M1 (gabungan) dilaporkan sebagai deskriptif.
- Tiga benih = tiga pembagian lipatan. Taksiran titik = rata-rata metrik ketiga benih (prediksi out-of-fold tiap
  benih dinilai sendiri, **tidak** dirata-ratakan antarbenih). CI = bootstrap 2.000 kali bergugus pasien; tiap ulangan
  menghitung metrik per benih pada pasien yang sama lalu merata-ratakannya.
- Sensitivitas pada spesifisitas 90 % = ambang dari kuantil 0,9 skor kelas negatif. Kalibrasi = slope (regresi logistik hasil atas logit
  prediksi) dan intercept dengan slope dikunci 1 (offset). Net benefit pada ambang 1, 2, 5, 10 %.
- Sekunder 2 (teritori): regresi logistik multinomial; ukuran = AUROC satu-lawan-sisanya per teritori dan rata-rata
  makro.
- Kepekaan: sasaran utama dengan EKG Paced disertakan.

### P2 — 11 November 2026, sesudah M0/M1 dijalankan (perbaikan numerik, bukan perubahan analisis)

Ditulis **sesudah** melihat hasil M0/M1 (`Hasil_OMI_1.md`), jadi dicatat apa adanya. Pemicu: 160 peringatan
`overflow encountered in exp` dari penaksir slope/intercept kalibrasi dan batas bawah slope M0 + M1 sekunder 1 sebesar
−1336835,661. Penaksir Newton tanpa peredam meloncat pada replikat bootstrap yang prediksinya hampir konstan.

- Penaksir diganti Newton teredam: mulai dari logit prevalensi, langkah dipotong separuh sampai log-likelihood tidak
  turun, eta dibatasi ±30, paling banyak 100 iterasi. Tak konvergen atau |slope| > 10³ → replikat itu tidak ikut
  kuantil CI slope; jumlahnya dicetak per model.
- Definisi ukuran (slope = regresi logistik hasil atas logit prediksi; intercept dengan slope dikunci 1), model,
  lipatan, benih, bootstrap (2.000, benih 20261111), dan semua ukuran lain tidak berubah. M0/M1 dijalankan ulang
  utuh dengan `omi_m01.py` yang sudah diperbaiki; angka selain slope/intercept diharapkan identik dan diperiksa.

### P3 — 11 November 2026, sebelum M2/M3 dilatih (menetapkan butir "BELUM DITETAPKAN")

Ditulis sesudah hasil M0/M1 diketahui (`Hasil_OMI_1.md`) tetapi sebelum M2/M3 dilatih atau diuji coba pada label.

- **M2** mengikuti pola kode Arrest (`Uji_Arrest/02_cnn_arrest.py`) apa adanya; pola itu CNN polos, bukan ResNet,
  jadi kata "ResNet kecil" di bagian 3 tidak diikuti. Masukan 12 × 2.500 (10 s mentah, 500 → 250 Hz dengan rerata dua
  sampel), dikurangi rerata per sadapan, dibagi simpangan baku global lipatan latih. Empat blok Conv1d(kernel 7) +
  BatchNorm + ReLU + MaxPool(4), kanal 32-64-64-128, rerata global, dropout 0,3, satu lapis linear. Adam 1e-3,
  20 epoch tetap (tanpa henti dini; model epoch terakhir), batch 64, bobot kelas seimbang. Benih torch = benih lipatan.
  Sekunder 1 dilatih ulang di dalam NSTEMI dengan resep sama; sekunder 2 = keluaran softmax tiga kelas pada EKG OMI
  satu teritori. Lipatan, benih, bootstrap, dan ukuran sama dengan M0/M1 (fungsi yang sama di `omi_m01.py`).
- **M3** = model fondasi beku + probe regresi logistik L2, C dari CV bersarang dengan kisi dan log-loss yang sama
  dengan M1. Model: **ECGFounder** (bobot `PKUDigitalHealth/ECGFounder` `12_lead_ECGFounder.pth`, MIT; kode
  `NickLJLee/ECGFounder`, MIT) — wajib; **ECG-FM** (`wanglab/ecg-fm` `mimic_iv_ecg_physionet_pretrained.pt`, MIT;
  butuh `fairseq-signals`, lisensi tak tercantum) — dijalankan bila pustakanya terpasang di Windows/venv-gpu; bila
  tidak, dicatat "tidak dijalankan" dengan alasannya, bukan diganti model lain. ECG-JEPA dan HuBERT-ECG tidak
  dijalankan. Embedding = keluaran lapis sebelum kepala klasifikasi, dirata-ratakan atas waktu; pra-proses (laju
  sampel, panjang, normalisasi) mengikuti kode resmi tiap model dan ditulis di docstring skrip sebelum dijalankan.
- **Perbandingan utama** (bagian 4) tetap: M3 terbaik lawan M2 dan lawan M1. "Terbaik" dipilih dengan AUROC
  out-of-fold analisis utama, dan pemilihan itu dinyatakan sebagai sumber optimisme.
- **Server penilai** tetap dipakai sekali di akhir; ambang biner = titik spesifisitas 90 % dari prediksi out-of-fold.

### P4 — 11 November 2026, sesudah M0–M3a dan perbandingan utama diketahui

Semua butir di bawah ditulis sesudah `Hasil_OMI_3.md`. Butir 2 dan 3 eksploratif: dilaporkan terpisah dari hasil
pra-daftar dan tidak mengubah perbandingan utama atau model yang dikirim ke server penilai.

1. **ECG-FM tidak dijalankan.** Pengguna memutuskan 11 Nov 2026 tidak mencoba memasang `fairseq-signals` (tanpa
   dukungan resmi Windows; lisensi pustakanya tak tercantum). Sesuai P3 dicatat "tidak dijalankan" dan tidak diganti
   model lain. M3 terbaik = M3a, satu-satunya M3, jadi tidak ada optimisme dari pemilihan antarmodel M3.
2. **Strata `Time_Interval` (eksploratif).** EKG diambil sampai 7 hari sebelum angiografi; EKG yang jauh dari
   angiografi mungkin belum mencerminkan oklusi yang ditemukan. Analisis utama; batas kuartil dari semua EKG analisis
   utama yang punya `Time_Interval` (`pd.qcut`, 4); EKG tanpa nilai dihitung dan dikeluarkan. Per kuartil: n EKG,
   n OMI, AUROC M1, M2, M3a (rata-rata benih, prediksi out-of-fold yang sudah ada, tanpa latih ulang) dan selisih
   M3a − M2, dengan CI 95 % bootstrap bergugus pasien 2.000 di dalam kuartil (benih 20261113). Tanpa uji
   heterogenitas; dibaca deskriptif. Skrip `omi_waktu.py`.
3. **Kisi C diperlebar (kepekaan, eksploratif).** C terpilih M3a selalu 10⁻³, tepi bawah kisi. M3a analisis utama
   diulang dengan kisi {10⁻⁶, 10⁻⁵, 10⁻⁴} ∪ kisi terkunci; lipatan, benih, log-loss, dan bootstrap 2.000 (benih
   20261114) sama. Dilaporkan AUROC, AUPRC, Brier, Se@Sp90, slope, intercept, dan C terpilih. Hasil pra-daftar
   tetap yang dari kisi terkunci.
4. **Server penilai (rincian pelaksanaan, bukan perubahan).** Model = M3a dengan kisi terkunci: C dipilih dengan
   `pilih_C` atas semua EKG analisis utama (benih 20261107), model dilatih atas semua EKG itu, lalu diterapkan pada
   EKG `test.csv` (embedding dengan pra-proses yang sama; `test.csv` tidak punya kolom Paced, jadi semua EKG
   diprediksi). Ambang biner = rata-rata tiga ambang Sp90 out-of-fold (kuantil 0,9 skor bukan-OMI per benih, seperti
   `metrik`). Berkas CSV disiapkan asisten; unggah ke server (alamat di makalah data) dilakukan pengguna, sekali, dan
   hasilnya dicatat apa adanya.
