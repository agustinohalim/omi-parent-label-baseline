"""Fase E OMI (Prareg_OMI_E.md, terkunci 13 Nov 2026): kontrol STAFF III di dalam rekaman, oklusi kronis,
NSTEMI tanpa PCI per lapis, CNN berlabel AMI.

Masukan di luar repo: seperti omi_fase_d.py, ditambah oof_m3a_ami.npz (D2) dan raw250_train.npy (cache omi_m2.py).

Pakai:
  python omi_fase_e.py --unduh                         # potongan awal inflasi STAFF III (byte-range), Python sistem
  python-gpu omi_fase_e.py --embed-awal           # embedding ECGFounder potongan awal inflasi
  python-gpu omi_fase_e.py --cnn-ami              # E4: CNN M2 dengan sasaran AMI -> oof_m2_ami.npz
  python omi_fase_e.py --butir E1,E2,E3,E4 [--B 2000]  # analisis, Python sistem
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
from omi_m01 import AKAR, BENIH, pilih_C, pipa  # noqa: E402
from omi_konstruk import beda_auc, muat, sel  # noqa: E402
from omi_fase_d import (EMB_S3, FS, META_S3, NSAD, NSEG, OFFSET, RENCANA_S3, S3, UA, URL, auc_ci,  # noqa: E402
                        baca_seg, emb_utama, kelompok, panjang)

RENCANA_AWAL = S3 / "rencana_awal_staff3.csv"
EMB_AWAL = S3 / "emb_ecgfounder_staff3_awal.npy"
OOF_M2_AMI = AKAR / "oof_m2_ami.npz"


# ---------------------------------------------------------------- E1: data
def unduh():
    import wfdb
    seg = pd.read_csv(RENCANA_S3)
    awal, buang, total = [], [], 0
    for _, r in seg.iterrows():
        target = int(round(r.D0 * FS))
        sumber = "D0"
        ev = S3 / "meta" / f"{r.bi1}.event"
        if ev.exists():
            an = wfdb.rdann(str(S3 / "meta" / r.bi1), "event")
            inf = [s for s, n in zip(an.sample, an.aux_note) if "inflation" in str(n).lower()]
            if inf:
                d = min(inf, key=lambda s: abs(s - target))
                sumber = f"event (selisih dari D0 {abs(d - target) / FS:.1f} s)"
                target = int(d)
        a = target + FS
        if a + NSEG > panjang(r.bi1) or a + NSEG > r.awal_inf:
            buang.append((r.pasien, "potongan awal di luar batas atau menumpuk akhir inflasi"))
            continue
        f = S3 / "seg" / f"{r.bi1}_{a}.bin"
        if not (f.exists() and f.stat().st_size == NSEG * NSAD * 2):
            b0 = OFFSET + a * NSAD * 2
            req = urllib.request.Request(URL + f"{r.bi1}.dat", headers={
                "User-Agent": UA, "Range": f"bytes={b0}-{b0 + NSEG * NSAD * 2 - 1}"})
            with urllib.request.urlopen(req, timeout=60) as h:
                assert h.status == 206, (r.bi1, h.status)
                isi = h.read()
            assert len(isi) == NSEG * NSAD * 2, (r.bi1, len(isi))
            f.write_bytes(isi)
            total += len(isi)
        awal.append({"pasien": r.pasien, "awal_awal": a, "sumber_inflasi": sumber})
    pd.DataFrame(awal).to_csv(RENCANA_AWAL, index=False)
    print(f"Potongan awal inflasi: {len(awal)}; dibuang {len(buang)} {buang}. Diunduh sekarang: {total / 1e6:.1f} MB.")


def embed_awal():
    import torch
    from omi_m3_ecgfounder import BOBOT, KODE, praproses
    sys.path.insert(0, str(KODE))
    from net1d import Net1D
    seg = pd.read_csv(RENCANA_S3).merge(pd.read_csv(RENCANA_AWAL), on="pasien")
    X, ok = [], []
    for _, r in seg.iterrows():
        x, fx = baca_seg(r.bi1, r.awal_awal)
        ok.append(not fx)
        X.append(praproses(x).astype(np.float32))
    m = Net1D(in_channels=12, base_filters=64, ratio=1, filter_list=[64, 160, 160, 400, 400, 1024, 1024],
              m_blocks_list=[2, 2, 2, 3, 3, 4, 4], kernel_size=16, stride=2, groups_width=16, verbose=False,
              use_bn=False, use_do=False, n_classes=150, return_features=True)
    import numpy.core.multiarray as nca
    izin = ([(nca.scalar, "numpy.core.multiarray.scalar"), np.dtype]
            + [getattr(np.dtypes, n) for n in dir(np.dtypes) if n.endswith("DType")])
    with torch.serialization.safe_globals(izin):
        ck = torch.load(BOBOT, map_location="cpu", weights_only=True)
    hilang, _ = m.load_state_dict(ck["state_dict"], strict=False)
    assert not [k for k in hilang if not k.startswith("dense.")], "bobot tidak termuat"
    m.to(torch.device("cuda")).eval()
    with torch.no_grad():
        E = np.concatenate([m(torch.from_numpy(np.stack(X[k:k + 32])).cuda())[1].cpu().numpy()
                            for k in range(0, len(X), 32)])
    assert E.shape == (len(seg), 1024) and np.isfinite(E).all()
    np.save(EMB_AWAL, E)
    pd.DataFrame({"pasien": seg.pasien, "mutu_awal_ok": ok}).to_csv(S3 / "mutu_awal_staff3.csv", index=False)
    print(f"Embedding awal inflasi {E.shape}; mutu tidak ok {int(np.sum(~np.array(ok)))}.")


# ---------------------------------------------------------------- E4: CNN berlabel AMI (GPU environment)
def cnn_ami():
    from omi_m2 import EPOCH, muat_sinyal
    from omi_m2 import oof as oof_cnn
    t0 = time.time()
    tr = pd.read_csv(AKAR / "csv/CSV/train.csv", dtype={"Patient_id": str})
    X = muat_sinyal(tr)
    iu = np.flatnonzero((tr.Paced != 1).values)
    ut = tr.iloc[iu].reset_index(drop=True)
    Xu = np.asarray(X[iu])
    y, g = ut.AMI.values.astype(int), ut.Patient_id.values
    ps = [oof_cnn(Xu, y, g, b, EPOCH)[:, 1] for b in BENIH]
    np.savez(OOF_M2_AMI, ecg_row_record=ut.ecg_row_record.values, **{f"M2ami_{b}": p for b, p in zip(BENIH, ps)})
    print(f"CNN berlabel AMI: {len(y)} EKG, AMI {y.sum()}, {EPOCH} epoch, {(time.time() - t0) / 60:.1f} menit. "
          f"AUROC AMI per benih: " + ", ".join(f"{roc_auc_score(y, p):.3f}" for p in ps) + "; "
          f"OMI per benih: " + ", ".join(f"{roc_auc_score(ut.OMI, p):.3f}" for p in ps) + ".")


# ---------------------------------------------------------------- analisis
def e1(ut, B):
    print("## E1. STAFF III: awal inflasi, akhir inflasi, baseline\n")
    seg = pd.read_csv(META_S3)
    E3 = np.load(EMB_S3).reshape(-1, 2, 1024)
    aw = pd.read_csv(RENCANA_AWAL).merge(pd.read_csv(S3 / "mutu_awal_staff3.csv"), on="pasien")
    Ea = np.load(EMB_AWAL)
    assert len(Ea) == len(aw)
    print(f"Pasangan D3: {len(seg)} (mutu D3 tidak ok {int((~seg.mutu_ok).sum())}). Potongan awal: {len(aw)}, mutu "
          f"tidak ok {int((~aw.mutu_awal_ok).sum())}. Sumber penanda inflasi: "
          + "; ".join(f"{k}: {v}" for k, v in aw.sumber_inflasi.str.split(" ").str[0].value_counts().items())
          + f"; selisih terbesar dari D0 {aw.sumber_inflasi.str.extract(r'([0-9.]+) s')[0].astype(float).max()} s.\n")
    ia = {p: k for k, p in enumerate(aw.pasien)}
    pakai = [k for k, (p, ok) in enumerate(zip(seg.pasien, seg.mutu_ok))
             if ok and p in ia and aw.mutu_awal_ok.iloc[ia[p]]]
    jA = [ia[seg.pasien.iloc[k]] for k in pakai]
    n = len(pakai)
    print(f"Pasien dengan ketiga potongan bermutu: {n}.\n")
    E, g = emb_utama(ut), ut.Patient_id.values
    kel = kelompok(ut)
    sk = {}
    for nama, kol in [("probe-OMI", "OMI"), ("probe-AMI", "AMI")]:
        y = ut[kol].values.astype(int)
        C = pilih_C(E, y, g, BENIH[0])
        mdl = pipa(C).fit(E, y)
        sd = float(np.std(mdl.decision_function(E)[kel == 0]))
        L = np.stack([mdl.decision_function(E3[pakai, 0]), mdl.decision_function(Ea[jA]),
                      mdl.decision_function(E3[pakai, 1])], 1)  # baseline, awal, akhir
        sk[nama] = (L, sd, C)
        print(f"{nama}: C {C}; simpangan baku logit di Chongqing tanpa AMI {sd:.3f}.")
    print()
    rng = np.random.default_rng(20261126)
    boot = [rng.integers(0, n, n) for _ in range(B)]

    def ci(v):
        b = np.array([v[ix].mean() for ix in boot])
        return np.quantile(b, .025), np.quantile(b, .975)

    beda = {"(i) akhir − awal inflasi (rekaman sama)": (2, 1), "(ii) awal inflasi − baseline": (1, 0),
            "(iii) akhir inflasi − baseline": (2, 0)}
    print("| Model | Perbandingan | median dari → ke | rerata perubahan logit | bagian naik | "
          "rerata terstandar |")
    print("| --- | --- | --- | --- | --- | --- |")
    for nama, (L, sd, _) in sk.items():
        for bn, (a, b) in beda.items():
            d = L[:, a] - L[:, b]
            print(f"| {nama} | {bn} | {np.median(L[:, b]):.3f} → {np.median(L[:, a]):.3f} | "
                  f"{sel(d.mean(), *ci(d))} | {sel((d > 0).mean(), *ci((d > 0).astype(float)))} | "
                  f"{sel(d.mean() / sd, *(np.array(ci(d)) / sd))} |")
    print("\nSelisih terstandar probe-OMI − probe-AMI (berpasangan):\n")
    for bn, (a, b) in beda.items():
        Lo, so, _ = sk["probe-OMI"]
        La, sa, _ = sk["probe-AMI"]
        dd = (Lo[:, a] - Lo[:, b]) / so - (La[:, a] - La[:, b]) / sa
        print(f"- {bn}: {sel(dd.mean(), *ci(dd))}")
    print()


def e2(ut, P, B):
    print("## E2. Subkelompok di dalam tanpa AMI (skor kohort penuh)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    oa = np.load(AKAR / "oof_m3a_ami.npz")
    pr = {"probe-OMI": P["M3a"], "probe-AMI": [oa[f"ami_{b}"] for b in BENIH]}
    rng = np.random.default_rng(20261127)
    s = np.flatnonzero(kel == 0)
    print("| Subkelompok lawan sisa tanpa AMI | n subkelompok / n sisa | probe-OMI | probe-AMI |")
    print("| --- | --- | --- | --- |")
    for kol in ["CTO", "Prior_PCI", "UA", "VF_VT"]:
        y = (ut[kol].values[s] == 1).astype(int)
        r = auc_ci(y, g[s], {k: [p[s] for p in ps] for k, ps in pr.items()}, rng, B)
        print(f"| {kol} | {y.sum()} / {len(y) - y.sum()} | {sel(*r['probe-OMI'])} | {sel(*r['probe-AMI'])} |",
              flush=True)
    print()


def e3(ut, P, B):
    print("## E3. NSTEMI tanpa PCI dan OMI di dalam NSTEMI, per kuartil dan jenis kelamin\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    ns, pci = (ut.NSTEMI == 1).values, (ut.PCI == 1).values
    dua = {k: P[k] for k in ("M2", "M3a")}
    rng = np.random.default_rng(20261128)
    q = pd.qcut(ut.Time_Interval, 4, labels=["Q1", "Q2", "Q3", "Q4"]).astype(str).values
    lapis = [("semua", np.ones(len(ut), bool))] + [(f"kuartil {k}", q == k) for k in ["Q1", "Q2", "Q3", "Q4"]] + \
            [("laki-laki", (ut.gender == 1).values), ("perempuan", (ut.gender == 0).values)]
    pasangan = {"(b5) NSTEMI tanpa OMI dan tanpa PCI lawan tanpa AMI": ((kel == 1) & ns & ~pci, kel == 0),
                "OMI lawan AMI tanpa OMI, di dalam NSTEMI": ((kel == 2) & ns, (kel == 1) & ns)}
    print("| Lapis | Pasangan | n pos / n neg | M2 | M3a |")
    print("| --- | --- | --- | --- | --- |")
    for ln, lm in lapis:
        for pn, (pos, neg) in pasangan.items():
            s = np.flatnonzero(lm & (pos | neg))
            y = pos[s].astype(int)
            r = auc_ci(y, g[s], {k: [p[s] for p in ps] for k, ps in dua.items()}, rng, B)
            print(f"| {ln} | {pn} | {y.sum()} / {len(y) - y.sum()} | {sel(*r['M2'])} | {sel(*r['M3a'])} |",
                  flush=True)
    print()


def e4(ut, P, B):
    print("## E4. CNN berlabel AMI lawan CNN berlabel OMI\n")
    o = np.load(OOF_M2_AMI, allow_pickle=True)
    assert (o["ecg_row_record"] == ut.ecg_row_record.values).all()
    pa = [o[f"M2ami_{b}"] for b in BENIH]
    kel, g = kelompok(ut), ut.Patient_id.values
    rng = np.random.default_rng(20261129)
    pr = {"CNN-OMI (M2)": P["M2"], "CNN-AMI": pa}
    sas = {"OMI lawan semua": (np.ones(len(ut), bool), "OMI"), "(c) OMI lawan AMI tanpa OMI": (kel >= 1, "OMI"),
           "AMI lawan tanpa AMI": (np.ones(len(ut), bool), "AMI")}
    print("| Sasaran | n pos / n | CNN-OMI | CNN-AMI | selisih CNN-OMI − CNN-AMI |")
    print("| --- | --- | --- | --- | --- |")
    for nama, (m, kol) in sas.items():
        s = np.flatnonzero(m)
        y = ut[kol].values[s].astype(int)
        r = auc_ci(y, g[s], {k: [p[s] for p in ps] for k, ps in pr.items()}, rng, B)
        t, lo, hi, nn_ = beda_auc(y, g[s], [p[s] for p in P["M2"]], [p[s] for p in pa], rng, B)
        print(f"| {nama} | {y.sum()} / {len(y)} | {sel(*r['CNN-OMI (M2)'])} | {sel(*r['CNN-AMI'])} | "
              f"{sel(t, lo, hi)} |", flush=True)
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--butir", default="")
    ap.add_argument("--unduh", action="store_true")
    ap.add_argument("--embed-awal", action="store_true")
    ap.add_argument("--cnn-ami", action="store_true")
    arg = ap.parse_args()
    if arg.unduh:
        return unduh()
    if arg.embed_awal:
        return embed_awal()
    if arg.cnn_ami:
        return cnn_ami()
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase E OMI — keluaran omi_fase_e.py (B = {arg.B}, butir {arg.butir})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    t0 = time.time()
    for k, f in [("E1", lambda: e1(ut, arg.B)), ("E2", lambda: e2(ut, P, arg.B)), ("E3", lambda: e3(ut, P, arg.B)),
                 ("E4", lambda: e4(ut, P, arg.B))]:
        if k in butir:
            f()
    print(f"Waktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
