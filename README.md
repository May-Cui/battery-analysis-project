# Battery Analysis Project
👤 Author: Jimei (May) Cui  
👥 **Supervisors:** Kawa Manmi, Ferran Brosa Planella  
🔗 [LinkedIn](https://www.linkedin.com/in/jimei-cui/) | [GitHub](https://github.com/May-Cui/)

## Project Overview

This project investigates four diagnostic methods for lithium-ion battery degradation:  
- Differential Capacity Analysis (**dQ/dV**)  
- Differential Voltage Analysis (**dV/dQ**)  
- Differential Coulometry Spectroscopy (**DCS**)  
- Differential Power–Energy Analysis (**dP/dE**)  

---
## 🎯 Outputs

The main deliverable of this project is the **poster** presented at the Faraday Institution FUSE 2025 programme.  

- [View Poster PDF](Docs/poster_final.pdf) — official version  
- ![Poster preview](Docs/poster_final.jpg)  
- PPTX source available at `Docs/poster_final.pptx` (optional, for editing)  

Additional outputs:  
- **Figures** — All poster-ready figures are available in `Plots/` (`.png`/`.svg`).  
- **Analysis Pipelines** — Reproducible implementations of dQ/dV, dV/dQ, dP/dE, and LEAN (see `Notebooks/`).  
- **Documentation** — Weekly progress log (`Docs/progress-log.md`) and glossary of key terms (`Docs/battery-terminology.md`).  
---
### Methodological Notes

1. **From DCS to LEAN**  
   The work initially started with the **Differential Coulometry Spectroscopy (DCS)** method, following the BioLogic application note ([Application Note #57](https://www.biologic.net/documents/dcs-battery-application-note-57/)).  
   Later in the literature review, I came across the **LEAN method** proposed by **Feng et al., 2020** ([link](https://www.sciencedirect.com/science/article/pii/S2590116820300084)), which can be understood as a *normalised version* of DCS.  
   Since LEAN provides mathematically stable and comparable outputs across cells, the final comparative study was conducted using **LEAN together with dQ/dV, dV/dQ, and dP/dE**.  

2. **Interpolation vs. Downsampling**  
   In the early stages, I implemented both **interpolation-based** and **filtering/downsampling-based** re-sampling strategies.  
   - With dense datasets, both routes produced similar results.  
   - However, interpolation effectively “creates” points and should only be used for sparse/uneven data, while modern best practice is **downsampling** to preserve fidelity.  
   - All poster figures and main results therefore used the **downsampling + LEAN** route.  

   For reproducibility:  
   - **`40_pipeline_all_methods.ipynb`** → final unified pipeline (downsampling + LEAN, used in poster).  
   - **`30_pipeline_interpolation_dcs.ipynb`** → alternative interpolation + DCS route (kept for exploration).  

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
  - `40_pipeline_all_methods.ipynb`
  - `exploratory/`
    - `explore_multicycle_plots.ipynb`
    - `explore_Borealis_dcs.ipynb`
    - `explore_Borealis_dpde.ipynb`
    - `explore_Borealis_dvdq_dqdv.ipynb`
    - `explore_cui2024_halfcell_fitting.ipynb`

- **Docs/**
  - `progress-log.md`
  - `battery-terminology.md`
  - `bibliography.bib` (optional)

- **Plots/**
  - Poster-ready `.png` figures
  - Intermediate test plots

- `.gitignore`  
- `README.md`

---

## 📊 Data

This project is based on several published lithium-ion battery datasets (raw files not included here due to size):  
1. **Cui et al. (2024) — Half-cell / Full-cell Formation Data** 
- Source: [Zenodo record](https://zenodo.org/records/14577286)
- Used for: Reproducing SOC alignment and dV/dQ analysis, building the first pipeline. 
- Local path example:
Data/raw_data/03032025_cui2024_formation_analysis/Formation/...
2. **McMaster Dataset (Anselma et al., 2021) — LFP Aging Data** 
- Source: [Borealis DOI: 10.5683/SP3/23MFNE](https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/23MFNE) 
- (linked via [McMaster Battery Lab](https://battery.mcmaster.ca/research/#tab-content-datasets-and-algorithms)) 
- Used for: Cross-dataset testing of dV/dQ pipeline at single mileage points. - Local path example:
Data/raw_data/BatteryAging_HEV_A123_LFP/...
3. **Borealis Dataset — Samsung 30T Fast-Charge (Duque et al., 2023)** 
- Source: [Borealis DOI: 10.5683/SP3/UYPYDJ](https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/UYPYDJ) 
- Subfolder used: 03 - CONSTANT CURRENT protocol 
- Used for: Core analysis of all four methods (dQ/dV, dV/dQ, dP/dE, DCS), poster results. 
- Local path example:
Data/raw_data/03-CONSTANT CURRENT protocol_Cycles 0 to 1000/Cycle_0072/...
---

## 📓 Project Notebooks

- `10_extract_qv_from_raw_216.ipynb` — Extract Q–V segments from Cui2024 formation data.  
- `20_dqdv_dvdq_borealis.ipynb` — Implementation of dQ/dV and dV/dQ analysis for Borealis.  
- `30_pipeline_interpolation_dcs.ipynb` — Interpolation-based pipeline (all four methods, exploration only).  
- `40_pipeline_all_methods.ipynb` — Final unified pipeline (downsampling + LEAN, used in poster).  

Exploratory notebooks are stored in `Notebooks/exploratory/`.

---

## 📑 Documentation (`Docs/`)

  - `progress-log.md` — Weekly progress log with overall reflection
  - `battery-terminology.md` — Glossary of technical terms  
  - `bibliography.bib` — (Optional) BibTeX references  
  - `poster_final.pdf` — Final poster (official deliverable)  
  - `poster_final.jpg` — Poster preview image
---

## 📈 Plots (`Plots/`)

- Contains output figures generated by the notebooks.  
- Poster-ready plots (`.png` and `.svg`) are included here.  
- Each figure can be reproduced by running the corresponding notebook.  

