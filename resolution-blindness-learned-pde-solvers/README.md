# Resolution blindness and certification of learned PDE solvers

Public reproducibility package prepared for the Nature Communications transfer manuscript.

## Scope
This repository layer contains the minimum source-data tables and plotting scripts that reproduce all four main figures and eight Supplementary figures in the transfer manuscript. It also records the software environment and the provenance crosswalk linking manuscript claims to the original computational artifacts.

## Reproduce the figures
1. Create the Python environment from `environment.yml` or install `requirements.txt`.
2. Run `python generate_main_figures.py`.
3. Run `python generate_supplementary_figures.py`.
4. Generated files are written to `figures_generated/`; compare them with the manuscript/Supplementary figures in the submission package.

## Scientific-computation archives
The full peer-review computation used additional archives prepared with the submission:
- `Nature_Source_Data_v3.zip`
- `Code_Review_Package_v1.zip`
- `Nature_GINO_Baseline_v2.zip`
- `Additional_Review_Material_v1.zip`

Those archives contain the central solver/training code, larger case-level outputs, meshes/snapshots, GINO reimplementation materials and other reviewer artifacts. They remain part of the journal peer-review package and will be incorporated into the final DOI-minting archival release after a final disclosure/security scan.

## Integrity boundaries
- The GINO result is an architecture-matched PyTorch reimplementation, not official-package output.
- Selective correction is applied to the mesh-native reduced surrogate, not directly to Geo-FNO or GINO.
- The two-dimensional post-correction certificate is discrete relative to the stabilized finite-element reference.
- The compact CSV files in `source_data/` are packaging derivatives of locked source tables; they do not introduce new model training or new scientific results.

## Licensing
- Code: MIT License; see `LICENSE_CODE`.
- Source data and documentation: Creative Commons Attribution 4.0 International (CC BY 4.0); see `LICENSE_DATA`.

## Citation and archival DOI
Public repository URL:
https://github.com/ajaynitw1995/my/tree/main/resolution-blindness-learned-pde-solvers

A persistent DOI will be minted for the final archival release before publication. Once available, the DOI will be added to `CITATION.cff`, `.zenodo.json`, and the manuscript Data/Code Availability statements.
