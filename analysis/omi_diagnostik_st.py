"""Diagnostik ciri ST OMI — DI LUAR PRA-DAFTAR (11 Nov 2026), deskriptif saja.

Ditulis sesudah M1 memberi AUROC 0,615, untuk memeriksa apakah ciri ST rusak atau sinyalnya memang lemah.
Tidak melatih model apa pun dan tidak mengubah analisis terdaftar.

1. Median ST60 maksimum (11 sadapan, tanpa aVR), ST60 V2, ST60 II, dan QRS per jenis SKA.
2. AUROC ST60 maksimum: STEMI lawan bukan-SKA, dan OMI lawan bukan-OMI.
3. Bagian EKG dengan ST60 maksimum > 0,1 mV per jenis.
4. AUROC ST60 maksimum untuk OMI per kuartil Time_Interval.

Populasi = analisis utama (tanpa Paced) dengan status ciri 'ok'.

Pakai: python omi_diagnostik_st.py $OMI_DATA
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score

akar = Path(sys.argv[1])
tr = pd.read_csv(akar / "csv/CSV/train.csv", dtype={"Patient_id": str})
st = pd.read_csv(akar / "ciri_st_train.csv")
assert (tr.ecg_med_record.values == st.ecg_med_record.values).all()
d = pd.concat([tr, st.drop(columns="ecg_med_record")], axis=1)
d = d[(d.Paced != 1) & (d.status == "ok")].copy()
L = ["I", "II", "III", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
d["maxST"] = d[[f"st60_{l}" for l in L]].max(axis=1)
jenis = {"STEMI": d.STEMI == 1, "NSTEMI": d.NSTEMI == 1, "UA": d.UA == 1,
         "bukan SKA": (d.STEMI + d.NSTEMI + d.UA) == 0}

print(f"n EKG = {len(d)}\n")
print("| Jenis | n | ST60 maks median (mV) | ST60 V2 median | ST60 II median | QRS median (ms) | ST60 maks > 0,1 mV |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for k, m in jenis.items():
    g = d[m]
    print(f"| {k} | {len(g)} | {g.maxST.median():.3f} | {g.st60_V2.median():.3f} | {g.st60_II.median():.3f} "
          f"| {g.qrs_ms.median():.0f} | {(g.maxST > 0.1).mean():.3f} |")

m = jenis["STEMI"] | jenis["bukan SKA"]
print(f"\nAUROC ST60 maks, STEMI lawan bukan SKA: {roc_auc_score(jenis['STEMI'][m], d.maxST[m]):.3f}")
print(f"AUROC ST60 maks, OMI lawan bukan-OMI: {roc_auc_score(d.OMI, d.maxST):.3f}\n")

d["kuartil"] = pd.qcut(d.Time_Interval, 4)
print("| Time_Interval (kuartil) | n | OMI % | AUROC ST60 maks (OMI) |")
print("| --- | --- | --- | --- |")
for b, g in d.groupby("kuartil", observed=True):
    print(f"| {b} | {len(g)} | {100 * g.OMI.mean():.1f} | {roc_auc_score(g.OMI, g.maxST):.3f} |")
