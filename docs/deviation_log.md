# Deviation Log — thesis-rp-migration

Per §14.5 of `UG_Thesis-v1-locked-edit-1`. Every departure from the LOCKED configuration is logged here. New entries appended chronologically below the pre-seeded baseline.

---

## Pre-seeded entries (2026-05-11, carried forward from v1-LOCKED-edit-1 Appendix A)

### Deviation 2026-05-11: [V3-FINAL §5, §6, §8] D1 — Study area pivot
- **Trigger:** Surma–Kushiyara flash-flood regime incompatible with daily-resolution AMS + daily CMIP6 forcing chain.
- **Section invoked:** §5 fallback elevation; R7 deactivated for primary; R8 newly activated for D.1 change-factor AMS.
- **Substitution:** Primary = BWDB SW46.9L (Bahadurabad Transit, Brahmaputra/Jamuna left bank, river-km 46.9, 25.1303°N 89.7346°E). Sylhet SW267 demoted to §5 fallback.
- **Justification:** Mainstem slow-rise regime methodologically consistent with daily AMS framing; cluster comparability with Mohammed 2018, Gädeke 2022, Khalequzzaman 2023, Aishi 2026 enabled.
- **Novelty impact:** Lose haor-regime axis; retain (i)–(iv) joint claim at Bahadurabad.
- **Supervisor notified:** 2026-05-11
- **Chapter sections to update:** Ch.1, Ch.3, Ch.4, Ch.5, Ch.7.

### Deviation 2026-05-11: [V3-FINAL §6, §14.3] D2 — BC route resolution
- **Trigger:** Mishra 2020 uses EQM, not QDM; internal inconsistency with §14.3 QDM specification.
- **Section invoked:** CL-1.
- **Substitution:** Own QDM (Cannon, Sobie & Murdock 2015) via xclim, trained on gridded BMD reference, primary route. Mishra 2020 EQM demoted to U3c comparator only.
- **Justification:** QDM trend-preservation property essential for RP-migration interpretation (Cannon 2015 §3.2).
- **Novelty impact:** Strengthens N3 axis content.
- **Chapter sections to update:** Ch.5 §Methodology.

### Deviation 2026-05-11: [V3-FINAL §6] D3 — GCM list rationale rewording
- **Trigger:** ACCESS-CM2 not in ISIMIP3b primary set; old rationale invoked ISIMIP3b dependence.
- **Section invoked:** CL-5; §6 rationale text.
- **Substitution:** GCM list retained (ACCESS-CM2, MPI-ESM1-2-HR, GFDL-ESM4) with rewritten rationale; acquisition route = raw ESGF.
- **Justification:** ISIMIP3b DOI 10.48364/ISIMIP.842396.1 primary set excludes ACCESS-CM2; raw ESGF coverage verified.
- **Novelty impact:** None (text-only).

### Deviation 2026-05-11: [V3-FINAL §4] D4 — Aishi 2026 mischaracterisation
- **Trigger:** Original entry described "GBM trunk, monthly" — actual is Ganges, Jamuna, Padma rivers individually, horizon 2051–2070.
- **Section invoked:** §4.
- **Substitution:** Rewritten per Section 4.
- **Justification:** Verified against Appl. Comput. Geosci. 29:100327.
- **Novelty impact:** Strengthens contrast on monthly-vs-daily and horizon offset.

### Deviation 2026-05-11: [V3-FINAL §9, §14.3 E.3] D5 — ANOVA design
- **Trigger:** "Monte Carlo N=500" on saturated 54-cell factorial has zero genuine residual; ANOVA underspecified.
- **Section invoked:** §14.3 E.3, §9.
- **Substitution:** Full-factorial 54-cell deterministic + parametric within-cell bootstrap B=200 (10,800 realisations); Type-II ANOVA with bootstrap residual.
- **Justification:** Bosshard 2013 WRR 49:1523; Meresa 2022, Hattermann 2018 bootstrap extension.
- **Novelty impact:** Strengthens N3.

### Deviation 2026-05-11: [V3-FINAL §14.3 A.3] D6 — SAR speckle filter
- **Trigger:** Refined-Lee not built-in to GEE.
- **Section invoked:** §14.3 A.3, §13 anchor promotion.
- **Substitution:** Mullissa et al. 2021 `gee_s1_ard` pipeline (multi-temporal Lee primary, mono-temporal Refined-Lee fallback, GEE `focal_mean` last-resort).
- **Justification:** Mullissa et al. 2021 Remote Sens. 13:1954 peer-reviewed.
- **Novelty impact:** None.

### Deviation 2026-05-11: [V3-FINAL §6] D7 — GloFAS v4.0 coverage
- **Trigger:** Original §6 stated "GloFAS v4.0 1979–2025"; actual is 1980-01-01 to 2022-07-31.
- **Section invoked:** §6 OBSERVED DISCHARGE Tier 3.
- **Substitution:** Corrected; added Appendix D for GloFAS-vs-BWDB cross-validation.
- **Justification:** ECMWF release notes (2022), JRC v4.0 catalogue.
- **Novelty impact:** None.

### Deviation 2026-05-11: [V3-FINAL §5, §6] D8 — Station ID lock
- **Trigger:** Original "Sylhet (BWDB)" lacked station ID; superseded by Bahadurabad pivot.
- **Section invoked:** §5, §6, §14.3.
- **Substitution:** Primary = BWDB SW46.9L Bahadurabad Transit, 25.1303°N 89.7346°E, river-km 46.9.
- **Justification:** BWDB Hydrology Directorate station catalogue; Banglapedia drainage area (536,000 km²); IFCDR 1998 (573,500 km²); Rao et al. 2020 long-record context.
- **Novelty impact:** Locked.

### Deviation 2026-05-11: [V3-FINAL §4, §13] M1 — Khalequzzaman 2023 promotion
- **Trigger:** Mischaracterised as "precipitation tail only, no hydraulics".
- **Section invoked:** §4, §13.
- **Substitution:** Promoted to direct competitor; Brahmaputra-basin overlap acknowledged.
- **Justification:** Verified against Springer Natural Hazards Ch.16.
- **Novelty impact:** Raises novelty bar; joint (i)–(iv) intact.

### Deviation 2026-05-11: [V3-FINAL §14.3 D.6] M2 — RP-migration formula
- **Trigger:** F_proj non-exceedance vs exceedance ambiguous.
- **Section invoked:** §14.3 D.6.
- **Substitution:** F explicitly = non-exceedance CDF; T_future computation expanded; [1, 500] yr boundary handling in main algorithm.
- **Justification:** Slater et al. 2021 GRL convention.
- **Novelty impact:** None.

### Deviation 2026-05-11: [V3-FINAL §8, Ch.7] N1 — IDW orographic limitation
- **Trigger:** IDW smooths orographic gradients; previously undocumented.
- **Section invoked:** §8 V2, Ch.7 §Limitations.
- **Substitution:** Documented (no methodological change); cite Prakash 2015.
- **Justification:** R6 honest scope.
- **Novelty impact:** None.

### Deviation 2026-05-11: [V3-FINAL §8 CL-3] N2 — calibration-window framing
- **Trigger:** "Cal-window sensitivity 1988–2014 vs 1993–2014" on fixed held-out 2015–2022 tests sample-size, not climate-period.
- **Section invoked:** §8 V2, CL-3.
- **Substitution:** Reframed explicitly as sample-size sensitivity.
- **Justification:** R6.
- **Novelty impact:** None.

### Deviation 2026-05-11: [V3-FINAL §7 Chain C] N3 — Option β pre-commit
- **Trigger:** Timeline arithmetic; CL-1 + CL-2 workload renders Option α infeasible.
- **Section invoked:** §7 Chain C, §12 R9.
- **Substitution:** HEC-RAS excluded; Day-5 binary gate eliminated; R9 active in Ch.1, Ch.5, Ch.7; R8 active for D.1.
- **Justification:** Timeline arithmetic.
- **Novelty impact:** None.

### Deviation 2026-05-14: [v1-LOCKED-edit-1 §6, §14.1 Chain B] C2 — Dual-track BC training reference
- **Trigger:** BD-local BMD precipitation insufficient as forcing reference for ~536,000 km² Brahmaputra catchment dominated by upstream (Tibet/Assam/Bhutan) precipitation.
- **Section invoked:** Update Log 2026-05-14 amendment C2 (option b″).
- **Substitution:** D.1 forcing chain bias-corrected against ERA5 basin-mean over Brahmaputra catchment polygon above SW46.9L (1988–2014). BMD-trained QDM retained for BD-territory rainfall validation only. tasmax/tasmin acquired for archival per m1 decision; reclassified supplementary.
- **Justification:** Rao et al. 2020 Nat. Commun. 11:6017 upper-basin precipitation control. ERA5 0.25° per Hersbach et al. 2020.
- **Novelty impact:** None (methodological refinement; strengthens defensibility of D.1).
- **Chapter sections to update:** Ch.4 §Data, Ch.5 §Methodology, Ch.7 §Limitations.

---

## New entries (append below)

### Deviation 2026-05-19: [Component A.1] LIM-A1-1 — GEE interactive personal-account auth
- **Trigger:** D-A1-2 decision favoured personal-account interactive auth over service-account auth for setup speed in a 30-day sprint.
- **Section invoked:** R10 (reproducibility); §14.6 reproducibility infrastructure.
- **Substitution:** N/A — this is an accepted limitation, not a methodological substitution.
- **Justification:** Service-account setup requires a Google Cloud project with billing enabled and key-file management; for a 30-day single-author UG thesis on a single workstation this overhead is disproportionate. Personal-account auth produces methodologically identical satellite outputs.
- **Reproducibility cost:** Reviewers reproducing Chain A must authenticate independently via their own GEE-enabled Google account. Identity of authenticator does not affect output values, only the credential at acquisition time. Acquisition-date metadata logged per scene to enable reviewer replication of the exact monsoon scene set.
- **Novelty impact:** None.
- **Supervisor notified:** Pending (Day-0 setup memo).
- **Chapter sections to update:** Ch.5 §Methodology (GEE auth subsection); Appendix A (Scripts: GEE auth step note).

<!-- Format per §14.5:
## Deviation YYYY-MM-DD: [Component {ID}] - [trigger]
- **Trigger:**
- **Section invoked:**
- **Substitution:**
- **Justification:**
- **Novelty impact:**
- **Supervisor notified:**
- **Chapter sections to update:**
-->
### A.1 closure 2026-05-19: Component A.1 complete
- **Status:** verify_a1.py exit 0 confirmed.
- **Tag:** v0.1.0-alpha pushed.
- **Setup deviations logged:** LIM-A1-1 (GEE personal-account auth), LIM-A1-2 (GEE notebook-mode auth, GCP project registration friction).
- **Open dependencies for downstream chains:** CDS API registration (deferred to Chain B.0b, Day 3–4); BWDB Excel structural audit (deferred to A.2 session).
- **No methodological deviation; no rollback condition invoked.**
