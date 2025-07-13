# Week 1  
Date: 30 June – 6 July 2025  

---

## Summary of Work Completed

- Set up `FUSE_env` and GitHub repository structure.
- Followed the Cui et al. (2024) notebook using the provided half-cell and full-cell files.
- Created `Exploring_cui2024_halfcell_fitting.ipynb` to reproduce SOC alignment and `dV/dQ` analysis. Ran and debugged multiple times to understand each processing step and output.
- Reproduced plots using the two referenced data files. Began reviewing related papers to interpret the plot features and investigate the rationale behind file selection.
- Used helper functions directly from the notebook. Spent time tracing inputs/outputs and exploring how they might be reused or adapted.
- Drafted `dvdq_explained.md` with planned structure and notes for each section.
- Maintained:
  - `battery-terminology.md` (technical glossary)  
  - `Analysis-techs.md` (overview of four core diagnostic methods)  
  - `paper_summary.md` (summaries and questions raised)  
  - `progress-log.md` (this file)

---

## Planned for Week 2

- Investigate the origin and structure of the two example files.
- Apply `dV/dQ` to a new dataset (e.g. Joule 2024).
- Begin simplified implementation of the method.
- Explore PyProBE in parallel.
- Prepare notebooks for `dQ/dV`, `DCS`, and `dP/dE`.
- Finalise glossary and method summaries.
- Attempt charge/discharge segmentation as outlined in the suggested project plan.

---

## GitHub Notes

Working locally on:

- `Exploring_cui2024_halfcell_fitting.ipynb`  
- `dvdq_explained.ipynb`  
- `Analysis-techs.md`  
- `battery-terminology.md`  
- `paper_summary.md`  

First push planned after Week 2 once core content is ready.

# Week 2  
Date: 7 July – 13 July 2025  

---

## Summary of Work Completed

- Created `extract_qv_from_raw_216.ipynb` to process a set of raw formation data (`Nova_Formation-216.csv`) from Cui et al. (2024), extract clean charge Q–V segments, and visualise capacity-voltage relationships.  
  Applied interpolation, Savitzky-Golay smoothing, and gradient calculation to generate `dV/dQ` plots for Cell 216 and explored how smoothing and x-axis choices affected the curve features.
- Built a clean and generalised implementation of the `dV/dQ` pipeline in `analyze_dvdq.ipynb`, separating logic from testing and preparing for batch processing or extension to other datasets.  
  While developing this, I referred to Cui et al.’s `DVF_functions.py` script for structural ideas related to differential voltage analysis—particularly how they handled interpolation, Savitzky-Golay filtering, and gradient computation. I adapted these methods to work directly with raw full-cell aging data, as my focus is on implementing and comparing differential diagnostic techniques rather than reconstructing full-cell curves from half-cell measurements.
- Structured the method documentation in `dvdq_explained.md`, explaining the purpose, implementation, and interpretation of `dV/dQ` analysis, along with technical notes on interpolation and differentiation.
- Based on supervisor suggestion, began applying the pipeline to a second dataset (McMaster, Anselma et al., 2021) to explore cross-dataset applicability of differential analysis methods.  
  Reproduced V–Q and `dV/dQ` plots for one cell at a single mileage point.  
  This dataset was selected in part because it was compiled into a single, well-structured Excel file, making it straightforward to load and apply the same pipeline directly.  
  I first plotted the V–Q curve for a cell from the McMaster dataset and visually compared it to the corresponding result published in the Anselma et al. (2021) paper, confirming consistency.  
  Since the paper did not include any differential diagnostic plots (e.g., `dV/dQ`, `dQ/dV`), I proceeded to apply my own `dV/dQ` analysis to the same cell at that mileage point, as an initial exploration of degradation-related features.
- Maintained:
  - `battery-terminology.md` (technical glossary)
  - `dvdq_explained.md` (in-depth method notes)  
  - `paper_summary.md` (summaries and questions raised)  
  - `progress-log.md` (this file)

---