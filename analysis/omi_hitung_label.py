"""Hitung ulang label dataset OMI Chongqing (Du dkk., Sci Data 13:1009; figshare 29925314, CC0).

Membaca train.csv dan test.csv dari $OMI_DATA/csv/CSV/ (di luar repo) dan mencetak
tabel Markdown yang disalin apa adanya ke Hasil_OMI_0.md. Tidak ada pemodelan di sini.

Pakai:
    python-gpu analysis/omi_hitung_label.py [folder_csv]
"""
import sys
from pathlib import Path

import pandas as pd

FOLDER = Path(sys.argv[1] if len(sys.argv) > 1 else "data/chongqing/csv/CSV")
TERITORI = {
    "LM": ["LM"],
    "LAD": ["PLAD", "MLAD", "DLAD", "DB"],
    "LCX": ["PLCX", "MLCX", "DLCX", "OM"],
    "RCA": ["PRCA", "MRCA", "DRCA"],
}
SEGMEN = [s for v in TERITORI.values() for s in v]


def baris(*kol):
    print("| " + " | ".join(str(k) for k in kol) + " |")


def main():
    tr = pd.read_csv(FOLDER / "train.csv", dtype={"Patient_id": str})
    te = pd.read_csv(FOLDER / "test.csv", dtype={"Patient_id": str})

    print("## 1. Ukuran berkas\n")
    baris("Berkas", "EKG (baris)", "Pasien unik", "Kolom")
    baris("---", "---", "---", "---")
    baris("train.csv", len(tr), tr.Patient_id.nunique(), len(tr.columns))
    baris("test.csv", len(te), te.Patient_id.nunique(), len(te.columns))
    irisan = set(tr.Patient_id) & set(te.Patient_id)
    print(f"\nPasien di latih dan uji sekaligus: {len(irisan)}. "
          f"Rekaman `.dat` ganda di latih: {tr.ecg_row_record.duplicated().sum()}.\n")

    print("## 2. Label biner di train.csv (nilai 1)\n")
    baris("Kolom", "n = 1", "% EKG", "nilai unik")
    baris("---", "---", "---", "---")
    for k in ["AMI", "OMI", "STEMI", "NSTEMI", "UA", "CTO", "PCI", "VF_VT", "Paced", "Prior_PCI"]:
        baris(k, int((tr[k] == 1).sum()), f"{100 * (tr[k] == 1).mean():.2f}", sorted(tr[k].dropna().unique().tolist()))

    print("\n## 3. Silang OMI × jenis SKA (train.csv)\n")
    jenis = (tr.STEMI.astype(str) + tr.NSTEMI.astype(str) + tr.UA.astype(str))
    nama = {"100": "STEMI", "010": "NSTEMI", "001": "UA", "000": "bukan SKA"}
    tr["_jenis"] = jenis.map(nama).fillna("ganda:" + jenis)
    tab = pd.crosstab(tr["_jenis"], tr["OMI"])
    baris("Jenis", "OMI = 0", "OMI = 1", "Jumlah")
    baris("---", "---", "---", "---")
    for j, r in tab.iterrows():
        baris(j, r.get(0, 0), r.get(1, 0), r.sum())
    baris("**Jumlah**", int(tab.get(0, pd.Series()).sum()), int(tab.get(1, pd.Series()).sum()), int(tab.values.sum()))

    print("\n## 4. Pembuluh penyebab pada EKG OMI = 1 (train.csv)\n")
    omi = tr[tr.OMI == 1]
    akut = (omi[SEGMEN] == 1)
    ter = pd.DataFrame({t: akut[s].any(axis=1) for t, s in TERITORI.items()})
    jml = ter.sum(axis=1)
    print(f"Nilai segmen yang muncul: {sorted(pd.unique(tr[SEGMEN].values.ravel()).tolist())} "
          f"(1 = oklusi akut, 2 = CTO menurut makalah).\n")
    baris("Kelompok", "n EKG OMI")
    baris("---", "---")
    baris("tanpa segmen akut", int((jml == 0).sum()))
    baris("satu teritori", int((jml == 1).sum()))
    baris("lebih dari satu teritori", int((jml > 1).sum()))
    for t in TERITORI:
        baris(f"satu teritori: {t}", int(((jml == 1) & ter[t]).sum()))
    print("\nSatu teritori, dipecah per jenis SKA:\n")
    baris("Jenis", *TERITORI.keys())
    baris("---", *["---"] * len(TERITORI))
    for j in ["STEMI", "NSTEMI", "UA", "bukan SKA"]:
        m = (omi["_jenis"] == j) & (jml == 1)
        baris(j, *[int((m & ter[t]).sum()) for t in TERITORI])

    print("\n## 5. Demografi dan Time_Interval\n")
    baris("Berkas", "usia median (IQR)", "usia hilang", "laki-laki (gender=1) %", "Time_Interval median (IQR)")
    baris("---", "---", "---", "---", "---")
    for nm, d in [("train", tr), ("test", te)]:
        q = d.age.quantile([.25, .5, .75])
        t = d.Time_Interval.quantile([.25, .5, .75])
        baris(nm, f"{q[.5]:.0f} ({q[.25]:.0f}–{q[.75]:.0f})", int(d.age.isna().sum()),
              f"{100 * (d.gender == 1).mean():.2f}", f"{t[.5]:.0f} ({t[.25]:.0f}–{t[.75]:.0f})")
    epp = tr.groupby("Patient_id").size()
    print(f"\nEKG per pasien (latih): maks {epp.max()}, pasien dengan > 1 EKG: {(epp > 1).sum()}.")


if __name__ == "__main__":
    main()
