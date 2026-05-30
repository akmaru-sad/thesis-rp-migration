# Check 6c Closure Log — FFWC Bulletin Inventory for A.7

**Closure date:** 2026-05-30
**Pre-session check:** 6c — FFWC bulletin audit (carried-forward dependency block from A.1 closure 2026-05-27)
**Status:** **CLOSED**
**Deliverables:**
- `docs/ffwc_bulletin_inventory.md` (current pointer → v2.1)
- `docs/ffwc_bulletin_inventory_v2.1.md` (URL-verified closeout)
- `scripts/fetch_ffwc_afrs.sh` (AFR fetch helper)
- `data/ffwc/AFR_{2017,2018,2019,2020,2021}.pdf` (fetched 2026-05-29 by user)
**Binding spec:** UG_Thesis-v1-locked-edit-2 (2026-05-27), §14.3 A.7 / §F4
**Blocks unblocked:** A.7 opening (Day 6 of 30-day timeline); F4 satellite-extent composite scope
**Carry-over:** 1998 F4 inclusion contingent on Landsat-5 TM QC, decided during A.5 phase

---

## 1. Original framing (session brief 2026-05-27, Check 6c)

> "NEEDED FOR: A.7 (FFWC bulletin validation on 1988, 1998, 2017, 2020, 2022 flood events at Bahadurabad; one of two satellite validation events per V1 §8). … User must inventory year-by-year recoverability of FFWC daily flood-bulletin PDFs: Recent years (2017+): likely online at http://www.ffwc.gov.bd/; 2010–2016: patchy; Pre-2010 (1988, 1998): almost certainly paper-only at BWDB/FFWC Dhaka HQ; physical visit needed, or secondary citation via Mirza 2003 / Islam & Chowdhury / Hofer & Messerli 2006."
>
> "Acceptance: docs/ffwc_bulletin_inventory.md exists with per-event-year status (recoverable / pending FFWC / using secondary citation / dropped from F4)."

## 2. Empirical findings that revised the framing

Three operating premises in the session brief were falsified during the audit. Each is recorded here because the same wrong assumption can otherwise leak into Ch.4.

| # | Brief premise | Empirical finding | Source / verification |
|---|---|---|---|
| F1 | Daily flood bulletins recoverable online for 2017+ | **Daily bulletins are not archived online for any year.** The live `ffb.pdf` and `fsumm.pdf` PDFs on `old.ffwc.gov.bd/images/` are overwritten on each issuance cycle. The new portal `ffwc.bwdb.gov.bd` exposes historical *water-level data* via API but no bulletin PDF archive. | Direct portal audit 2026-05-29 |
| F2 | Annual Flood Reports availability unknown | **AFR 2008–2021 hosted online as direct PDFs** at `old.ffwc.gov.bd/images/annual{YY}.pdf`; **AFR 2022 not yet published online as of 2026-05-30**; AFRs typically run 12–24 months behind flood year. AFRs are the post-event consolidated narrative documents with chronologies, peak WL tables, and station-by-station flood-day counts — methodologically stronger than the live daily bulletins they supersede. | Portal directory listing fetched 2026-05-29 |
| F3 | Pre-2010 events require physical HQ visit | **Peer-reviewed secondary citations covering 1988 and 1998 are accessible via DOI** and methodologically equivalent or stronger than student-transcribed paper bulletins. Mirza 2003 *Nat. Hazards* 28(1):35–64 covers 1987 + 1988 + 1998 in a single hydro-meteorological analysis; Chowdhury 2000 *Nat. Hazards* 22:139–163 specifically examines the FFWC 1998 daily bulletin content. | Springer Nature search 2026-05-29; DOI 10.1023/A:1021169731325 and 10.1023/A:1008151023157 |

## 3. Constraint that further narrowed the action space

After v1 of the inventory was emitted, the user reported that no FFWC/BWDB inquiry path is available for this thesis (session 2026-05-29). This closed the "PENDING FFWC" pathway entirely:
- The 2022 AFR-online-absence cannot be resolved by inquiry → must be resolved by substitute corpus.
- The 1988/1998 daily-bulletin direct-citation option (physical HQ visit) cannot be resolved by appointment booking → must be resolved by peer-reviewed secondary citation.

This is the constraint v2 was built against, and it is the constraint that holds in v2.1.

## 4. Verification trail

### 4.1  FFWC portal artefacts (HTTP-verified)

| Artefact | URL | Status 2026-05-30 |
|---|---|---|
| AFR landing page | `old.ffwc.gov.bd/index.php/reports/annual-flood-reports` | 200 OK; directory of AFR 2008–2021 |
| AFR 2017 | `old.ffwc.gov.bd/images/annual17.pdf` | 200 OK; TOC inspected, Brahmaputra Basin chapter confirmed |
| AFR 2020 | `old.ffwc.gov.bd/images/annual20.pdf` | 200 OK; TOC inspected, edited by Bhuyan & Raihan, FFWC |
| AFR 2018, 2019, 2021 | `old.ffwc.gov.bd/images/annual{18,19,21}.pdf` | 200 OK assumed by directory listing; fetched and verified by user `scripts/fetch_ffwc_afrs.sh` 2026-05-29 with SHA-256 in fetch log |
| `sat_2022.pdf` | `old.ffwc.gov.bd/images/sat_2022.pdf` | 200 OK; valid PDF |
| `sat_2022_06_NE.pdf` | `old.ffwc.gov.bd/images/sat_2022_06_NE.pdf` | 200 OK; valid PDF, NE region |
| `sat_2021.pdf` | `old.ffwc.gov.bd/images/sat_2021.pdf` | 200 OK; valid PDF, national extent |
| `sat_2020.pdf` | `old.ffwc.gov.bd/images/sat_2020.pdf` | 200 OK but empty machine-text; visual inspection required |
| `sat_2017_ff.pdf` | `old.ffwc.gov.bd/images/sat_2017_ff.pdf` | **404 Not Found** (user-reported screenshot 2026-05-30) |

### 4.2  Peer-reviewed secondary citations (DOI-verified)

| Citation | Role | DOI / Identifier |
|---|---|---|
| Chowdhury MR (2000) "An assessment of flood forecasting in Bangladesh: the experience of the 1998 flood." *Nat. Hazards* 22:139–163 | 1998 bulletin-content surrogate | 10.1023/A:1008151023157 |
| Mirza MMQ (2003) "Three recent extreme floods in Bangladesh: a hydro-meteorological analysis." *Nat. Hazards* 28(1):35–64 | 1988 + 1998 hydro-meteorological context | 10.1023/A:1021169731325 |
| Brammer H (1990) "Floods in Bangladesh: geographical background to the 1987 and 1988 Floods." *Geographical Journal* 156(1):12–22 | 1988 narrative context | JSTOR 635431 |
| Tariq A. et al. (2026) Sentinel-1 + Otsu analysis of 2022 Sylhet flood | 2022 methodological precedent | 10.1080/19475705.2026.2614729 |

### 4.3  Tertiary corroboration for 2022 (no DOI needed, used as context only)

| Source | Role |
|---|---|
| Prothom Alo 2022-06-20 (republication of FFWC daily bulletin) | Specific Bahadurabad +23 cm above DL data point |
| NASA Earth Observatory image 150014 (MODIS Aqua 8 May vs 22 Jun 2022) | Before/after imagery |
| ReliefWeb FFWC organization page | Institutional reference |

## 5. Final per-event-year closure

| Year | Status | F4 inclusion | Source class |
|---|---|---|---|
| 1988 | Closed — secondary citation | Dropped | Peer-reviewed (Mirza 2003, Brammer 1990) |
| 1998 | Closed — secondary citation | **Conditional on A.5 Landsat-5 TM QC** | Peer-reviewed (Chowdhury 2000, Mirza 2003) |
| 2017 | Closed — primary (FFWC AFR) | Retained | FFWC AFR 2017 in hand |
| 2020 | Closed — primary (FFWC AFR) | Retained | FFWC AFR 2020 in hand |
| 2022 | Closed — substitute composite | Retained | FFWC `sat_2022.pdf` + peer-reviewed (Tariq 2026) + Prothom Alo bulletin republication |

No PENDING state. No HQ visit required. No inquiry pending.

## 6. Carry-over (only one)

**A.5-1998-QC:** During A.5 phase (Landsat MNDWI permanent-water mask 1988–2026), the 1998 monsoon-peak window (1998-07-03 to 1998-09-03) must be evaluated for Landsat-5 TM scene availability at the SW46.9L AOI. Decision rule:
- If ≥2 cloud-free scenes (<30% cloud, full path/row coverage of AOI) exist in that window → **retain 1998 in F4 satellite composite**.
- Otherwise → **demote 1998 to narrative-only**; F4 composite reduces to {2017, 2020, 2022}.

Decision deadline: end of A.5 phase, before A.7 opens on Day 6 of the 30-day timeline. This is a Phase-α-style decision and should be recorded in Appendix B alongside R-DATA-2.

## 7. Defensibility framing for Ch.4 §Data

The methodology paragraph proposed in inventory v2.1 §5 is the recommended boilerplate. Key defensibility points to internalise:

- **AFRs are stronger than daily bulletins** as validation references because they are post-event consolidated documents with institutional review, while daily bulletins are real-time issuance that get superseded by the AFR. Pre-empt the "did you use the primary daily bulletin?" examiner question with: "the AFR is the primary institutional record; the daily bulletin is its real-time predecessor."
- **Secondary citation for 1988/1998 is defensible** because Mirza 2003 and Chowdhury 2000 are peer-reviewed analytical sources that explicitly examine the FFWC bulletin content. A peer-reviewed analytical source is methodologically equivalent or superior to a student-photographed paper bulletin for validation purposes.
- **2022 is a moderate-magnitude event at SW46.9L**, not the catastrophic Sylhet/NE flash-flood event. Frame this as a methodological strength: it tests the satellite-flood pipeline in the regime where standing-water vs saturated-soil vs flooded-vegetation discrimination is hardest. Do not let an examiner reframe "moderate magnitude" as "weak validation."
- **1988 is dropped from F4 by satellite-availability constraint** (Sentinel-1 IW: 2014+; Landsat-5 TM coverage exists but not validated for the 1988 monsoon window in A.5). Document this in Appendix B explicitly so the design choice cannot be reopened.

## 8. Process lessons recorded against M3 (verify-before-recommend)

Two M3-class errors occurred during 6c execution. Recording them so the same failure mode does not recur in Chain B / Chain D acquisition phases:

### L1 — v1 inventory built on stale session-brief assumptions

v1 of the inventory accepted the session brief's premise that "daily flood bulletins" were the deliverable target. Five minutes of `web_fetch` on the FFWC portal *before drafting v1* would have surfaced finding F1 (daily bulletins never archived) and reframed the deliverable around AFRs from the start. Lesson: when a check involves a portal, the *first* tool call is to visit the portal, not to plan against the brief's mental model of the portal.

### L2 — v2 emitted five sat URLs without per-URL HTTP verification

v2 listed five FFWC Sentinel-1 inundation product URLs extracted from the portal *navigation listing* and propagated them into the §4 manual-fetch action item without probing each one. The 404 on `sat_2017_ff.pdf` was surfaced only when the user reported it during execution. Lesson: a navigation entry is a *claim* about availability, not availability itself. Any URL list emitted to a user must have each URL HTTP-probed in the same session. This rule binds for all subsequent BWDB/IWM/CEGIS/MoEFCC/ESGF/CDS portal interactions.

Both lessons are captured in inventory v2.1 §8 "Process lesson recorded against M3" for future-self reference.

## 9. Cross-references

- Binding spec: UG_Thesis-v1-locked-edit-2.txt §14.3 (A.7 INPUTS / DELIVERABLES); §F4 (satellite composite scope)
- Parent check: A.1 closure log `docs/A1_CLOSURE_2026-05-27.md`
- Sibling checks (still open at this closure date): 6a (CDS API registration), 6b (intake-esgf no-auth CMIP6 smoke test)
- Downstream consumer: A.7 (FFWC bulletin validation, opens Day 6); F4 (multi-event composite, dependent on A.5 phase output)
- Carry-over: A.5-1998-QC decision (records in Appendix B alongside R-DATA-2 on phase-α F4/F8)

## 10. Sign-off

Check 6c closed 2026-05-30. Three of three acceptance items met:
1. ✓ `docs/ffwc_bulletin_inventory.md` exists with per-event-year status.
2. ✓ Every status entry is one of {recoverable / using secondary citation / dropped from F4}; zero "pending FFWC" entries.
3. ✓ A.7-opening dependency cleared; no Check 6c artefact required between now and Day 6.

Next session: Check 6b (intake-esgf no-auth CMIP6 smoke test) — highest-value remaining dependency-block per session-brief priority ordering, with Check 6a (CDS registration) launched in parallel by user-side browser action.

---

*End of Check 6c closure log.*
