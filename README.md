# omi-parent-label-baseline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24223296.svg)](https://doi.org/10.5281/zenodo.24223296)

Analysis code, aggregate logs, analysis plans and fold assignments for the manuscript *A parent-label baseline for
ECG models trained on nested labels: what a reviewed occlusion label adds within infarction* (in preparation).

The study trains the same models twice on an open 12-lead ECG dataset, once on the dataset's reviewed acute
coronary occlusion label (TIMI 0–1, "OMI") and once on the broader acute myocardial infarction label, and scores
both within infarction. The infarction-trained model's AUROC there is the parent-label baseline; the difference is
the paired gain of the narrow label. Models: a logistic-regression probe on the frozen ECGFounder embedding, a 1-D
CNN trained from scratch, and age–sex and ST-amplitude baselines. An external test uses STAFF III recordings made
during elective balloon occlusion.

**No ECG data, embeddings, predictions or model weights are included.** All inputs are openly available:

- Chongqing 12-lead ECG dataset for acute coronary syndrome prediction (Du et al., *Scientific Data* 13:1009,
  2026), CC0, https://doi.org/10.6084/m9.figshare.29925314. Set `OMI_DATA` to the folder that holds `csv/CSV/`,
  `row_data/` and `med/` (default `data/chongqing`). Derived arrays and out-of-fold predictions are written there.
- STAFF III database 1.0.0 on PhysioNet, Open Data Commons Attribution licence,
  https://physionet.org/content/staffiii/1.0.0/. `omi_fase_d.py --unduh` fetches only the 10-s segments used
  (byte ranges). Set `STAFF3_DATA` (default `data/staffiii`).
- ECGFounder (Li et al., 2025), MIT: the `Net1D` code from https://github.com/NickLJLee/ECGFounder (commit
  67367071) in `ECGFOUNDER_CODE` (default `ext/ECGFounder`) and the 12-lead weights `12_lead_ECGFounder.pth` from
  PKUDigitalHealth/ECGFounder in `ECGFOUNDER_WEIGHTS` (default `ext/12_lead_ECGFounder.pth`).

## Requirements

Python 3.12.10 with NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, SciPy 1.18.1, matplotlib 3.11.1 and wfdb 4.3.1.
The CNN and the ECGFounder embeddings (`omi_m2.py`, `omi_m3_ecgfounder.py --embed*`, `omi_fase_d.py
--embed-staff3`, `omi_fase_e.py --embed-awal --cnn-ami`, `omi_fase_f.py --cnn-benih`): a separate GPU environment
with PyTorch 2.14.0 (CUDA 13.0) and NumPy 2.5.4, called `python-gpu` in the docstrings. Seeds are set in the
scripts.

## Layout

- `analysis/` — scripts. Each docstring gives its inputs, outputs and usage. Order: `omi_hitung_label.py` (label
  counts), `omi_ciri_st.py` and `omi_cek_titik_j.py` (ST amplitudes), `omi_m01.py` (age–sex and ST models),
  `omi_m2.py` (CNN), `omi_m3_ecgfounder.py` (embeddings and probe), `omi_banding.py` (pre-registered comparison),
  `omi_waktu.py` and `omi_diagnostik_st.py`, then the analysis plans in order: `omi_konstruk.py` (plan B),
  `omi_fase_c.py` to `omi_fase_h.py` (plans C–H, with their amendments as options such as `--butir H8`), and
  `omi_gambar.py` (figures). Folds come from `lipatan()` in `omi_m01.py`.
- `logs/` — stdout of the runs, aggregate results only (library warnings removed).
- `results/` — the working notes `Hasil_OMI_0.md` to `Hasil_OMI_14.md` in which every number of the manuscript was
  recorded, with the copied output.
- `preregistration/` — the pre-registration (`Prareg_OMI.md`, with its four deviations) and the analysis plans B–H
  (`Prareg_OMI_B.md` to `Prareg_OMI_H.md`, with amendment P1 in plan G and P1–P5 in plan H), in their final text, and
  `commit_log.txt`, the time each was committed in the authors' working repository before the analysis it governed.
- `subsets/` — `folds.csv`, the patient-grouped five-fold assignment of the 17,622 primary-analysis ECGs for the
  three seeds, stratified by the occlusion label and by the infarction label; `rencana_staff3.csv`,
  `rencana_awal_staff3.csv` and `buang_staff3.csv`, the STAFF III segments (baseline, early and end of inflation)
  and the excluded patients.

Comments, logs, notes and plans are in Indonesian. Glossary: *benih* seed, *lipatan* fold, *selisih* difference,
*keunggulan* gain, *rujukan* baseline, *label teracak* shuffled label, *nol* null, *jarak* delay from ECG to
angiography, *infark* infarction, *oklusi* occlusion, *kuartil* quartile, *aturan baca* reading rule, *penyimpangan*
deviation, *pra-daftar* pre-registration, *latih* train, *uji* test, *potongan* segment, *inflasi* balloon inflation.
Model labels: M0 age–sex, M1 ST amplitudes, M2 CNN, M3a ECGFounder probe. Working notes refer to internal review
rounds and planning files that are not part of this repository.

## Licence

MIT. See `LICENSE`.
