# Satellite-Constrained Return-Period Migration of Flood Hazard at Bahadurabad (Brahmaputra / Jamuna) under CMIP6 Climate Scenarios

**Status:** v0.1.0-alpha · 30-day undergraduate thesis sprint · LOCKED configuration (v1-LOCKED-edit-1, 2026-05-14)

## Scope

This thesis links satellite-derived historical flood evidence, station-based multi-distribution flood-frequency analysis, and CMIP6-driven future-climate signals to estimate how historical flood return periods migrate at BWDB station SW46.9L (Bahadurabad Transit, Brahmaputra/Jamuna left bank) under SSP2-4.5 and SSP5-8.5 by 2041–2070, with four-source uncertainty attribution.

**One station · 3 GCMs · 2 SSPs · 1 horizon · NO HEC-RAS · daily QDM-BC chain · 4-source ANOVA UQ with bootstrap.**

## Repository Map

```
thesis-rp-migration/
├── code/
│   ├── chain_a_satellite/   Sentinel-1 ARD + Landsat MNDWI (GEE + Python)
│   ├── chain_b_cmip6/       ESGF acquisition + QDM bias correction + IDW gridding
│   ├── chain_d_ffa/         Multi-distribution FFA + RP-migration
│   ├── chain_e_uq/          ANOVA + within-cell bootstrap + tornado
│   └── utils/               Shared I/O, paths, logging, A.1 verification
├── data/                    Raw/processed data (all gitignored except .gitkeep)
├── results/                 Outputs by chain (.parquet, .csv, .pdf, .png)
├── docs/
│   ├── chapters/            Ch.1–Ch.8 + appendices (Markdown)
│   ├── supplementary/
│   └── deviation_log.md     Pre-seeded with v1-LOCKED-edit-1 deviations
├── notebooks/               Exploration notebooks (committed with cells stripped)
├── tests/                   pytest gates
├── environment.yml          conda-forge geo stack
├── requirements.txt         pip-pinned Python-pure libs
├── pyproject.toml           Declares thesis_rp_migration as local package
├── .pre-commit-config.yaml  Enforced: black, isort, nbstripout
├── .env.example             Template for DATA_ROOT etc.
├── A1_SETUP.md              Setup runbook (READ THIS FIRST)
├── LICENSE                  MIT (code)
└── LICENSE-DATA             CC-BY-4.0 (docs, figures, derived results)
```

## Quick Start

1. Read `A1_SETUP.md` — the setup runbook
2. Run `python code/utils/verify_a1.py` — must exit 0 before any other work
3. See `docs/chapters/` for chapter drafts as they accrue

## Citation

See `CITATION.cff`. Zenodo DOI will be minted on submission.

## License

- **Code:** MIT (see `LICENSE`)
- **Documentation, figures, derived results:** CC-BY-4.0 (see `LICENSE-DATA`)
- **Raw data (BWDB, BMD, restricted-redistribution extracts):** NOT redistributed. See `.gitignore`.

## Reproducibility Caveats (per R10)

- GEE authentication uses interactive personal account; reproduction requires reviewer authentication
- BWDB raw discharge/stage data NOT redistributed (licensing pending); derived AMS and QC diagnostics deposited to Zenodo on submission
- BMD station network raw data NOT redistributed; gridded reference deposited to Zenodo only if redistribution licence permits, otherwise IDW correction factors + station list only

## Contact

Author: [TO FILL] · ORCID: [TO FILL] · Supervisor: [TO FILL]
