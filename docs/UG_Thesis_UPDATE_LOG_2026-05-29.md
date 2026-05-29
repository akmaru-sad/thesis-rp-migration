# UG_Thesis Binding-Spec Update Log — 2026-05-29

**Effective date:** 2026-05-29
**Supersedes:** UG_Thesis-v1-locked-edit-2 (2026-05-27)
**Prepares for:** UG_Thesis-v1-locked-edit-3 (forthcoming, this update log is the change set)
**Author:** Look Sad, Environmental Engineering UG thesis
**Title:** Satellite-Constrained Return-Period Migration of Flood Hazard at Bahadurabad (Brahmaputra/Jamuna) under CMIP6 Climate Scenarios

---

## Scope of this update

This log records the closure of pre-session Check 6b (ESGF acquisition path) and finalises the substantive changes that arose during its execution. Three items: D14 finalisation, P-REST acquisition protocol, and a sharpening of the data-availability verification protocol. No scope reductions. No rollback triggered. Binding scope (station, GCMs, SSPs, horizon, FFA, novelty claims) unchanged.

---

## 1. Closure of Check 6b — ESGF acquisition path

### 1.1 What was checked

Pre-session Check 6b required verification that CMIP6 daily `pr` for the locked matrix — three GCMs (ACCESS-CM2, MPI-ESM1-2-HR, GFDL-ESM4) × three experiments (historical, ssp245, ssp585) × variant `r1i1p1f1` × grid `gn` or `gr` — is recoverable on the no-auth path documented in the parent-session brief (2026-05-27).

### 1.2 What was found

The post-Globus ESGF federation is in an interim partitioned state, with the Europe/AU SOLR domain (DKRZ, NCI, CEDA, IPSL) and the US Globus/ElasticSearch domain (ORNL backbone after LLNL shutdown 2025-07-29) holding non-identical replicas. Within the Europe/AU domain, all 9 locked tuples are recoverable but require three indices, not two:

- ACCESS-CM2 daily `pr` `r1i1p1f1` → published at NCI, not replicated to DKRZ or CEDA for daily fields
- MPI-ESM1-2-HR daily `pr` `r1i1p1f1` → published at DKRZ, not replicated to NCI or CEDA for daily fields
- GFDL-ESM4 daily `pr` `r1i1p1f1` → replicated to CEDA (all three experiments), additionally mirrored at `esgf3.dkrz.de` for SSP245

The parent-session assertion that "both DKRZ and NCI host all three GCMs at Level 3" was incorrect for GFDL-ESM4 daily `pr` and overstated for ACCESS-CM2 and MPI-ESM1-2-HR (each hosted at exactly one of the two named nodes). Direct SOLR REST querying with `distrib=true` and `replica=true` against DKRZ as a federation entry point confirmed all 9 tuples present across the three-node configuration.

### 1.3 What was rejected

The `intake-esgf` Python library failed on this environment with a reproducible `ValueError: Must have equal len keys and value when setting with an iterable` during DataFrame assembly for SOLR-indexed sources (ACCESS-CM2, MPI-ESM1-2-HR), and returned spurious empty results for GFDL-ESM4 because the library does not propagate `distrib=true` semantics consistently across SOLR indices. The library was abandoned as the acquisition driver. The bug is reproducible and should be reported to `https://github.com/esgf2-us/intake-esgf`.

### 1.4 What was adopted

Direct SOLR REST queries via `urllib.request` (Python standard library) against the DKRZ endpoint with `distrib=true` and `replica=true`, followed by per-dataset wget-script generation via the ESGF wget endpoint, executed with the `-s` flag per ESGF documentation for the post-OpenID transition period. The acquisition path is unauthenticated end-to-end. A single-file pilot download confirmed the path works on residential-grade Bangladesh network connectivity.
## 1a. Closure of Check 6a — CDS API path (added 2026-05-29 afternoon)

CDS API (Copernicus Climate Data Store) verified operational for ERA5
acquisition. Three verifications completed:

- `cdsapi` Python library installed in `esgf` mamba environment
- `~/.cdsapirc` configured with current post-migration URL
  (`https://cds.climate.copernicus.eu/api`) and personal access token
- End-to-end smoke test (`b0_cds_smoke_test.py`) returned a valid
  NetCDF for a minimal ERA5 reanalysis-single-levels request

B.0b (ERA5 basin-mean acquisition over the Brahmaputra catchment
polygon above SW46.9L, 1988–2014 historical reference for QDM
training per C2 amendment) is now unblocked.

Per parent-session brief's noted common failure modes: (1) per-dataset
licence acceptance was performed in browser before API call; (2) URL
field in ~/.cdsapirc uses the post-migration endpoint, not the
deprecated `/v2` form found in older tutorials.
---

## 2. Deviation D14 — finalised (replaces pending wording)

### 2.1 Final wording for §14.3 B.1

D14 (effective 2026-05-29): B.1 CMIP6 acquisition uses direct ESGF SOLR REST querying against `https://esgf-data.dkrz.de/esg-search/search` with parameters `distrib=true`, `replica=true`, `latest=true`, `type=Dataset`. Federated queries reach the Europe/AU SOLR partition (DKRZ + NCI + CEDA + IPSL). Per-dataset wget scripts are fetched from `https://esgf-data.dkrz.de/esg-search/wget` and executed with `-s` to bypass the deprecated OpenID prompt. No authentication is used. The legacy `esgf-pyclient` library and the `intake-esgf` wrapper are deprecated for this work: the former is incompatible with the post-Globus federation, the latter has a reproducible DataFrame-assembly bug on the current SOLR index responses (see §1.3).

### 2.2 Reproducibility upgrade (R10)

The no-auth REST + wget acquisition path is a documented R10 improvement over cluster precedent. Any reader can replicate without credentials, eduGAIN membership, institutional affiliation, or Globus identity. Document this explicitly in Ch.4 §Data as a deliberate methodological choice and note the partitioned-federation interim state under which the acquisition was performed (2026-05-29). Cite the ESGF transition announcement (`https://wcrp-cmip.org/esgf-information/`) and the DKRZ ESGF user-account documentation as supporting evidence for the no-auth claim.

---

## 3. New protocol entry — P-REST (data-availability verification)

**Protocol P-REST (effective 2026-05-29):** Data-availability verification for ESGF-hosted datasets is performed via direct SOLR REST queries with the full filter set actually used in acquisition (`project`, `source_id`, `experiment_id`, `variable_id`, `table_id`, `variant_label`, `grid_label`), not by coarser facet enumeration or web-UI inspection. Library wrappers are convenience layers and are not authoritative for availability determinations. Verification queries must include `distrib=true` and `replica=true` to surface replicated holdings, and must be timestamped with both the query URL and the response `numFound` count for audit. M3 (no DOI/library hallucination) extends to library-reported availability: a library reporting an empty result is not evidence of absence until verified by REST.

---

## 4. R-1 status — not triggered

R-1 (Mishra 2020 EQM replaces QDM as primary if CMIP6 data unrecoverable on no-auth path) was reworded in edit-2 with trigger "if intake-esgf returns 0 datasets for ≥2 of 3 locked GCMs by Day 4." Under the P-REST protocol, library-reported emptiness no longer constitutes a valid R-1 trigger. Updated trigger wording for edit-3:

**R-1 (revised):** If REST-verified availability shows 0 datasets at Level 4 (full filter set including variant_label) across the Europe/AU SOLR partition (DKRZ + NCI + CEDA + IPSL) AND the US-domain Globus/ElasticSearch index for ≥2 of 3 locked GCMs, revert CL-1 to Mishra 2020 EQM as primary bias correction. Library-reported emptiness is excluded as a trigger.

Status 2026-05-29: R-1 not triggered. All 9 tuples verified present at Level 4 on the Europe/AU partition.

---

## 5. Sharpening of pre-session check protocol

Three lessons from Check 6b execution that bind on all subsequent pre-session checks:

1. **Level confirmation must specify filter depth.** "Hosts the GCM" (Level 1) is not equivalent to "hosts the GCM's daily `pr` for `r1i1p1f1`" (Level 4). All future check artefacts must record the filter set used. This is now formally protocol entry P-LEVEL.

2. **Library tooling is not the ground truth for federation state.** Direct REST or browser-UI inspection takes precedence over library output when the two disagree. This formalises as protocol entry P-GROUND-TRUTH.

3. **Federation partitioning may require multi-index queries.** A single-node query is insufficient evidence of absence; cross-domain federated queries are required before any data-gap finding is declared. This formalises as protocol entry P-FED.

P-LEVEL, P-GROUND-TRUTH, and P-FED bind on all remaining pre-session checks and on any future data-availability re-verification.

---

## 6. Timeline impact

Check 6b consumed approximately 6 hours of execution time on 2026-05-29 (diagnostic, library debugging, REST pivot, pilot download). Net schedule slip: 0 days. The 30-day timeline remains intact. Check 6a (CDS API registration) can proceed in parallel from 2026-05-30 while the bulk CMIP6 downloads run unattended. Check 6c (FFWC bulletin audit) remains scheduled for the next 2–3 days per the parent-session brief.

---

## 7. Outstanding items for edit-3

The following will be folded into UG_Thesis-v1-locked-edit-3 when the binding spec is reissued:

- D14 final wording per §2.1 above
- Protocol entries P-REST, P-LEVEL, P-GROUND-TRUTH, P-FED added to §13 session protocol
- R-1 trigger reworded per §4 above
- §14.3 B.1 acquisition method updated to reference REST + wget per D14
- Ch.4 §Data text updated per §2.2 R10 documentation
- Appendix B updated with this update log as the edit-3 change set basis

---

## 8. References

- ESGF transition announcement: `https://wcrp-cmip.org/esgf-information/`
- DKRZ ESGF user account documentation: `https://docs.dkrz.de/doc/getting_started/getting-a-user-account/esgf-user-account.html`
- ESGF federated nodes list: `https://esgf.github.io/nodes.html`
- ESGF Next-Gen migration: scheduled for May 2026 per the WCRP announcement; the present acquisition predates the migration and is documented under the interim partitioned state
- Parent-session brief: 2026-05-27 (Check 6 dependency block)
- This update log artefact (repo): `docs/B1_acquisition_<UTC-timestamp>.log` and `docs/B1_acquisition_manifest_<UTC-timestamp>.json`

---

**End of update log 2026-05-29.**
