"""Fase D OMI (Prareg_OMI_D.md, terkunci 13 Nov 2026): kelompok pembanding, probe label AMI, uji eksternal STAFF III.

Masukan di luar repo:
  $OMI_DATA/  csv/CSV/train.csv, oof_m01.csv, oof_m2_utama.npz, oof_m3a.npz, emb_ecgfounder_train.npy
  $STAFF3_DATA/meta/  STAFF-III-Database-Annotations.xlsx, <rec>.hea, <rec>.event (PhysioNet staffiii 1.0.0)
  $STAFF3_DATA/seg/   potongan 10 s (byte-range, dari --unduh)

D1  AUROC kelompok pembanding dipecah (STEMI / NSTEMI / PCI) dan per kuartil Time_Interval dan jenis kelamin.
D2  probe ECGFounder dengan sasaran AMI (prosedur fase A), dinilai untuk OMI; selisih dengan probe-OMI.
D3  STAFF III: skor probe-OMI dan probe-AMI akhir, baseline cath lab lawan akhir inflasi balon, berpasangan.

Pakai:
  python omi_fase_d.py --butir D1,D2 [--B 2000]        # Python sistem
  python omi_fase_d.py --unduh                          # potongan STAFF III (byte-range), Python sistem
  python-gpu omi_fase_d.py --embed-staff3          # embedding ECGFounder potongan STAFF III
  python omi_fase_d.py --butir D3 [--B 2000]            # probe-OMI dan probe-AMI akhir dilatih di sini
"""
import argparse
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, indeks_bootstrap, oof, pilih_C, pipa  # noqa: E402
from omi_konstruk import beda_auc, muat, sel  # noqa: E402

import os  # noqa: E402
S3 = Path(os.environ.get("STAFF3_DATA", "data/staffiii"))
URL = "https://physionet.org/files/staffiii/1.0.0/data/"
UA = "journal-fit-check/0.1"
BUANG = {1, 4, 5, 6, 89}  # spreadsheet: sadapan mungkin tertukar atau terbalik
FS, GAIN, NSAD, OFFSET = 1000, 1600.0, 9, 512
NSEG = 10 * FS
EMB_S3 = S3 / "emb_ecgfounder_staff3.npy"
META_S3 = S3 / "segmen_staff3.csv"
RENCANA_S3 = S3 / "rencana_staff3.csv"
BUANG_S3 = S3 / "buang_staff3.csv"


# ---------------------------------------------------------------- umum
def auc_ci(y, g, pr, rng, B):
    """pr: {model: [p_benih...]}. Titik = rerata AUROC antarbenih; CI bootstrap bergugus pasien."""
    titik = {m: np.mean([roc_auc_score(y, p) for p in ps]) for m, ps in pr.items()}
    v = {m: [] for m in pr}
    for idx in indeks_bootstrap(g, rng, B):
        if len(np.unique(y[idx])) < 2:
            continue
        for m, ps in pr.items():
            v[m].append(np.mean([roc_auc_score(y[idx], p[idx]) for p in ps]))
    return {m: (titik[m], np.quantile(v[m], .025), np.quantile(v[m], .975)) for m in pr}


def kelompok(ut):
    o, a = ut.OMI.values.astype(int), ut.AMI.values.astype(int)
    return np.where(o == 1, 2, np.where(a == 1, 1, 0))  # 2 OMI, 1 AMI tanpa OMI, 0 tanpa AMI


# ---------------------------------------------------------------- D1
def d1(ut, P, B):
    print("## D1. Kelompok pembanding dipecah (skor OMI kohort penuh)\n")
    kel, g_all = kelompok(ut), ut.Patient_id.values
    rng = np.random.default_rng(20261123)
    st, ns, pci = (ut.STEMI == 1).values, (ut.NSTEMI == 1).values, (ut.PCI == 1).values
    uji = {"(b1) AMI tanpa OMI, STEMI": (kel == 1) & st,
           "(b2) AMI tanpa OMI, NSTEMI": (kel == 1) & ns,
           "(b3) AMI tanpa OMI, PCI = 1": (kel == 1) & pci,
           "(b4) AMI tanpa OMI, PCI = 0": (kel == 1) & ~pci,
           "(b5) AMI tanpa OMI, NSTEMI dan PCI = 0": (kel == 1) & ns & ~pci,
           "(b) AMI tanpa OMI, semua": kel == 1}
    print("Pembanding: tanpa AMI (n = %d).\n" % np.sum(kel == 0))
    print("| Kelompok uji | n EKG uji | " + " | ".join(P) + " |")
    print("| --- | --- | " + " | ".join("---" for _ in P) + " |")
    for nama, m in uji.items():
        s = np.flatnonzero(m | (kel == 0))
        y = m[s].astype(int)
        r = auc_ci(y, g_all[s], {k: [p[s] for p in ps] for k, ps in P.items()}, rng, B)
        print(f"| {nama} | {m.sum()} | " + " | ".join(sel(*r[k]) for k in P) + " |")
    print()
    dua = {k: P[k] for k in ("M2", "M3a")}
    perb = {"(a) OMI lawan tanpa AMI": (2, 0), "(b) AMI tanpa OMI lawan tanpa AMI": (1, 0),
            "(c) OMI lawan AMI tanpa OMI": (2, 1)}
    q = pd.qcut(ut.Time_Interval, 4, labels=["Q1", "Q2", "Q3", "Q4"]).astype(str).values
    lapis = [(f"kuartil {k}", q == k) for k in ["Q1", "Q2", "Q3", "Q4"]] + \
            [("laki-laki", (ut.gender == 1).values), ("perempuan", (ut.gender == 0).values)]
    print("Per kuartil Time_Interval (batas P4) dan jenis kelamin, M2 dan M3a:\n")
    print("| Lapis | Pasangan | n pos / n neg | M2 | M3a |")
    print("| --- | --- | --- | --- | --- |")
    for ln, lm in lapis:
        for pn, (pos, neg) in perb.items():
            s = np.flatnonzero(lm & ((kel == pos) | (kel == neg)))
            y = (kel[s] == pos).astype(int)
            r = auc_ci(y, g_all[s], {k: [p[s] for p in ps] for k, ps in dua.items()}, rng, B)
            print(f"| {ln} | {pn} | {y.sum()} / {len(y) - y.sum()} | {sel(*r['M2'])} | {sel(*r['M3a'])} |",
                  flush=True)
    print()


# ---------------------------------------------------------------- D2
def emb_utama(ut):
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    E = np.load(AKAR / "emb_ecgfounder_train.npy")
    assert E.shape == (len(tr), 1024)
    E = E[np.flatnonzero((tr.Paced != 1).values)]
    assert len(E) == len(ut)
    return E


def d2(ut, P, B):
    print("## D2. Probe ECGFounder dengan sasaran AMI (prosedur fase A)\n")
    t0 = time.time()
    E, g = emb_utama(ut), ut.Patient_id.values
    ya = ut.AMI.values.astype(int)
    hasil = [oof(E, ya, g, b, True) for b in BENIH]
    pa = [h[0][:, 1] for h in hasil]
    Cs = sorted({c for h in hasil for c in h[1]})
    np.savez(AKAR / "oof_m3a_ami.npz", **{f"ami_{b}": p for b, p in zip(BENIH, pa)})
    print(f"Latih: {(time.time() - t0) / 60:.1f} menit. C terpilih: {Cs}.\n")
    rng = np.random.default_rng(20261124)
    kel = kelompok(ut)
    pr = {"probe-OMI (M3a)": P["M3a"], "probe-AMI": pa}
    sas = {"OMI lawan semua": np.ones(len(ut), bool), "(c) OMI lawan AMI tanpa OMI": kel >= 1,
           "AMI lawan tanpa AMI": np.ones(len(ut), bool)}
    print("| Sasaran | n pos / n | probe-OMI | probe-AMI | selisih OMI − AMI |")
    print("| --- | --- | --- | --- | --- |")
    for nama, m in sas.items():
        s = np.flatnonzero(m)
        y = (ut.AMI.values[s] if nama.startswith("AMI") else ut.OMI.values[s]).astype(int)
        r = auc_ci(y, g[s], {k: [p[s] for p in ps] for k, ps in pr.items()}, rng, B)
        t, lo, hi, n = beda_auc(y, g[s], [p[s] for p in P["M3a"]], [p[s] for p in pa], rng, B)
        print(f"| {nama} | {y.sum()} / {len(y)} | {sel(*r['probe-OMI (M3a)'])} | {sel(*r['probe-AMI'])} | "
              f"{sel(t, lo, hi)} |", flush=True)
    print(f"\nPer benih AUROC probe-AMI untuk OMI lawan semua: "
          + ", ".join(f"{roc_auc_score(ut.OMI, p):.3f}" for p in pa) + ".\n")


# ---------------------------------------------------------------- D3: data STAFF III
def rek(kode):
    """'1c' -> '001c'."""
    k = str(kode).strip()
    return f"{int(k[:-1]):03d}{k[-1]}"


def tabel_staff3():
    import openpyxl
    wb = openpyxl.load_workbook(S3 / "meta/STAFF-III-Database-Annotations.xlsx", read_only=True)
    out = []
    for r in wb.worksheets[0].iter_rows(values_only=True):
        if not isinstance(r[0], int) or r[6] is None:
            continue
        d0, d1_, _ = (float(x) for x in str(r[8]).split(";"))
        art = str(r[7] or "")
        out.append({"pasien": r[0], "usia": r[1], "jk": str(r[2]).strip().lower(),
                    "bc1": rek(r[4]) if r[4] else None, "bi1": rek(r[6]), "arteri_teks": art,
                    "arteri": "LAD" if "LAD" in art else "RCA" if "RCA" in art else
                    "sirkumfleks" if "circ" in art.lower() else "lainnya",
                    "D0": d0, "D1": d1_, "infark_lama": str(r[28]).strip().lower() != "no"})
    return pd.DataFrame(out)


def panjang(rec):
    return int((S3 / "meta" / f"{rec}.hea").read_text().split()[3])


def rencana_segmen():
    import wfdb
    t = tabel_staff3()
    baris, buang = [], []
    for _, r in t.iterrows():
        if r.pasien in BUANG:
            buang.append((r.pasien, "sadapan bermasalah (spreadsheet)"))
            continue
        if pd.isna(r.bc1):
            buang.append((r.pasien, "tanpa BC1"))
            continue
        nb = panjang(r.bc1)
        a_base = (nb // 2 // FS) * FS
        ni = panjang(r.bi1)
        target = int(round((r.D0 + r.D1) * FS))
        sumber = "D0 + D1"
        ev = S3 / "meta" / f"{r.bi1}.event"
        if ev.exists():
            an = wfdb.rdann(str(S3 / "meta" / r.bi1), "event")
            defl = [s for s, n in zip(an.sample, an.aux_note) if "deflation" in str(n).lower()]
            if defl:
                d = min(defl, key=lambda s: abs(s - target))
                sumber = f"event (selisih dari D0 + D1 {abs(d - target) / FS:.1f} s)"
                target = int(d)
        a_inf = target - FS - NSEG
        if a_base + NSEG > nb or a_inf < 0 or a_inf + NSEG > ni:
            buang.append((r.pasien, "segmen di luar batas rekaman"))
            continue
        baris.append({**r.to_dict(), "awal_base": a_base, "awal_inf": a_inf, "sumber_deflasi": sumber})
    return pd.DataFrame(baris), buang


def unduh():
    seg, buang = rencana_segmen()
    (S3 / "seg").mkdir(exist_ok=True)
    total = 0
    for _, r in seg.iterrows():
        for rec, a in [(r.bc1, r.awal_base), (r.bi1, r.awal_inf)]:
            f = S3 / "seg" / f"{rec}_{a}.bin"
            if f.exists() and f.stat().st_size == NSEG * NSAD * 2:
                continue
            b0 = OFFSET + a * NSAD * 2
            req = urllib.request.Request(URL + f"{rec}.dat", headers={
                "User-Agent": UA, "Range": f"bytes={b0}-{b0 + NSEG * NSAD * 2 - 1}"})
            with urllib.request.urlopen(req, timeout=60) as h:
                assert h.status == 206, (rec, h.status)
                isi = h.read()
            assert len(isi) == NSEG * NSAD * 2, (rec, len(isi))
            f.write_bytes(isi)
            total += len(isi)
    seg.to_csv(RENCANA_S3, index=False)  # dibaca --embed-staff3 (venv-gpu tanpa wfdb)
    pd.DataFrame(buang, columns=["pasien", "alasan"]).to_csv(BUANG_S3, index=False)
    print(f"Pasien dengan pasangan segmen: {len(seg)}; dibuang sebelum unduh: {len(buang)} {buang}. "
          f"Diunduh sekarang: {total / 1e6:.1f} MB.")


def baca_seg(rec, a):
    """-> (12, 5000) mV di 500 Hz, urutan I, II, III, aVR, aVL, aVF, V1–V6; dan status mutu."""
    from scipy.signal import resample_poly
    x = np.frombuffer((S3 / "seg" / f"{rec}_{a}.bin").read_bytes(), dtype="<i2").reshape(NSEG, NSAD).T
    x = x.astype(np.float64) / GAIN  # V1..V6, I, II, III
    datar = 0
    for c in x:
        sama = np.flatnonzero(np.diff(c) != 0)
        batas = np.concatenate([[-1], sama, [len(c) - 1]])
        datar = max(datar, int(np.max(np.diff(batas))))
    v, I, II, III = x[:6], x[6], x[7], x[8]
    d = np.vstack([I, II, III, -(I + II) / 2, I - II / 2, II - I / 2, v])
    d = resample_poly(d, 1, 2, axis=1)
    assert d.shape == (12, 5000)
    return d, datar > FS


def embed_staff3():
    import torch
    from omi_m3_ecgfounder import BOBOT, KODE, praproses
    sys.path.insert(0, str(KODE))
    from net1d import Net1D
    seg = pd.read_csv(RENCANA_S3)
    buang = list(pd.read_csv(BUANG_S3).itertuples(index=False, name=None))
    X, ok = [], []
    for _, r in seg.iterrows():
        b, fb = baca_seg(r.bc1, r.awal_base)
        i, fi = baca_seg(r.bi1, r.awal_inf)
        ok.append(not (fb or fi))
        X += [praproses(b).astype(np.float32), praproses(i).astype(np.float32)]
    seg["mutu_ok"] = ok
    m = Net1D(in_channels=12, base_filters=64, ratio=1, filter_list=[64, 160, 160, 400, 400, 1024, 1024],
              m_blocks_list=[2, 2, 2, 3, 3, 4, 4], kernel_size=16, stride=2, groups_width=16, verbose=False,
              use_bn=False, use_do=False, n_classes=150, return_features=True)
    import numpy.core.multiarray as nca
    izin = ([(nca.scalar, "numpy.core.multiarray.scalar"), np.dtype]
            + [getattr(np.dtypes, n) for n in dir(np.dtypes) if n.endswith("DType")])
    with torch.serialization.safe_globals(izin):
        ck = torch.load(BOBOT, map_location="cpu", weights_only=True)
    hilang, lebih = m.load_state_dict(ck["state_dict"], strict=False)
    assert not [k for k in hilang if not k.startswith("dense.")], "bobot tidak termuat"
    print(f"Muat bobot: kunci hilang {len(hilang)}, kunci lebih {len(lebih)}.")
    m.to(torch.device("cuda")).eval()
    E = []
    with torch.no_grad():
        for k in range(0, len(X), 32):
            _, f = m(torch.from_numpy(np.stack(X[k:k + 32])).cuda())
            E.append(f.cpu().numpy())
    E = np.concatenate(E)
    assert E.shape == (2 * len(seg), 1024) and np.isfinite(E).all()
    np.save(EMB_S3, E)  # baris 2k = baseline, 2k+1 = akhir inflasi
    seg.to_csv(META_S3, index=False)
    print(f"Embedding STAFF III {E.shape}; pasangan {len(seg)}, mutu tidak ok {int((~seg.mutu_ok).sum())}; "
          f"dibuang sebelum segmen {len(buang)}: {buang}.")


# ---------------------------------------------------------------- D3: analisis
def d3(ut, B):
    from scipy.stats import wilcoxon
    print("## D3. STAFF III: baseline cath lab lawan akhir inflasi balon\n")
    seg = pd.read_csv(META_S3)
    E3 = np.load(EMB_S3)
    print(f"Pasangan tersegmen: {len(seg)}. Mutu tidak ok (nilai konstan > 1 s): "
          f"{int((~seg.mutu_ok).sum())} pasien {seg.pasien[~seg.mutu_ok].tolist()}, dibuang.\n")
    pakai = seg.mutu_ok.values
    seg = seg[pakai].reset_index(drop=True)
    E3 = E3.reshape(-1, 2, 1024)[pakai]
    print("Sumber penanda deflasi: " + "; ".join(f"{k}: {v}" for k, v in seg.sumber_deflasi.str.split(" ").str[0]
                                                    .value_counts().items())
          + f". Selisih event dari D0 + D1 terbesar: {seg.sumber_deflasi.str.extract(r'([0-9.]+) s')[0].astype(float).max()} s.\n")
    E, g = emb_utama(ut), ut.Patient_id.values
    kel = kelompok(ut)
    skor = {}
    print("| Model | sasaran latih | C | n latih |")
    print("| --- | --- | --- | --- |")
    for nama, kol in [("probe-OMI", "OMI"), ("probe-AMI", "AMI")]:
        y = ut[kol].values.astype(int)
        C = pilih_C(E, y, g, BENIH[0])
        mdl = pipa(C).fit(E, y)
        print(f"| {nama} | {kol} | {C} | {len(y)} |")
        lg = np.stack([mdl.decision_function(E3[:, 0]), mdl.decision_function(E3[:, 1])], 1)
        lg_cq = mdl.decision_function(E)
        skor[nama] = (lg, lg_cq)
    print()
    rng = np.random.default_rng(20261125)
    n = len(seg)
    boot = [rng.integers(0, n, n) for _ in range(B)]

    def ci(f):
        v = np.array([f(ix) for ix in boot])
        return np.quantile(v, .025), np.quantile(v, .975)

    def sig(z):
        return 1 / (1 + np.exp(-z))

    print("| Model | skala | median baseline | median akhir inflasi | rerata perubahan | bagian naik | "
          "AUROC akhir inflasi lawan baseline | Wilcoxon p |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for nama, (lg, _) in skor.items():
        for sk, s in [("logit", lg), ("peluang", sig(lg))]:
            d = s[:, 1] - s[:, 0]
            yy = np.r_[np.zeros(n), np.ones(n)]

            def au(ix, s=s):
                return roc_auc_score(np.r_[np.zeros(len(ix)), np.ones(len(ix))], np.r_[s[ix, 0], s[ix, 1]])
            print(f"| {nama} | {sk} | {np.median(s[:, 0]):.3f} | {np.median(s[:, 1]):.3f} | "
                  f"{sel(d.mean(), *ci(lambda ix, d=d: d[ix].mean()))} | "
                  f"{sel((d > 0).mean(), *ci(lambda ix, d=d: (d[ix] > 0).mean()))} | "
                  f"{sel(roc_auc_score(yy, np.r_[s[:, 0], s[:, 1]]), *ci(au))} | {wilcoxon(d).pvalue:.2g} |")
    do, da = (skor["probe-OMI"][0][:, 1] - skor["probe-OMI"][0][:, 0],
              skor["probe-AMI"][0][:, 1] - skor["probe-AMI"][0][:, 0])
    print(f"\nSelisih rerata perubahan logit probe-OMI − probe-AMI (berpasangan, deskriptif): "
          f"{sel((do - da).mean(), *ci(lambda ix: (do[ix] - da[ix]).mean()))}.\n")
    print("Deskriptif per arteri dan infark lama (logit, rerata perubahan; bagian naik):\n")
    print("| Lapis | n | probe-OMI | probe-AMI |")
    print("| --- | --- | --- | --- |")
    lapis = [(f"arteri {a}", seg.arteri.values == a) for a in ["LAD", "RCA", "sirkumfleks", "lainnya"]] + \
            [("tanpa infark lama", ~seg.infark_lama.values), ("dengan infark lama", seg.infark_lama.values)]
    for ln, m in lapis:
        if m.sum() == 0:
            continue
        print(f"| {ln} | {m.sum()} | {do[m].mean():.3f}; {(do[m] > 0).mean():.2f} | "
              f"{da[m].mean():.3f}; {(da[m] > 0).mean():.2f} |")
    print("\nLetak skor STAFF III terhadap Chongqing (skor model akhir pada EKG latihnya sendiri, persentil di "
          "kelompok tanpa AMI; median kelompok Chongqing sebagai rujukan):\n")
    print("| Model | median STAFF baseline | median STAFF akhir inflasi | median CQ tanpa AMI | "
          "median CQ AMI tanpa OMI | median CQ OMI | persentil baseline | persentil akhir inflasi |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for nama, (lg, cq) in skor.items():
        ref = cq[kel == 0]
        print(f"| {nama} | {np.median(lg[:, 0]):.3f} | {np.median(lg[:, 1]):.3f} | {np.median(ref):.3f} | "
              f"{np.median(cq[kel == 1]):.3f} | {np.median(cq[kel == 2]):.3f} | "
              f"{100 * np.mean(ref < np.median(lg[:, 0])):.1f} | {100 * np.mean(ref < np.median(lg[:, 1])):.1f} |")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--butir", default="")
    ap.add_argument("--unduh", action="store_true")
    ap.add_argument("--embed-staff3", action="store_true")
    arg = ap.parse_args()
    if arg.unduh:
        unduh()
        return
    if arg.embed_staff3:
        embed_staff3()
        return
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase D OMI — keluaran omi_fase_d.py (B = {arg.B}, butir {arg.butir})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    t0 = time.time()
    if "D1" in butir:
        d1(ut, P, arg.B)
    if "D2" in butir:
        d2(ut, P, arg.B)
    if "D3" in butir:
        d3(ut, arg.B)
    print(f"Waktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
