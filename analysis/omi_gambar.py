"""Gambar naskah OMI (Artikel_OMI_Rencana.md bagian F) dari prediksi out-of-fold yang sudah ada. Tanpa latih ulang.

Urutan sejak draf 8 (13 Nov 2026, panel 7: "no figure shows the headline result"):
Gambar 1  (a) Selisih AUROC berpasangan label oklusi − label infark untuk enam perbandingan, probe dan CNN, CI 95 %,
          disalin dari tabel G1 dan G2 Hasil_OMI_11.md, dengan pita ±0,03; (b) sejak draf 9 (panel 8): label oklusi
          lawan setiap pembanding untuk (c), probe, disalin dari Hasil_OMI_12.md (H1 STEMI, H2 enam kontrol, H3 jarak
          dalam model, H4(iii) berlapis kuartil jarak); (c) sejak draf 13 (panel 12): keunggulan tujuh label bersarang
          (enam kontrol + oklusi) atas probe berlabel infark, masing-masing dinilai terhadap labelnya sendiri
          (H8(i) Hasil_OMI_14.md), dengan pita 2,5–97,5 % keunggulan 100 label teracak (perm_h7.csv, H7(ii)).
          Sampai draf 12 panel (c) berisi sebaran AUROC dua nol permutasi.
Gambar 2  Selisih label per kuartil Time_Interval, disalin dari tabel F2 Hasil_OMI_10.md (bukan dihitung ulang).
Gambar 3  Kurva keputusan: (a) utama M2, M3a; (b) NSTEMI-OMI M2, M3a.
Gambar S1 ROC analisis utama (M0, M2, M3a) dan kalibrasi M2 dan M3a (desil prediksi); Gambar 1 sampai draf 7.
Sejak draf 7 (13 Nov 2026) M1 (fitur ST) tidak digambar: pengukurannya gagal cek STEMI dan hanya ada di Suplemen S1.

Kurva (Gambar 3, S1) memakai benih 20261107 saja; angka di naskah tetap rata-rata tiga benih dari Hasil_OMI_1–4.
Rumus net benefit sama dengan omi_m01.metrik: TP/n − FP/n · t/(1 − t).
Data di luar repo: $OMI_DATA. Keluaran: folder argumen pertama (PNG 300 dpi + PDF).

Pakai:
    python-gpu analysis/omi_gambar.py <folder_keluaran>
"""
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import roc_curve  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR  # noqa: E402

BENIH = 20261107
WARNA = {"M0": "#9e9e9e", "M1": "#e69f00", "M2": "#0072b2", "M3a": "#d55e00"}
NAMA = {"M0": "Age-sex model", "M1": "ST-amplitude model", "M2": "CNN",
        "M3a": "ECGFounder probe"}


def nb(y, p, t):
    n = len(y)
    return np.sum((p >= t) & (y == 1)) / n - np.sum((p >= t) & (y == 0)) / n * t / (1 - t)


def simpan(fig, keluar, nama):
    fig.savefig(keluar / f"{nama}.png", dpi=300, bbox_inches="tight")
    fig.savefig(keluar / f"{nama}.pdf", bbox_inches="tight")
    plt.close(fig)


def main(keluar):
    keluar = Path(keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    ut = tr[tr.Paced != 1].reset_index(drop=True)
    o1 = pd.read_csv(AKAR / "oof_m01.csv")
    assert (o1.ecg_med_record.values == ut.ecg_med_record.values).all()
    o2 = np.load(AKAR / "oof_m2_utama.npz", allow_pickle=True)
    assert (o2["ecg_row_record"] == ut.ecg_row_record.values).all()
    o3 = np.load(AKAR / "oof_m3a.npz")
    y = ut.OMI.values.astype(int)
    P = {"M0": o1[f"M0_{BENIH}"].values, "M1": o1[f"M1_{BENIH}"].values,
         "M2": o2[f"M2_{BENIH}"], "M3a": o3[f"utama_{BENIH}"]}

    # Gambar 1
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.6))
    for m, p in P.items():
        if m == "M1":
            continue
        f, t, _ = roc_curve(y, p)
        a.plot(f, t, color=WARNA[m], lw=1.6, label=NAMA[m])
    a.plot([0, 1], [0, 1], color="0.7", lw=0.8, ls="--")
    a.set(xlabel="1 − specificity", ylabel="Sensitivity", title="(a) ROC, OMI vs non-OMI")
    a.legend(fontsize=8, loc="lower right")
    for m in ["M2", "M3a"]:
        p = P[m]
        q = pd.qcut(p, 10, labels=False, duplicates="drop")
        mp = pd.Series(p).groupby(q).mean()
        my = pd.Series(y).groupby(q).mean()
        b.plot(mp, my, "o-", color=WARNA[m], ms=4, lw=1.2, label=NAMA[m])
    b.plot([0, 1], [0, 1], color="0.7", lw=0.8, ls="--")
    b.set(xscale="log", yscale="log", xlim=(5e-3, 1), ylim=(5e-3, 1), xlabel="Mean predicted probability (decile)",
          ylabel="Observed OMI proportion", title="(b) Calibration (no recalibration)")
    b.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    simpan(fig, keluar, "gambarS1_roc_kalibrasi")

    # Gambar 2
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.6))
    ts = np.linspace(0.005, 0.30, 120)
    prev = y.mean()
    for m in ["M2", "M3a"]:
        a.plot(ts * 100, [nb(y, P[m], t) for t in ts], color=WARNA[m], lw=1.6, label=NAMA[m])
    a.plot(ts * 100, prev - (1 - prev) * ts / (1 - ts), color="k", lw=1, ls="--", label="Treat all")
    a.axhline(0, color="0.5", lw=0.8, label="Treat none")
    a.set(ylim=(-0.01, prev + 0.01), xlabel="Threshold probability (%)", ylabel="Net benefit",
          title="(a) OMI vs non-OMI")
    a.legend(fontsize=8)
    o2n = np.load(AKAR / "oof_m2_nstemi.npz", allow_pickle=True)
    yn = o2n["OMI"].astype(int)
    pn = {"M2": o2n[f"M2_{BENIH}"], "M3a": o3[f"nstemi_{BENIH}"]}
    assert len(pn["M3a"]) == len(yn)
    from sklearn.metrics import roc_auc_score
    print("Cek urutan (AUROC benih ini, harus sama dengan 'Per benih' di Hasil_OMI_1–3): "
          + ", ".join(f"utama {m} {roc_auc_score(y, p):.3f}" for m, p in P.items()) + "; "
          + ", ".join(f"NSTEMI {m} {roc_auc_score(yn, p):.3f}" for m, p in pn.items()))
    ts = np.linspace(0.01, 0.60, 120)
    prevn = yn.mean()
    for m, p in pn.items():
        b.plot(ts * 100, [nb(yn, p, t) for t in ts], color=WARNA[m], lw=1.6, label=NAMA[m])
    b.plot(ts * 100, prevn - (1 - prevn) * ts / (1 - ts), color="k", lw=1, ls="--", label="Treat all")
    b.axhline(0, color="0.5", lw=0.8, label="Treat none")
    b.set(ylim=(-0.02, prevn + 0.02), xlabel="Threshold probability (%)", ylabel="Net benefit",
          title="(b) NSTEMI-OMI vs NSTEMI non-OMI")
    b.legend(fontsize=8)
    fig.tight_layout()
    simpan(fig, keluar, "gambar3_kurva_keputusan")

    # Gambar 2: disalin dari tabel F2 Hasil_OMI_10.md, baris (c)
    teks = (Path(__file__).parent.parent / "results" / "Hasil_OMI_10.md").read_text(encoding="utf-8")
    baris = re.findall(r"^\| (Q\d) \| \(c\) OMI lawan AMI tanpa OMI \| (\d+) / (\d+) \| (.*?) \| (.*?) \|$", teks, re.M)
    assert len(baris) == 4, baris
    sel = re.compile(r"(-?[\d.]+) \[(-?[\d.]+), (-?[\d.]+)\]")
    fig, a = plt.subplots(figsize=(6, 4.2))
    x = np.arange(4)
    for k, m in enumerate(["M3a", "M2"]):
        v = np.array([[float(z) for z in sel.match(r[3 + k]).groups()] for r in baris])
        a.errorbar(x + (k - 0.5) * 0.16, v[:, 0], yerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], fmt="o",
                   color=WARNA[m], capsize=3, ms=5, label=NAMA[m])
    a.axhline(0, color="0.5", lw=0.8)
    lab = ["Q1 (closest)", "Q2", "Q3", "Q4 (farthest)"]
    a.set_xticks(x, [f"{lab[i]}\n{r[1]} OMI / {r[2]} ECGs" for i, r in enumerate(baris)], fontsize=8)
    a.set(ylabel="AUROC difference, occlusion − infarction label",
          title="OMI vs infarction without occlusion, by ECG-to-angiography delay")
    a.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    simpan(fig, keluar, "gambar2_selisih_label_kuartil")
    gambar_utama(keluar)
    print(f"Gambar 1–3 dan S1 ditulis ke {keluar} (benih kurva {BENIH}).")


def gambar_utama(keluar):
    """Gambar 1: selisih label berpasangan (Hasil_OMI_11 G1, G2) dan dua nol permutasi."""
    teks = (Path(__file__).parent.parent / "results" / "Hasil_OMI_11.md").read_text(encoding="utf-8")
    sel = r"(-?[\d.]+ \[-?[\d.]+, -?[\d.]+\])"
    g2 = dict((k, (a, b)) for k, a, b in re.findall(
        r"^\| (.+?) \| \d+ / \d+ \| " + sel + r" \| " + sel + r" \|$", teks, re.M))
    g1 = dict((k, (a, b)) for k, a, b in re.findall(
        r"^\| (STEMI|NSTEMI) \| \d+ / \d+ \| [\d.]+ \| [\d.]+ \| " + sel + r" \| [\d.]+ \| [\d.]+ \| " + sel + r" \|$",
        teks, re.M))
    baris = [("OMI vs all other ECGs", g2["OMI lawan semua"]),
             ("OMI vs infarction without occlusion", g2["(c) OMI lawan AMI tanpa OMI"]),
             ("   within STEMI", g1["STEMI"]), ("   within NSTEMI", g1["NSTEMI"]),
             ("OMI vs no infarction", g2["OMI lawan tanpa infark"]),
             ("Infarction vs no infarction", g2["AMI lawan tanpa AMI"])]
    angka = re.compile(r"(-?[\d.]+) \[(-?[\d.]+), (-?[\d.]+)\]")
    # (b) sejak draf 9: label oklusi lawan setiap pembanding untuk (c), probe, dari Hasil_OMI_12 (H1–H4)
    h = (Path(__file__).parent.parent / "results" / "Hasil_OMI_12.md").read_text(encoding="utf-8")
    h1 = re.search(r"^\| \(c\) OMI lawan AMI tanpa OMI \| \d+ / \d+ \| [\d.]+ \| [\d.]+ \| " + sel + r" \|$", h, re.M)
    h2 = dict((k, v) for k, v in re.findall(
        r"^\| (.+?) \| \d+ \| [\d.]+ \| (?:ya|tidak) \| " + sel + r" \|$", h, re.M))
    h3 = re.search(r"\(c\), dengan jarak: " + sel, h)
    h4 = re.search(r"^probe: \(ii\) .*?; \(iii\) selisih AUROC berlapis kuartil " + sel, h, re.M)
    nama_k = {"PCI": "with PCI", "VF/VT": "with VF/VT", "usia >= median AMI": "age ≥ median",
              "laki-laki": "in men", "dekat angiografi (<= median AMI)": "delay ≤ median", "STEMI": "with discharge STEMI"}
    assert h1 and h3 and h4 and set(h2) == set(nama_k), (h1, h3, h4, h2)
    pemb = [("Infarction label", g2["(c) OMI lawan AMI tanpa OMI"][0]),
            ("Infarction label, delay in model", h3.group(1)),
            ("Infarction label, within delay quartiles", h4.group(1)),
            ("Discharge-STEMI comparator", h1.group(1))] + [("Control: infarction " + v, h2[k]) for k, v in nama_k.items()]
    fig, (a, c, b) = plt.subplots(1, 3, figsize=(16, 4.8), gridspec_kw={"width_ratios": [1.3, 1.3, 1]})
    yk = np.arange(len(baris))[::-1]
    a.axvspan(-0.03, 0.03, color="0.92", zorder=0, label="±0.03 equivalence margin")
    a.axvline(0, color="0.5", lw=0.8)
    for k, m in enumerate(["M3a", "M2"]):
        v = np.array([[float(z) for z in angka.match(r[1][k]).groups()] for r in baris])
        a.errorbar(v[:, 0], yk + (0.5 - k) * 0.24, xerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], fmt="o",
                   color=WARNA[m], capsize=3, ms=5, label=NAMA[m])
    a.set_yticks(yk, [r[0] for r in baris], fontsize=8)
    a.set(xlabel="AUROC difference, occlusion label − infarction label",
          title="(a) Paired label difference, scored for OMI")
    a.legend(fontsize=7.5, loc="lower right")
    yc = np.arange(len(pemb))[::-1]
    v = np.array([[float(z) for z in angka.match(r[1]).groups()] for r in pemb])
    c.axvspan(-0.03, 0.03, color="0.92", zorder=0)
    c.axvline(0, color="0.5", lw=0.8)
    c.errorbar(v[:, 0], yc, xerr=[v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], fmt="o", color=WARNA["M3a"], capsize=3, ms=5)
    c.set_yticks(yc, [r[0] for r in pemb], fontsize=8)
    c.set(xlabel="AUROC difference, occlusion label − comparator",
          title="(b) Probe, OMI vs infarction without occlusion")
    # (c) sejak draf 13 (panel 12): keunggulan tiap label bersarang klinis atas probe berlabel infark, dinilai
    # terhadap labelnya sendiri (Hasil_OMI_14 H8(i)), dengan rentang 2,5–97,5 % 100 label teracak (perm_h7.csv, H7(ii))
    h14 = (Path(__file__).parent.parent / "results" / "Hasil_OMI_14.md").read_text(encoding="utf-8")
    rows = dict(re.findall(r"^\| (.+?) \| \d+ / 2646 \| [\d.]+ \| [\d.]+ \| " + sel + r" \|$", h14, re.M))
    nama_c = {"OMI (label oklusi)": "Occlusion (OMI)", "usia >= median AMI": "Age ≥ median",
              "laki-laki": "Men", "STEMI": "Discharge STEMI", "VF/VT": "VF/VT",
              "dekat angiografi (<= median AMI)": "Delay ≤ median", "PCI": "PCI"}
    assert set(rows) == set(nama_c), rows
    urut = sorted(rows, key=lambda k: float(angka.match(rows[k]).group(1)))
    v = np.array([[float(z) for z in angka.match(rows[k]).groups()] for k in urut])
    acak = pd.read_csv(AKAR / "perm_h7.csv").keunggulan
    lo, hi = np.quantile(acak, [.025, .975])
    yb = np.arange(len(urut))
    b.axvspan(lo, hi, color="0.88", zorder=0, label="100 shuffled\nlabels, 2.5–97.5 %")
    b.axvline(0, color="0.5", lw=0.8)
    warna = [WARNA["M3a"] if k.startswith("OMI") else "0.35" for k in urut]
    for y_, r, w in zip(yb, v, warna):
        b.errorbar(r[0], y_, xerr=[[r[0] - r[1]], [r[2] - r[0]]], fmt="o", color=w, capsize=3, ms=5)
    b.set_yticks(yb, [nama_c[k] for k in urut], fontsize=8)
    b.set(xlabel="AUROC gain over the infarction-trained probe,\nscored on each label within infarction",
          title="(c) Nested labels, each on its own label")
    b.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    simpan(fig, keluar, "gambar1_selisih_label")


if __name__ == "__main__":
    main(sys.argv[1])
