# B.0b — ERA5 BASIN-MEAN ACQUISITION LOG

**Component:** B.0b (Chain B, CMIP6 + bias correction)
**Binding spec:** UG_Thesis-v1-locked-edit-2 (eff. 2026-05-27) + 2026-05-29 update log
**Session:** 2026-05-30 (continuation; parents 2026-05-27, 2026-05-29)
**Operator mode:** P1 (upstream-verified)
**Output role:** Empirical target distribution for the basin-mean ERA5-trained QDM (C2 amendment) — PRIMARY D.1 forcing chain.
**Script:** `code/chain_b_cmip6/b0b_era5_basinmean.py`

---

## 1. UPSTREAM VERIFICATION (M1)

| Input | Status | Source |
|-------|--------|--------|
| ERA5 = primary D.1 forcing reference | ✅ | edit-1 §6 ERA5 BASIN-MEAN block; C2 decision 2026-05-14 |
| Polygon source deferred to "session entry" | ✅ resolved here (D4) | edit-1 §6 |
| SW46.9L coords 25.1303 N, 89.7346 E | ✅ locked | edit-1 §5; m4 closed 2026-05-14 |
| Drainage area ~536,000 km² (alt 573,500) | ✅ | Banglapedia / IFCDR 1998 |
| Usable AMS = 34 yr (1988–2024 less 2001/F8, 2011, 2013/Q2a) | ✅ | A2_phase_alpha_per_year_summary.csv |

---

## 2. TECHNICAL FACTS RE-VERIFIED (M3, web search 2026-05-30)

- **Endpoint:** `https://cds.climate.copernicus.eu/api` (post-2024 CDS migration). API key carries **no** deprecated `<UID>:` prefix.
- **Dataset:** `derived-era5-single-levels-daily-statistics` (replaces the legacy ERA5 daily-statistics application).
- **Request keys confirmed:** `product_type`, `variable`, `year`, `month`, `day`, `daily_statistic`, `time_zone`, `frequency`, `area`, `grid`.
- **Variable:** `total_precipitation`, accumulated in **metres**. Conversion **×1000 → mm/day**.
- **ERA5-Land exclusion fact:** the ERA5-Land *derived daily-statistics* product **omits accumulated variables, including total precipitation** — disqualifying it from a daily-product workflow (D1).

---

## 3. DECISIONS RESOLVED THIS SESSION

| # | Decision | Resolution | Rationale (1-line) |
|---|----------|-----------|--------------------|
| D1 | ERA5 vs ERA5-Land | **ERA5 0.25° single-levels** | ERA5-Land daily product lacks tp; 0.1° washed out by basin-averaging; pre-2000 ERA5-Land artefacts |
| D2 | hourly vs daily product | **daily product (`daily_sum`)** + hourly unit cross-check | light/fast transfer off B.1 bandwidth; cross-check closes tp unit footgun |
| D3 | bbox vs regional cube | **bbox via `area` + client-side polygon mask** | A/B distinction collapses for daily data; raw cube retained for provenance |
| D4 | polygon source | **HydroSHEDS pour-point delineation (primary); GRDC Brahmaputra MRB (fallback/area cross-check)** | only pour-point delineation truly means "above the gauge"; MRB terminates negligibly downstream of Bahadurabad |
| D5 | output format | **CSV + NetCDF (CF + provenance)** | CSV git-tracked + auditable; NetCDF archival |

### PROPOSED DEVIATION D15 — calibration window (REQUIRES SIGN-OFF)
- **Spec text:** edit-1 §6 / §14.3 B.4a/b → QDM calibration window **1988–2014 (27 yr)**.
- **Proposed:** **1985–2014 (30 yr)**.
- **Justification:** Cannon, Sobie & Murdock (2015) recommend ≥30 yr for QDM calibration. The QDM calibration window is **independent** of the 1988 discharge-record start; ERA5 (from 1940) and CMIP6 historical (to 2014) both span 1985–2014. The 27-yr figure arose from conflating the calibration window with the C2 **elasticity regression** window, which alone is Q-limited to 1988–2014 (and in practice **n ≈ 24** Q-points after AMS exclusions 2001/2011/2013).
- **Consistency requirement:** the change-factor "historical" baseline P_basin,99,hist must use the SAME window as the QDM calibration → also 1985–2014.
- **Script default:** `CALIB_START = 1985`. Revert by setting `CALIB_START = 1988`.

### PROPOSED DEVIATION D16 — polygon method (REQUIRES SIGN-OFF)
- **Spec text:** edit-1 §6 → "HydroSHEDS Level-3 or GRDC MRB" (session context said "Level 5/6" — contradiction noted).
- **Proposed:** HydroSHEDS pour-point delineation (flow-direction grid, Lehner & Grill 2013) snapped to SW46.9L, area-validated to ~536,000 km² ±10%; GRDC MRB as independent area cross-check and interim input.
- **Justification:** pre-cut Pfafstetter/MRB tiles do not terminate at the gauge; pour-point delineation is the only defensible realisation of "catchment above SW46.9L." Falls within the spec's HydroSHEDS option (uses the same Lehner & Grill 2013 product), executed correctly.

---

## 4. ACQUISITION STRATEGY

- **Spatial:** bbox `[N=31.5, W=82.0, S=23.0, E=97.5]` at 0.25°; trimmed by polygon mask. Lon convention 0–360 vs −180–180 trapped in `basin_mean()` (raises if zero cells inside).
- **Temporal:** **per-year chunking** (one CDS request/year). Restartable — existing non-empty yearly NetCDFs are skipped. Robust to CDS queue timeouts and per-request cost limits.
- **Aggregation:** area-weighted basin mean, weights = cos(lat) over cells whose centroid lies inside the polygon, normalised to 1. Fractional boundary-cell coverage is a documented second-order refinement (negligible for a ~1,900-cell, ~536,000 km² basin; the basin perimeter-to-area ratio makes boundary fraction error <<1%).
- **Footprint:** daily product ≈ 30 MB raw; basin-mean series ~10,958 rows; outputs <10 MB.

---

## 5. UNIT VERIFICATION PROTOCOL (D2, mandatory — record verdict here)

Run once: `python -m chain_b_cmip6.b0b_era5_basinmean --verify-units`
Procedure: download July 1998 **hourly** tp; hand-aggregate (resample 1D sum ×1000) to domain-mean daily mm; compare against `daily_sum`×1000 for the same cells/month. PASS if max |diff| < 0.5 mm.

| Field | Value |
|-------|-------|
| Sample period | 1998-07 (monsoon peak; 1998 = major flood year, amax 103,129 m³/s) |
| Hourly-aggregated domain-mean (mm) | _<paste from run>_ |
| daily_sum product domain-mean (mm) | _<paste from run>_ |
| max \|diff\| (mm) | _<paste>_ |
| Verdict | _PASS / REVIEW_ |
| Conversion confirmed | ×1000 (m→mm) _Y/N_ |

> If REVIEW: inspect the daily day-boundary/accumulation-shift convention (ERA5 tp at 00:00 UTC = accumulation 23:00→00:00 of the previous day) before trusting the series for P₉₉.

---

## 6. OUTPUTS

| Artefact | Path | Tracked? |
|----------|------|----------|
| Raw yearly cubes | `results/era5_raw/era5_tp_dailysum_<YYYY>.nc` | git-ignored |
| Basin-mean CSV | `results/baseline/era5_basinmean_brahmaputra_1985_2014.csv` | **tracked** |
| Basin-mean NetCDF | `results/baseline/era5_basinmean_brahmaputra_1985_2014.nc` | **tracked** |

NetCDF global attrs record dataset id, daily_statistic, calibration window, polygon path, validated area, n cells, unit-conversion provenance, and citations (Hersbach 2020; Cannon 2015).

---

## 7. OPEN ITEMS / DOWNSTREAM HOOKS

- [ ] D15 / D16 sign-off → fold into Edit-3 reissue.
- [ ] Catchment polygon delineated and committed to `data/gis/` (D4 primary path).
- [ ] Unit-verification verdict pasted into §5 above.
- [ ] B.4b QDM consumes this series as the ERA5 reference (calibration window must match D15).
- [ ] C2 elasticity regression: separate window 1988–2014 (n≈24), NOT 1985–2014 — do not propagate D15 to the elasticity step.
- [ ] Reviewer-vulnerability ledger: 27-yr→30-yr resolves the Cannon-2015 exposure on the bias-correction calibration; the elasticity regression's n≈24 remains a (smaller, correctly-scoped) limitation for Ch.7.

---

## 8. GOVERNANCE NOTE

D15 and D16 modify binding-spec text (edit-1 §6/§14.3) and therefore require deviation-log entries under Appendix B protocol. This log records them as PROPOSED pending user sign-off; the binding spec remains authoritative until Edit-3 is reissued.
