"""Fase H OMI (Prareg_OMI_H.md, terkunci 13 Nov 2026): pembanding berlabel STEMI dan label kontrol-negatif.

Masukan di luar repo ($OMI_DATA): seperti omi_fase_g.py. Keluaran latih: oof_m3a_stemi.npz, kontrol_h2.npz.

Pakai:
  python omi_fase_h.py --latih          # H1 probe-STEMI (tiga lipatan, C dari CV dalam) dan H2 probe kontrol
  python omi_fase_h.py --butir H1,H2,H3,H4 [--B 2000]   # H3: penyimpangan P1; H4: P2; H5-H6: P3; H7: P4; H8: P5
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).parent))
from omi_m01 import AKAR, BENIH, oof  # noqa: E402
from omi_konstruk import beda_auc, muat, sel  # noqa: E402
from omi_fase_d import auc_ci, emb_utama, kelompok  # noqa: E402
from omi_fase_f import probe_oof  # noqa: E402

F_STEMI = AKAR / "oof_m3a_stemi.npz"
F_KONTROL = AKAR / "kontrol_h2.npz"
F1_ASLI = 0.6431
G1_P95 = 0.6092


def label_kontrol(ut):
    kel = kelompok(ut)
    ami = kel >= 1
    usia, ti = ut.age.values, ut.Time_Interval.values
    syarat = {"PCI": ut.PCI.values == 1, "VF/VT": ut.VF_VT.values == 1,
              "usia >= median AMI": usia >= np.median(usia[ami]),
              "laki-laki": ut.gender.values == 1,
              "dekat angiografi (<= median AMI)": ti <= np.median(ti[ami]),
              "STEMI": ut.STEMI.values == 1}
    return {k: (ami & v).astype(int) for k, v in syarat.items()}


def latih():
    ut, _ = muat()
    E, g = emb_utama(ut), ut.Patient_id.values
    t0 = time.time()
    ys = ut.STEMI.values.astype(int)
    hasil = [oof(E, ys, g, b, True) for b in BENIH]
    np.savez(F_STEMI, **{f"stemi_{b}": h[0][:, 1] for b, h in zip(BENIH, hasil)})
    print(f"H1 probe-STEMI: {(time.time() - t0) / 60:.1f} menit, C terpilih {sorted({c for h in hasil for c in h[1]})}",
          flush=True)
    simpan = {"OMI_asli": probe_oof(E, ut.OMI.values.astype(int), g)}
    for k, y in label_kontrol(ut).items():
        simpan[k] = probe_oof(E, y, g)
        print(f"H2 {k}: positif {y.sum()} ({(time.time() - t0) / 60:.1f} menit)", flush=True)
    np.savez(F_KONTROL, **simpan)


def h1(ut, P, B):
    print("## H1. Label oklusi lawan label STEMI (probe)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    o = np.load(F_STEMI)
    ps = [o[f"stemi_{b}"] for b in BENIH]
    rng = np.random.default_rng(20261160)
    ns = (ut.NSTEMI == 1).values
    st = (ut.STEMI == 1).values
    sas = {"OMI lawan semua": np.ones(len(ut), bool), "(c) OMI lawan AMI tanpa OMI": kel >= 1,
           "di dalam NSTEMI": (kel >= 1) & ns, "di dalam STEMI (deskriptif)": (kel >= 1) & st}
    print("| Sasaran | n OMI / n | probe-OMI | probe-STEMI | selisih OMI − STEMI |")
    print("| --- | --- | --- | --- | --- |")
    hasil = {}
    for nama, m in sas.items():
        s = np.flatnonzero(m)
        y = ut.OMI.values[s].astype(int)
        ao = np.mean([roc_auc_score(y, p[s]) for p in P["M3a"]])
        a2 = np.mean([roc_auc_score(y, p[s]) for p in ps])
        d = beda_auc(y, g[s], [p[s] for p in P["M3a"]], [p[s] for p in ps], rng, B)
        hasil[nama] = d
        print(f"| {nama} | {y.sum()} / {len(y)} | {ao:.3f} | {a2:.3f} | {sel(*d[:3])} |", flush=True)
    a = np.mean([roc_auc_score(ut.STEMI.values, p) for p in ps])
    print(f"\nAUROC probe-STEMI untuk sasaran latihnya sendiri (STEMI lawan semua): {a:.3f}.")
    d = hasil["(c) OMI lawan AMI tanpa OMI"]
    print(f"Aturan: batas bawah selisih (c) > 0: **{'ya' if d[1] > 0 else 'tidak'}**.\n")


def h2(ut, P, B):
    print("## H2. Label kontrol-negatif di dalam infark (probe, C = 0,001, lipatan 20261107)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    o = np.load(F_KONTROL)
    s = np.flatnonzero(kel >= 1)
    y = ut.OMI.values[s].astype(int)
    pa = o["OMI_asli"]
    asli = roc_auc_score(y, pa[s])
    print(f"Probe berlabel OMI asli pada lipatan ini: AUROC (c) {asli:.4f} (F1: {F1_ASLI}).\n")
    rng = np.random.default_rng(20261161)
    lab = label_kontrol(ut)
    print("| Label kontrol (AMI dan …) | n positif | AUROC (c) untuk OMI | > p95 nol berlapis (0,609) | selisih asli − kontrol |")
    print("| --- | --- | --- | --- | --- |")
    semua = True
    for k in lab:
        pk = o[k]
        ak = roc_auc_score(y, pk[s])
        d = beda_auc(y, g[s], [pa[s]], [pk[s]], rng, B)
        semua &= d[1] > 0
        print(f"| {k} | {lab[k].sum()} | {ak:.3f} | {'ya' if ak > G1_P95 else 'tidak'} | {sel(*d[:3])} |", flush=True)
    print(f"\nAturan: batas bawah selisih asli − kontrol > 0 untuk setiap kontrol: **{'ya' if semua else 'tidak'}**.\n")


def h3(ut, B):
    """Penyimpangan P1: kendali jarak EKG ke angiografi."""
    print("## H3. Jarak EKG ke angiografi (penyimpangan P1)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    s = np.flatnonzero(kel >= 1)
    y = ut.OMI.values[s].astype(int)
    ti = ut.Time_Interval.values.astype(float)
    d = auc_ci(y, g[s], {"jarak": [-ti[s]]}, np.random.default_rng(20261162), B)["jarak"]
    print(f"(i) AUROC jarak saja (skor = −Time_Interval) untuk (c): {sel(*d)}.\n")
    E = emb_utama(ut)
    Ej = np.column_stack([E, np.log1p(ti)])
    yo, ya = ut.OMI.values.astype(int), (kel >= 1).astype(int)
    t0 = time.time()
    p = {"OMI, tanpa jarak": probe_oof(E, yo, g), "AMI, tanpa jarak": probe_oof(E, ya, g),
         "OMI, dengan jarak": probe_oof(Ej, yo, g), "AMI, dengan jarak": probe_oof(Ej, ya, g)}
    print(f"Latih empat *probe*: {(time.time() - t0) / 60:.1f} menit.\n")
    print("| *Probe* | AUROC (c) |")
    print("| --- | --- |")
    for k, v in p.items():
        print(f"| {k} | {roc_auc_score(y, v[s]):.3f} |")
    rng = np.random.default_rng(20261163)
    hasil = {}
    for versi in ["tanpa jarak", "dengan jarak"]:
        hasil[versi] = beda_auc(y, g[s], [p[f"OMI, {versi}"][s]], [p[f"AMI, {versi}"][s]], rng, B)
        print(f"\n(ii) Selisih label oklusi − label infark, (c), {versi}: {sel(*hasil[versi][:3])}.")
    print(f"\nAturan: batas bawah selisih dengan jarak > 0: **{'ya' if hasil['dengan jarak'][1] > 0 else 'tidak'}**.\n")


def auc_lapis(y, p, q):
    """AUROC hanya atas pasangan positif/negatif di lapis yang sama: rerata AUROC per lapis berbobot n1*n0."""
    num = den = 0.0
    for k in np.unique(q):
        m = q == k
        n1, n0 = int(y[m].sum()), int((1 - y[m]).sum())
        if n1 and n0:
            num += roc_auc_score(y[m], p[m]) * n1 * n0
            den += n1 * n0
    return num / den


def h4(ut, P, B):
    """Penyimpangan P2: persentil probe-AMI di nol, Q4 - Q1, AUROC berlapis kuartil, perubahan dengan jarak."""
    import pandas as pd
    from omi_fase_f import muat_ami
    from omi_m01 import indeks_bootstrap
    print("## H4. Penyimpangan P2\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    s = np.flatnonzero(kel >= 1)
    y, gs = ut.OMI.values[s].astype(int), g[s]
    E = emb_utama(ut)
    pa1 = probe_oof(E, (kel >= 1).astype(int), g)
    a1 = roc_auc_score(y, pa1[s])
    pf = pd.read_csv(AKAR / "perm_f1.csv")
    nf = pf.loc[pf.perm > 0, "auc_c"].values
    ng = pd.read_csv(AKAR / "perm_g1.csv").auc_c.values
    print(f"(i) *Probe* berlabel AMI, lipatan 20261107, C 0,001: AUROC (c) {a1:.4f}. Nol tanpa lapis: "
          f"{(nf < a1).mean() * 100:.0f} % di bawahnya (p95 {np.quantile(nf, .95):.4f}); nol berlapis: "
          f"{(ng < a1).mean() * 100:.0f} % di bawahnya (p95 {np.quantile(ng, .95):.4f}). "
          f"Aturan ≤ p95 berlapis: **{'ya' if a1 <= np.quantile(ng, .95) else 'tidak'}**.\n")
    pa, ca = muat_ami(ut)
    q = pd.qcut(ut.Time_Interval, 4, labels=["Q1", "Q2", "Q3", "Q4"]).astype(str).values[s]
    pas = {"probe": ([p[s] for p in P["M3a"]], [p[s] for p in pa]), "CNN": ([p[s] for p in P["M2"]], [p[s] for p in ca])}

    def gain_q(ix, k, po, pi):
        m = q[ix] == k
        return (np.mean([roc_auc_score(y[ix][m], p[ix][m]) for p in po])
                - np.mean([roc_auc_score(y[ix][m], p[ix][m]) for p in pi]))

    def stat(ix, po, pi):
        d41 = gain_q(ix, "Q4", po, pi) - gain_q(ix, "Q1", po, pi)
        dl = (np.mean([auc_lapis(y[ix], p[ix], q[ix]) for p in po])
              - np.mean([auc_lapis(y[ix], p[ix], q[ix]) for p in pi]))
        return d41, dl

    semua = np.arange(len(s))
    hasil = {}
    for nama, (po, pi) in pas.items():
        rng = np.random.default_rng(20261164 if nama == "probe" else 20261165)
        t = stat(semua, po, pi)
        v = np.array([stat(ix, po, pi) for ix in indeks_bootstrap(gs, rng, B)])
        lo, hi = np.quantile(v, .025, axis=0), np.quantile(v, .975, axis=0)
        hasil[nama] = (t, lo, hi)
        print(f"{nama}: (ii) Q4 − Q1 {sel(t[0], lo[0], hi[0])}; (iii) selisih AUROC berlapis kuartil "
              f"{sel(t[1], lo[1], hi[1])}.", flush=True)
    t, lo, hi = hasil["probe"]
    print(f"\nAturan (ii) CI Q4 − Q1 *probe* di dalam ±0,03: **{'ya' if lo[0] >= -0.03 and hi[0] <= 0.03 else 'tidak'}**. "
          f"Aturan (iii) batas bawah *probe* > 0: **{'ya' if lo[1] > 0 else 'tidak'}**.\n")
    ti = ut.Time_Interval.values.astype(float)
    Ej = np.column_stack([E, np.log1p(ti)])
    yo, ya = ut.OMI.values.astype(int), (kel >= 1).astype(int)
    p4 = [pa1, probe_oof(E, yo, g), probe_oof(Ej, yo, g), probe_oof(Ej, ya, g)]
    pk = [p[s] for p in p4]

    def dd(ix):
        return ((roc_auc_score(y[ix], pk[2][ix]) - roc_auc_score(y[ix], pk[3][ix]))
                - (roc_auc_score(y[ix], pk[1][ix]) - roc_auc_score(y[ix], pk[0][ix])))
    rng = np.random.default_rng(20261166)
    v = [dd(ix) for ix in indeks_bootstrap(gs, rng, B)]
    lo, hi = np.quantile(v, [.025, .975])
    print(f"(iv) (keunggulan dengan jarak) − (keunggulan tanpa jarak): {sel(dd(semua), lo, hi)}. "
          f"Aturan CI di dalam ±0,03: **{'ya' if lo >= -0.03 and hi <= 0.03 else 'tidak'}**.\n")


def h5(ut, B):
    """Penyimpangan P3: pasangan bersarang kedua, STEMI lawan NSTEMI di dalam AMI."""
    from omi_fase_f import muat_ami
    print("## H5. Pasangan bersarang kedua: STEMI di dalam infark (penyimpangan P3)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    s = np.flatnonzero((kel >= 1) & ((ut.STEMI == 1) | (ut.NSTEMI == 1)).values)
    y = ut.STEMI.values[s].astype(int)
    o = np.load(F_STEMI)
    ps = [o[f"stemi_{b}"][s] for b in BENIH]
    pa = [p[s] for p in muat_ami(ut)[0]]
    a_s = np.mean([roc_auc_score(y, p) for p in ps])
    a_a = np.mean([roc_auc_score(y, p) for p in pa])
    d = beda_auc(y, g[s], ps, pa, np.random.default_rng(20261167), B)
    print(f"STEMI lawan NSTEMI di dalam AMI ({y.sum()} / {len(y)}): *probe* berlabel STEMI {a_s:.3f}, berlabel AMI "
          f"{a_a:.3f}; selisih {sel(*d[:3])}.\n")


def h6(ut):
    """Penyimpangan P3: titik-balik tinjauan label dengan pertukaran berpola skor EKG."""
    print("## H6. Titik-balik tinjauan label (penyimpangan P3)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    E = emb_utama(ut)
    pa = probe_oof(E, (kel >= 1).astype(int), g)
    s = np.flatnonzero(kel >= 1)
    tipe = np.where(ut.STEMI.values == 1, 0, np.where(ut.NSTEMI.values == 1, 1, 2))
    rng = np.random.default_rng(20261168)
    acak = np.zeros(len(ut), int)
    for t in range(3):
        m = np.flatnonzero((kel >= 1) & (tipe == t))
        n_pos = int(((kel == 2) & (tipe == t)).sum())
        acak[rng.choice(m, n_pos, replace=False)] = 1
    print("| k pasangan ditukar | % EKG infark berubah label | AUROC (c) *probe* label tertukar | AUROC (c) *probe*-AMI | keunggulan |")
    print("| --- | --- | --- | --- | --- |")
    for k in [0, 25, 50, 100, 200, 400]:
        lab = acak.copy()
        for t in range(3):
            m = np.flatnonzero((kel >= 1) & (tipe == t))
            kt = int(round(k * len(m) / len(s)))
            neg = m[lab[m] == 0]
            pos = m[lab[m] == 1]
            naik = neg[np.argsort(-pa[neg])[:kt]]
            turun = pos[np.argsort(pa[pos])[:kt]]
            lab[naik], lab[turun] = 1, 0
        p = probe_oof(E, lab, g)
        a1, a0 = roc_auc_score(lab[s], p[s]), roc_auc_score(lab[s], pa[s])
        ubah = int((lab[s] != acak[s]).sum())
        print(f"| {k} | {100 * ubah / len(s):.1f} | {a1:.3f} | {a0:.3f} | {a1 - a0:+.3f} |", flush=True)
    print()


def h7(ut, B):
    """Penyimpangan P4: interval rujukan induk dan sebaran keunggulan nol pada labelnya sendiri."""
    import pandas as pd
    from omi_fase_f import muat_ami
    from omi_fase_g import PERM_G, lapis_tipe
    print("## H7. Interval rujukan dan sebaran keunggulan nol (penyimpangan P4)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    ami = kel >= 1
    pa, ca = muat_ami(ut)
    o = np.load(F_STEMI)
    ps = [o[f"stemi_{b}"] for b in BENIH]
    st, ns = (ut.STEMI == 1).values, (ut.NSTEMI == 1).values
    yo = ut.OMI.values.astype(int)
    rng = np.random.default_rng(20261169)
    print("### H7(i) Rujukan induk dengan interval (bootstrap bergugus pasien, benih 20261169)\n")
    print("| Rujukan | Sasaran | n pos / n | AUROC [95 % CI] |")
    print("| --- | --- | --- | --- |")
    baris = [("*probe* berlabel AMI", "(c) OMI lawan AMI tanpa OMI", ami, yo, pa),
             ("CNN berlabel AMI", "(c) OMI lawan AMI tanpa OMI", ami, yo, ca),
             ("*probe* berlabel AMI", "di dalam STEMI", ami & st, yo, pa),
             ("CNN berlabel AMI", "di dalam STEMI", ami & st, yo, ca),
             ("*probe* berlabel AMI", "di dalam NSTEMI", ami & ns, yo, pa),
             ("CNN berlabel AMI", "di dalam NSTEMI", ami & ns, yo, ca),
             ("*probe* berlabel STEMI", "(c) OMI lawan AMI tanpa OMI", ami, yo, ps),
             ("*probe* berlabel AMI", "STEMI lawan NSTEMI di dalam AMI (pasangan kedua)", ami & (st | ns),
              ut.STEMI.values.astype(int), pa)]
    for nama, sas, m, y0, pr in baris:
        s = np.flatnonzero(m)
        y = y0[s]
        t, lo, hi = auc_ci(y, g[s], {"r": [p[s] for p in pr]}, rng, B)["r"]
        print(f"| {nama} | {sas} | {y.sum()} / {len(y)} | {sel(t, lo, hi)} |", flush=True)
    print()
    print("### H7(ii) Keunggulan nol pada label acak sendiri (lipatan 20261107, C 0,001)\n")
    E = emb_utama(ut)
    s = np.flatnonzero(ami)
    pa1 = probe_oof(E, ami.astype(int), g)
    po1 = probe_oof(E, yo, g)
    k_asli = roc_auc_score(yo[s], po1[s]) - roc_auc_score(yo[s], pa1[s])
    print(f"Label oklusi pada lipatan dan C yang sama: AUROC (c) {roc_auc_score(yo[s], po1[s]):.4f} − "
          f"{roc_auc_score(yo[s], pa1[s]):.4f} = keunggulan {k_asli:.4f}.\n")
    g1 = pd.read_csv(PERM_G).set_index("perm")
    f = AKAR / "perm_h7.csv"
    sudah = pd.read_csv(f) if f.exists() else pd.DataFrame(columns=["perm"])
    rek = sudah.to_dict("records")
    lp = lapis_tipe(ut)
    t0 = time.time()
    for k in range(1001, 1101):
        if k in set(sudah.perm):
            continue
        r = np.random.default_rng(k)
        yp = np.zeros_like(yo)
        for nama in ["STEMI", "NSTEMI", "lain"]:
            ix = np.flatnonzero(ami & (lp == nama))
            m = int(yo[ix].sum())
            if m:
                yp[r.choice(ix, m, replace=False)] = 1
        p = probe_oof(E, yp, g)
        cek = roc_auc_score(yo[s], p[s])
        if abs(cek - g1.loc[k, "auc_c"]) > 1e-9:
            print(f"BERHENTI: label {k} tidak sama dengan perm_g1.csv ({cek:.6f} lawan {g1.loc[k, 'auc_c']:.6f}).")
            return
        a1, a0 = roc_auc_score(yp[s], p[s]), roc_auc_score(yp[s], pa1[s])
        rek.append({"perm": k, "auc_sendiri": a1, "auc_ami_sendiri": a0, "keunggulan": a1 - a0})
        pd.DataFrame(rek).to_csv(f, index=False)
        print(f"label {k}: keunggulan {a1 - a0:+.4f} ({(time.time() - t0) / 60:.1f} menit)", flush=True)
    d = pd.read_csv(f)
    v = d.keunggulan.values
    q = np.quantile(v, [.025, .5, .95, .975])
    print(f"\nNol: {len(v)} label. Keunggulan rerata {v.mean():.4f}, SB {v.std(ddof=1):.4f}, persentil 2,5/50/95/97,5 "
          f"{q[0]:.4f} / {q[1]:.4f} / {q[2]:.4f} / {q[3]:.4f}, maksimum {v.max():.4f}. AUROC *probe* berlabel-acak "
          f"terhadap labelnya sendiri: rerata {d.auc_sendiri.mean():.4f}; *probe* berlabel AMI terhadap label acak: "
          f"rerata {d.auc_ami_sendiri.mean():.4f}.")
    print(f"Keunggulan label oklusi {k_asli:.4f}: persentil ke-{100 * (v < k_asli).mean():.0f} ({int((v >= k_asli).sum())} "
          f"dari {len(v)} ≥). Aturan > p95: **{'ya' if k_asli > q[2] else 'tidak'}**.\n")


def h8(ut, P, B):
    """Penyimpangan P5: skala label kontrol pada labelnya sendiri, titik operasi, jarak tanpa penalti."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import SplineTransformer
    from omi_fase_f import muat_ami
    from omi_m01 import indeks_bootstrap, lipatan
    print("## H8. Skala label klinis, titik operasi, jarak tanpa penalti (penyimpangan P5)\n")
    kel, g = kelompok(ut), ut.Patient_id.values
    ami = kel >= 1
    s = np.flatnonzero(ami)
    E = emb_utama(ut)
    pa1 = probe_oof(E, ami.astype(int), g)
    o = np.load(F_KONTROL)
    yo = ut.OMI.values.astype(int)
    # (i)
    print("### H8(i) Label bersarang klinis, masing-masing dinilai terhadap labelnya sendiri (lipatan 20261107, C 0,001)\n")
    print("| Label (AMI dan …) | positif / EKG AMI | AUROC *probe* berlabel itu | AUROC *probe*-AMI | keunggulan [95 % CI] |")
    print("| --- | --- | --- | --- | --- |")
    rng = np.random.default_rng(20261170)
    lab = dict(label_kontrol(ut))
    lab["OMI (label oklusi)"] = yo
    pred = {k: o[k] for k in label_kontrol(ut)}
    pred["OMI (label oklusi)"] = o["OMI_asli"]
    hasil = {}
    for k, y0 in lab.items():
        y = y0[s]
        a1, a0 = roc_auc_score(y, pred[k][s]), roc_auc_score(y, pa1[s])
        d = beda_auc(y, g[s], [pred[k][s]], [pa1[s]], rng, B)
        hasil[k] = d[0]
        print(f"| {k} | {y.sum()} / {len(y)} | {a1:.3f} | {a0:.3f} | {sel(*d[:3])} |", flush=True)
    urut = sorted(hasil, key=hasil.get, reverse=True)
    print(f"\nUrutan keunggulan: {', '.join(f'{k} {hasil[k]:.3f}' for k in urut)}. Label oklusi di urutan "
          f"{urut.index('OMI (label oklusi)') + 1} dari {len(urut)}; label kontrol dengan keunggulan lebih besar: "
          f"{sum(hasil[k] > hasil['OMI (label oklusi)'] for k in hasil)}.\n")
    # (ii)
    print("### H8(ii) Sensitivitas pada spesifisitas tetap, (c) OMI lawan infark tanpa oklusi (tiga penetapan lipatan)\n")
    y = yo[s]
    po3 = [p[s] for p in P["M3a"]]
    pa3 = [p[s] for p in muat_ami(ut)[0]]

    def sens(yy, p, sp):
        thr = np.quantile(p[yy == 0], sp)
        return (p[yy == 1] > thr).mean()

    def dsens(idx, sp):
        yy = y[idx]
        return (np.mean([sens(yy, p[idx], sp) for p in po3]), np.mean([sens(yy, p[idx], sp) for p in pa3]))

    semua = np.arange(len(y))
    ix = list(indeks_bootstrap(g[s], np.random.default_rng(20261171), B))
    frac = y.mean()
    print("| Spesifisitas | Se *probe*-OMI | Se *probe*-AMI | selisih [95 % CI] | tambahan OMI per 1.000 EKG infark [95 % CI] |")
    print("| --- | --- | --- | --- | --- |")
    for sp in [0.80, 0.90]:
        so, sa = dsens(semua, sp)
        v = np.array([np.subtract(*dsens(i, sp)) for i in ix])
        lo, hi = np.quantile(v, [.025, .975])
        print(f"| {sp:.0%} | {so:.3f} | {sa:.3f} | {sel(so - sa, lo, hi)} | "
              f"{1000 * frac * (so - sa):.0f} [{1000 * frac * lo:.0f}, {1000 * frac * hi:.0f}] |", flush=True)
    print(f"\nPrevalensi OMI di antara EKG infark: {y.sum()} / {len(y)} = {frac:.3f}.\n")
    # (iii)
    print("### H8(iii) Jarak tanpa penalti: regresi tahap kedua di dalam AMI\n")
    ti = np.log1p(ut.Time_Interval.values.astype(float))[s]

    def lg(p):
        p = np.clip(p, 1e-9, 1 - 1e-9)
        return np.log(p / (1 - p))

    def tahap2(skor):
        q = np.zeros(len(y))
        for a, b in lipatan(y, g[s], 20261107):
            st = SplineTransformer(n_knots=5, degree=3).fit(ti[a, None])
            xa = np.column_stack([lg(skor[a]), st.transform(ti[a, None])])
            xb = np.column_stack([lg(skor[b]), st.transform(ti[b, None])])
            q[b] = LogisticRegression(penalty=None, max_iter=5000).fit(xa, y[a]).predict_proba(xb)[:, 1]
        return q

    qo, qa = tahap2(o["OMI_asli"][s]), tahap2(pa1[s])
    print(f"AUROC (c) tahap kedua: label oklusi + spline jarak {roc_auc_score(y, qo):.3f}; label infark + spline jarak "
          f"{roc_auc_score(y, qa):.3f}.")
    d = beda_auc(y, g[s], [qo], [qa], np.random.default_rng(20261172), B)
    print(f"Selisih label oklusi − label infark, dengan jarak tanpa penalti: {sel(*d[:3])}. "
          f"Aturan batas bawah > 0: **{'ya' if d[1] > 0 else 'tidak'}**.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--butir", default="")
    ap.add_argument("--latih", action="store_true")
    arg = ap.parse_args()
    if arg.latih:
        return latih()
    butir = arg.butir.split(",")
    ut, P = muat()
    print(f"# Fase H OMI — keluaran omi_fase_h.py (B = {arg.B}, butir {arg.butir})\n")
    print(f"Analisis utama: {len(ut)} EKG, OMI {int(ut.OMI.sum())}, AMI {int(ut.AMI.sum())}.\n")
    t0 = time.time()
    for k, fn in [("H1", lambda: h1(ut, P, arg.B)), ("H2", lambda: h2(ut, P, arg.B)),
                  ("H3", lambda: h3(ut, arg.B)),
                  ("H4", lambda: h4(ut, P, arg.B)),
                  ("H5", lambda: h5(ut, arg.B)), ("H6", lambda: h6(ut)),
                  ("H7", lambda: h7(ut, arg.B)),
                  ("H8", lambda: h8(ut, P, arg.B))]:
        if k in butir:
            fn()
    print(f"Waktu jalan: {(time.time() - t0) / 60:.1f} menit.")


if __name__ == "__main__":
    main()
