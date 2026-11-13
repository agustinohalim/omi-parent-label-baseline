# Hasil OMI 5 — cek tata letak .med dan titik J untuk ciri ST M1 (12 November 2026)

> Satu-satunya sumber angka bagian ini. Menutup butir ⬜ di `Hasil_OMI_1.md` §7 ("ketepatan titik J terhadap
> anotasi manual pada sampel") sebelum angka M1 masuk naskah. Di luar pra-daftar, deskriptif, tanpa label: tidak ada
> kolom hasil yang dibaca, tidak ada ciri atau model yang diubah. Skrip `omi_cek_titik_j.py` (komit 3fff109; butir 3
> ditambahkan di dd7a394 sesudah gambar dilihat, lalu seluruh skrip dijalankan ulang). Log dan gambar di scratchpad
> sesi (`titik_j.log`, `titik_j_1.png`, `titik_j_2.png`), tidak masuk repo. **Pembaca gambar adalah asisten AI
> (Claude), bukan manusia, dan bukan anotasi manual titik J oleh ahli EKG.**

## 1. Tata letak berkas .med (objektif)

Bila susunan sadapan benar, hukum Einthoven berlaku per sampel. Analisis utama, n EKG = 17.622. Galat relatif =
rata-rata |selisih| / rata-rata |amplitudo| enam sadapan ekstremitas.

| Susunan | III − (II − I), median | p95 | aVR + (I + II)/2, median | p95 |
| --- | --- | --- | --- | --- |
| dipakai `omi_ciri_st.py`: (500, 12).T | 0.0000 | 0.0000 | 0.0055 | 0.0104 |
| alternatif (12, 500) | 0.7962 | 1.8785 | 0.6793 | 1.2545 |

Susunan yang dipakai benar: III = II − I tepat (sadapan turunan dihitung perangkat), aVR sesuai sampai galat
pembulatan. Urutan sadapan I, II, III, aVR di empat kolom pertama juga terkonfirmasi.

## 2. Titik J pada 30 EKG acak (visual, asisten AI)

Sampel: 30 dari 17.497 EKG analisis utama berstatus ciri "ok", benih 20261115 (daftar berkas di log). Tiap panel:
12 sadapan ditumpuk sesudah dikurangi garis PR, penanda awal QRS, titik J, dan J+60 ms.

| Pemeriksaan | Hasil |
| --- | --- |
| Awal QRS pada defleksi pertama | 30/30; beberapa 2–6 ms lebih awal, tidak mengubah garis PR (jendela 10–30 ms sebelumnya) |
| Titik J di akhir QRS (semua sadapan sudah kembali ke segmen ST) | 29/30 dalam ±10 ms; 1 (06835.med) ±5–10 ms terlalu awal, J+60 tetap di segmen ST |
| Titik J jatuh di tengah QRS atau di gelombang T | 0/30 |
| Satu sadapan berartefak berat | 1/30: 07712.med, V6 ±15 mV (ST60 V6 = 6,34 mV); sadapan lain normal |
| Garis dasar melayang di satu sadapan | 2/30: 09314.med (V6), 17610.med (V5/V6) |

Rentang QRS sampel 72–102 ms, sesuai median 84 ms seluruh data (`Hasil_OMI_1.md` §6).

## 3. Nilai ST60 tidak fisiologis (artefak), seluruh data

EKG berstatus ok, analisis utama, n = 17.497; |ST60| maksimum di 12 sadapan.

| Ambang | n EKG dengan sadapan mana pun di atas ambang | % |
| --- | --- | --- |
| > 0.5 mV | 459 | 2.62 |
| > 1 mV | 143 | 0.82 |
| > 2 mV | 74 | 0.42 |
| > 5 mV | 54 | 0.31 |

## 4. Bacaan

- **Ciri ST M1 tidak rusak secara sistematis.** Tata letak .med benar (bukti objektif), dan penempatan titik J dapat
  diterima pada 29–30 dari 30 EKG menurut pembacaan asisten. Kesimpulan `Hasil_OMI_1.md` §7 ("sinyal ST lemah pada
  data ini, bukan ciri yang rusak") bertahan, dengan catatan bahwa ini bukan anotasi ahli.
- **Ada artefak sadapan tunggal** pada sebagian kecil EKG (0,42 % dengan |ST60| > 2 mV, nilai yang hampir pasti
  bukan fisiologis). Algoritme pra-daftar (P1) tidak menyaring artefak. Pengaruhnya pada AUROC M1 kemungkinan kecil:
  satu ciri ST60 maks, yang berbasis peringkat, sudah memberi 0,602 (`Hasil_OMI_1.md` §6), dan model M1 sangat
  teregularisasi. Tidak diuji ulang (akan menjadi analisis pasca-hasil); ditulis di Limitations naskah.
- Angka M1 boleh masuk naskah dengan dua kalimat batasan: titik J otomatis diperiksa pada sampel oleh pembaca non-ahli
  (AI), dan artefak satu sadapan tidak disaring.
