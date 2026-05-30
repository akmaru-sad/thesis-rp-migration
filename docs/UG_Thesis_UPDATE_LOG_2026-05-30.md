# UG_THESIS UPDATE LOG — 2026-05-30 (B.0b session)

Appends to the 2026-05-29 log. Binding spec remains UG_Thesis-v1-locked-edit-2
until Edit-3 reissue. Entries below are session decisions + two PROPOSED
deviations requiring user sign-off.

---

## B.0b ACQUISITION DECISIONS (D1–D5) — ACCEPTED

- **D1 ERA5 vs ERA5-Land → ERA5 0.25° single-levels.** ERA5-Land derived
  daily-statistics product omits accumulated variables (incl.
  total_precipitation), forcing hourly self-aggregation; 0.1° resolution
  advantage is immaterial after basin-averaging over ~536,000 km²; ERA5-Land
  pre-2000 precip artefacts avoided.
- **D2 daily product + hourly unit cross-check.** Dataset
  `derived-era5-single-levels-daily-statistics`, `daily_statistic=daily_sum`,
  `frequency=1_hourly`, `time_zone=utc+00:00`. Mandatory one-month hourly
  cross-check verifies the m→mm (×1000) conversion and day-alignment.
- **D3 bbox + client-side polygon mask.** `area` server-side subset, then
  cos(lat)-weighted basin mean over centroid-in-polygon cells.
- **D4 polygon source (see D16).**
- **D5 outputs CSV + NetCDF.** CSV tracked in `results/baseline/`.

## PROPOSED DEVIATION D15 — QDM calibration window 1988–2014 → 1985–2014

- **Trigger:** edit-1 §6 / §14.3 B.4a/b specify a 27-yr (1988–2014) QDM
  calibration window, flagged as a reviewer vulnerability.
- **Finding:** the window was set by conflating the QDM calibration window
  with the C2 elasticity-regression window. Only the latter is Q-limited to
  1988–2014 (and is n≈24 after AMS exclusions 2001/2011/2013). The QDM
  calibration depends only on ERA5 (from 1940) ∩ CMIP6-historical (to 2014).
- **Decision:** set QDM calibration AND change-factor historical-baseline
  window to **1985–2014 (30 yr)**, satisfying Cannon, Sobie & Murdock 2015.
  The C2 elasticity regression window is UNCHANGED at 1988–2014.
- **Affected text:** §6 ERA5 BASIN-MEAN block (1988–2014 → 1985–2014);
  §14.3 B.4a/b calibration-window strings; D.1 change-factor P_hist window.
- **Status:** PROPOSED — awaiting sign-off; fold into Edit-3.

## PROPOSED DEVIATION D16 — catchment polygon method

- **Trigger:** edit-1 §6 offers "HydroSHEDS Level-3 or GRDC MRB"; session
  context said "Level 5/6" (contradiction). Neither pre-cut polygon
  terminates at SW46.9L.
- **Decision:** delineate catchment via HydroSHEDS flow-direction grid
  (Lehner & Grill 2013) snapped to the SW46.9L pour point; validate area to
  ~536,000 km² ±10%; retain GRDC Brahmaputra MRB as independent area
  cross-check and interim input. Treated as correct execution of the spec's
  HydroSHEDS option, not a new source.
- **Status:** PROPOSED — awaiting sign-off; fold into Edit-3.

## CARRY-FORWARD

- Edit-1 C2 (basin-mean ERA5-trained QDM primary) and m1 (tasmax/tasmin
  supplementary) unchanged.
- B.1 bulk acquisition continues unattended (8 tuples).
- Reviewer-vulnerability ledger: D15 retires the Cannon-2015 exposure on the
  bias-correction calibration sample.
