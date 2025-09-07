# 🔋 battery-analysis-project  
👤 **Author**: Jimei (May) Cui  
🔗 [LinkedIn](https://www.linkedin.com/in/jimei-cui/) | [GitHub](https://github.com/May-Cui/)  

👥 **Supervisors**: Kawa Manmi, Ferran Brosa Planella  

---

## 📖 Project Overview  
This repository contains the code, documentation, and outputs from my **Faraday Undergraduate Summer Experience (FUSE) 2025** internship at the University of Warwick.  

Implemented methods:  
- **dQ/dV** — Differential Capacity Analysis  
- **dV/dQ** — Differential Voltage Analysis  
- **DCS** — Differential Coulometry Spectroscopy  
- **dP/dE** — Differential Power–Energy Analysis  
- **LEAN** — Linear Energy Analysis of Noise (extension of DCS, used in final comparisons)  

---

## 🎯 Outputs  

### 🔹 Poster (Main Deliverable)  
- [Poster PDF](Docs/poster_final.pdf) — official version  
- ![Poster preview](Docs/poster_final.jpg)

### 🔹 Additional Outputs  
- **Figures** — Poster-ready plots in `Plots/` (`.png`)  
- **Analysis Pipelines** — Reproducible implementations of dQ/dV, dV/dQ, dP/dE, DCS, and LEAN (`Notebooks/`)  
- **Documentation** — Weekly log (`Docs/progress-log.md`), glossary (`Docs/battery-terminology.md`), and method notes (not included in this repo)  

---

## 🧭 Methodological Notes  

1. **From DCS to LEAN**  
   - Began with **Differential Coulometry Spectroscopy (DCS)** following BioLogic [Application Note #57](https://www.biologic.net/documents/dcs-battery-application-note-57/).  
   - Literature review introduced the **LEAN method** (Feng et al., 2020, [link](https://www.sciencedirect.com/science/article/pii/S2590116820300084)), an *extended version* of DCS.  
   - Final comparative study focused on **LEAN, dQ/dV, dV/dQ, and dP/dE**, as LEAN provided more stable cross-cell outputs.  

2. **Interpolation vs. Downsampling**  
   - Both strategies were tested:  
     - **Interpolation** useful for sparse/uneven data but may “create” points.  
     - **Downsampling** preserves fidelity and is preferred in modern practice.  
   - Poster results used the **downsampling + LEAN route**.  

   Reproducibility:  
   - `40_pipeline_all_methods.ipynb` → **main notebook** containing the final unified pipeline (downsampling + LEAN, used in poster).  
   - `30_pipeline_interpolation_dcs.ipynb` → interpolation + DCS pipeline (kept for exploration).  
   - Earlier notebooks are exploratory and interpolation-based only.  

---

## 📂 Project Folder Structure  

- **Data/**  
  - `raw_data/` — Original downloaded datasets (not uploaded)  
  - `processed_data/` — Downsampled / smoothed outputs  
  - `interp_data/` — Interpolation-based outputs  
  - `monotonic_segments/` — Extracted monotonic Q–V segments  
  - `processed_cache/` — Cached CSVs  

- **Notebooks/**  
  - `10_extract_qv_from_raw_216.ipynb`  
  - `20_dqdv_dvdq_borealis.ipynb`  
  - `30_pipeline_interpolation_dcs.ipynb`  
  - `40_pipeline_all_methods.ipynb` (**key notebook — final pipeline, poster plots generated here**)  
  - `exploratory/` — trial notebooks (multicycle plots, Borealis explorations, Cui2024 half-cell fitting, etc.)  

- **Docs/**  
  - `progress-log.md` — Weekly progress log  
  - `battery-terminology.md` — Glossary of terms  
  - `bibliography.bib` — References (optional)  
  - `poster_final.pdf` — Final poster (official deliverable)  
  - `poster_final.jpg` — Poster preview  

- **Plots/**  
  - Poster-ready `.png`/`.svg` figures  
  - Intermediate test plots  

- `.gitignore`  
- `README.md`  

---

## 📊 Data Sources  

1. **Cui et al. (2024) — Half-cell / Full-cell Formation Data**  
   - [Zenodo record](https://zenodo.org/records/14577286)  
   - Used for: Early exploration, dV/dQ pipeline prototyping  
   - Example path: `Data/raw_data/03032025_cui2024_formation_analysis/Formation/...`  

2. **McMaster Dataset (Anselma et al., 2021) — LFP Aging Data**  
   - [Borealis DOI: 10.5683/SP3/23MFNE](https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/23MFNE)  
   - Used for: Cross-dataset testing of dV/dQ pipeline at single mileage points  
   - Example path: `Data/raw_data/BatteryAging_HEV_A123_LFP/...`  

3. **Borealis Dataset — Samsung 30T Fast-Charge (Duque et al., 2023)**  
   - [Borealis DOI: 10.5683/SP3/UYPYDJ](https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/UYPYDJ)  
   - Subfolder: *03 – CONSTANT CURRENT protocol*  
   - Used for: Core analysis of all four methods, poster results  
   - Example path: `Data/raw_data/03-CONSTANT CURRENT protocol_Cycles 0 to 1000/Cycle_0072/...`  

---

## 📓 Notebooks  

- `10_extract_qv_from_raw_216.ipynb` — Extract Q–V segments (Cui2024)  
- `20_dqdv_dvdq_borealis.ipynb` — dQ/dV and dV/dQ for Borealis dataset  
- `30_pipeline_interpolation_dcs.ipynb` — Interpolation + DCS pipeline (exploration)  
- `40_pipeline_all_methods.ipynb` — **Final unified pipeline (downsampling + LEAN, poster plots)**  
- `exploratory/` — Supplementary tests (multicycle, dpde, etc.)  

---

## 📑 Documentation  

- `progress-log.md` — Weekly progress & reflections  
- `battery-terminology.md` — Glossary of technical terms
- `poster_final.*` — Final poster deliverables  

---

## 📈 Plots  

- Poster-ready `.png` figures  
- Intermediate test outputs  
- Each figure reproducible from the associated notebook  
