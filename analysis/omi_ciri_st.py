"""Ciri ST M1 untuk artikel OMI: amplitudo J+60 dan J+80 ms terhadap garis PR, 12 sadapan, dari denyut median.

Algoritme ditetapkan di Prareg_OMI.md, Penyimpangan P1 (11 Nov 2026), sebelum model dilatih. Skrip ini tidak
membaca label. Data di luar repo:
    $OMI_DATA/csv/CSV/train.csv
    $OMI_DATA/med/med_data/<id>.med   (dari ECG_median_data.zip)
Keluaran (di luar repo): $OMI_DATA/ciri_st_train.csv; ringkasan QC dicetak sebagai Markdown.

Pakai:
    python-gpu analysis/omi_ciri_st.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

import os  # noqa: E402
AKAR = Path(os.environ.get("OMI_DATA", "data/chongqing"))
SADAPAN = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
FS = 500


def baca_med(berkas):
    a = np.fromfile(berkas, dtype="<i2")
    return a.reshape(500, 12).T.astype(float)  # (12, 500), µV


def deteksi(x):
    """Kembalikan (r, awal_qrs, j) dalam indeks sampel, atau None bila gagal."""
    d = np.abs(np.diff(x, axis=1)).sum(0)
    d = np.convolve(d, np.ones(5) / 5, "same")
    v = np.abs(x - np.median(x, axis=1, keepdims=True)).sum(0)
    r = 150 + int(np.argmax(v[150:350]))
    lo, hi = max(r - 75, 1), min(r + 100, len(d))
    thr = 0.15 * d[lo:hi].max()
    awal = next((i - 5 for i in range(r, lo + 4, -1) if np.all(d[i - 5:i] < thr)), None)
    j = next((i for i in range(r, hi - 5) if np.all(d[i:i + 5] < thr)), None)
    if awal is None or j is None:
        return None
    return r, awal, j


def ciri(x):
    h = deteksi(x)
    if h is None:
        return None, "gagal"
    _, awal, j = h
    qrs_ms = (j - awal) * 1000 / FS
    if qrs_ms < 50 or qrs_ms > 200:
        return None, "qrs_di_luar"
    i60, i80 = j + 30, j + 40
    if i80 >= x.shape[1] or awal - 15 < 0:
        return None, "di_luar_jendela"
    pr = x[:, awal - 15:awal - 5].mean(axis=1)
    st60 = (x[:, i60] - pr) / 1000.0
    st80 = (x[:, i80] - pr) / 1000.0
    return np.concatenate([st60, st80, [qrs_ms]]), "ok"


def main():
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    kol = [f"st60_{s}" for s in SADAPAN] + [f"st80_{s}" for s in SADAPAN] + ["qrs_ms"]
    baris, status = [], []
    for rec in tr.ecg_med_record:
        f, st = ciri(baca_med(AKAR / "med/med_data" / rec))
        status.append(st)
        baris.append(f if f is not None else np.full(len(kol), np.nan))
    out = pd.DataFrame(baris, columns=kol)
    out.insert(0, "ecg_med_record", tr.ecg_med_record.values)
    out["status"] = status
    out.to_csv(AKAR / "ciri_st_train.csv", index=False)

    print("| Status deteksi | n EKG |")
    print("| --- | --- |")
    for k, n in pd.Series(status).value_counts().items():
        print(f"| {k} | {n} |")
    q = out.qrs_ms.dropna()
    print(f"\nDurasi QRS (ms), EKG lolos: median {q.median():.0f}, persentil 5–95 {q.quantile(.05):.0f}–"
          f"{q.quantile(.95):.0f}; n = {len(q)} dari {len(out)}.")


if __name__ == "__main__":
    main()
