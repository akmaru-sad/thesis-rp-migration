# A.2 Phase-α — Structural Audit of BWDB SW46.9L Delivery

**Component:** A.2 (BWDB Q/H QC + AMS extraction), Phase-α (structural audit, pre-QC).
**Date:** 2026-05-27.
**Files audited:**
- `MDD_SW46_9L.xlsx` (684 KB; SHA: not computed)
- `WL_3hr_SW46_9L.xlsx` (1,396 KB; SHA: not computed)
**Operator:** [user] + AI supervisor.
**Session pattern:** P1 (first implementation) with M1 upstream verification on A.1.
**Decisions in force:** Q1 confirmed verbatim · Q2 accepted with (c) tightening · Q3 25 yr preferred / 20 yr hard floor.

---

## 0. Audit verdict

**Phase-α does NOT pass cleanly.** Two issues are **blocking** further work on A.2 phase-β and require written resolution before AMS extraction proceeds. Five additional findings are informational but require Ch.4 documentation and deviation-log entries. The provisional usable record length is **34 years**, comfortably above the Q3 preferred floor of 30 yr — *conditional on* the two blocking issues being resolved.

| Finding | Severity | Status |
|---|---|---|
| F1: WL datum is mMSL, not PWD | Informational | Spec correction needed |
| F2: WL is daytime 5-readings/day from 1996-04-01, daily noon before | Informational | Spec correction needed |
| F3: MDD record ends 2024-12-31, NOT 2026 | Informational | Memory phrasing correction needed |
| **F4: 275 duplicate-date pairs 1995–1999 with differing MDD values** | **BLOCKING** | **Email BWDB + provisional merge rule needed** |
| F5: 2014 gap is unified across MDD and WL (214 days, monsoon intact) | Informational | Document in Ch.4 |
| F6: 2010–2013 dry-season gaps | Informational | Document in Ch.4 |
| F7: `WATER LEVEL(m)` column in MDD file is unreliable (33% zeros) | Informational | Do not use; use WL file exclusively |
| **F8: 2001 MDD values ~2× too large (max 192,906 m³/s)** | **BLOCKING** | **Email BWDB + provisional 2001 exclusion** |
| F9: Repeated identical MDD values in Feb 2019 low-flow regime | Informational | Stage-Q interpolation artefact; document |

---

## 1. File inventory

### MDD file
- Single sheet `Worksheet`, 13,248 rows × 13 columns.
- Header metadata in rows 1–8 (BWDB letterhead, invoice number, data type, date range, frequency name).
- Column header row: index 9 (Excel row 10).
- Data block: rows 11 onwards.
- Columns: `SL, DISTRICT, UPAZILA, RIVER, STATION ID, STATION NAME, DATETIME, WATER LEVEL(m), MDD(m)3/s, LATITUDE, LONGITUDE` plus two trailing all-NaN columns.
- Unique `STATION ID`: SW46.9L (confirmed).
- Coordinates per row: 25.13028°N, 89.73464°E (matches §5 lock to 5 decimal places).
- Date format: `DD-MM-YYYY` string (e.g., `01-01-1988`).
- Discharge unit declared: `MDD(m)3/s` — interpreted as **mean daily discharge in m³/s** (m³ written as "m)3/s" is a malformed superscript on export, not an alternative unit).
- Record span declared: 1988–2026.
- Record span actual: **1988-01-01 to 2024-12-31**. (See F3.)
- Data rows after empty-row drop: 13,235.

### WL file
- Single sheet `Worksheet`, 56,441 rows × 13 columns.
- Header metadata in rows 1–9 (BWDB letterhead, station metadata).
- Column header row: index 10 (Excel row 11).
- Data block: rows 12 onwards.
- Columns: `SL, DATA TYPE, DATE TIME, WL (mMSL)` plus six trailing all-NaN columns.
- Coordinates declared: 25.13028°N, 89.73464°E (matches MDD).
- Date format: `DD-MMM-YYYY HH:MM:SS AM/PM` string (e.g., `01-JAN-1988 12:00:00 PM`).
- WL unit declared: **mMSL** (metres above mean sea level). (See F1.)
- `DATA TYPE` code values: `M` (n=35,428) and `REGULAR` (n=21,000). Interpretation: `M` = manual archival ledger, `REGULAR` = current operational record. Transition not pinned in time but value-coherent across both codes; no impact on analysis.
- Record span declared: 1988–2026.
- Record span actual: **1988-01-01 12:00 to 2026-05-01 18:00**.
- Data rows after footer drop: 56,428.

---

## 2. Findings — full detail

### F1. WL datum is mMSL, not m PWD (informational)

**Observation.** WL file column header reads `WL (mMSL)`. The locked §6 Data Inventory and the source-of-truth memory both state "daily peak stage (m PWD)". These are different vertical reference systems.

**Implication.**
- The numerical stage values cannot be substituted for PWD values without an offset. BWDB convention typically uses **PWD = MSL + 0.46 m** (approximate; spatial variability exists). The exact offset for Bahadurabad must be confirmed if any cross-comparison with published PWD-referenced figures (e.g., Mohammed 2018, FFWC bulletins) is performed.
- Internal analyses in this thesis (forensic stage–discharge scatter, R7 stage-FFA fallback) operate within a single dataset and are **invariant under a constant datum offset**. So the datum mismatch does not affect within-thesis computations.
- Ch.4 §Data must state the actual delivered datum (mMSL) and document the convention conversion if any external comparison uses PWD.

**Action.** Update §6 of `UG_Thesis-v1-locked-edit-1.txt` from "(m PWD)" to "(mMSL as delivered; PWD–MSL offset documented in Ch.4)". Update userMemories. Add Deviation Log entry **D9** (text-only correction; no methodological impact).

### F2. WL is daytime 5-readings/day from 1996-04-01; daily noon before (informational)

**Observation.** The "3 Hourly" label in the export header is a BWDB product code, not a description of the actual cadence:
- **1988-01-01 to 1996-03-31:** 1 reading/day at 12:00:00 LT.
- **1996-04-01 to 2026-05-01:** 5 readings/day at 06:00, 09:00, 12:00, 15:00, 18:00 LT (BWDB working-hours manual-observation schedule; no overnight readings).

**Implication.**
- The userMemories phrase "3-hourly WL" is loose. Strictly: **diurnal 5-readings/day daytime working-window**, not true 3-hourly throughout 24 h.
- For the §14.3 A.2 forensic stage–discharge plot (Q1 forensic framing):
  - In the **1988–1995 daily-noon era**, MDD vs noon-WL is one-to-one and unambiguous.
  - In the **1996–2026 5-readings/day era**, the daily *peak* WL is computable from the 5 readings, BUT the true diurnal peak may fall outside the observation window (e.g., overnight). For rising/falling monsoon hydrographs at a slow-rise mainstem like Bahadurabad, the diurnal range is small and the working-window max is a defensible daily-peak proxy. For rapid-event spikes (rare here), this approximation degrades.
- R7 (stage-FFA fallback) is materially affected: peak-stage AMS cannot be reconstructed from sub-daily values for years 1988–1995. If R7 ever activates, the stage AMS would use **noon-WL** for 1988–1995 (proxy for daily peak) and **max-of-5-daytime-readings** for 1996+. This regime change is itself a methodological note for Ch.4/Ch.7.

**Action.** Update §6 of `UG_Thesis-v1-locked-edit-1.txt` to "WL: 1 reading/day (12:00 LT) 1988–1996-03-31; 5 readings/day daytime (06-09-12-15-18 LT) from 1996-04-01 onward; BWDB product code 'M' and 'REGULAR'". Update userMemories accordingly. Document in Ch.4 §Data and Ch.7 §Limitations. **D10**.

### F3. MDD record ends 2024-12-31, NOT 2026 (informational)

**Observation.** The MDD file's last data row is dated 2024-12-31. There are no 2025 or 2026 MDD records. The WL file extends to 2026-05-01, but **discharge data was not generated for 2025–2026** at delivery time.

**Implication.**
- The locked §14.3 D.3 spec is **already correct**: it reads "1988–2024, 37 yr usable per delivered BWDB record; 2025–2026 excluded per delivered gap profile per Update Log 2026-05-14." No methodological change required.
- The phrasing in userMemories — "BWDB SW46.9L delivered: MDD + 3-hourly WL (m PWD) for SW46.9L and SW267, record 1988–2026" — is loose and should be tightened.
- No A.7 satellite-validation event after 2024 can be discharge-cross-validated; that does not affect the locked validation event list (1988, 1998, 2017, 2020, 2022).

**Action.** Memory edit — clarify that MDD extends 1988–2024, WL extends 1988-01 to 2026-05. **D11** (text-only).

### F4. ★ BLOCKING ★ 275 duplicate-date pairs in 1995 with differing MDD values

**Observation.** All 275 duplicate-date pairs fall in **1995 only** (1995-04-01 through 1995-12-31). The differences are systematic (typically 10–30%) and persistent across consecutive days, not random noise. Example, 1995-04-01 to 1995-04-15:

| Date | MDD value 1 (m³/s) | MDD value 2 (m³/s) | Δ (%) |
|---|---|---|---|
| 1995-04-01 | 5,250.00 | 4,084.99 | -22.2 |
| 1995-04-02 | 5,290.00 | 4,110.13 | -22.3 |
| 1995-04-05 | 5,470.00 | 4,698.66 | -14.1 |
| 1995-04-10 | 6,430.00 | 6,095.97 | -5.2 |
| 1995-04-15 | 5,880.00 | 5,101.47 | -13.2 |

`SL` numbers for the two series are sequential and interleaved (e.g., 2646 then 2647 for 1995-04-01).

**Interpretation.** This is the textbook signature of **two parallel discharge series for the same calendar days from different rating curves** — almost certainly a pre- and post-rating-revision pair retained in BWDB's archive during a known rating-curve revision window. Bahadurabad has multiple documented rating-curve revisions through the 1990s due to morphological change in the active Brahmaputra channel.

**Implication.**
- BWDB has delivered both series without provenance flags. The export collapsed two distinct rating products into one column.
- AMS extraction without resolving the merge rule produces an **arbitrary** AMS for 1995.
- The 1995 AMS falls on 1995-07-11 (87,000 m³/s under MAX merge), which lies inside the duplicate-date window. **1995 is the only directly-affected AMS year.** 1996–1999 carry no duplicate-date dependency.

**Reconciliation against Q1.** Q1 confirms the §14.3 A.2 stage–discharge diagnostic is "forensic-documentation only, not a rating-curve reopener." The duplicate-date series here are **not** a question of re-estimating a rating curve — that is forbidden. They are a question of **which delivered series to use** when BWDB provided two. This is a data-provenance question for BWDB, not a rating-estimation question. M11 is not in conflict.

**Resolution path (recommended).**
1. **Email BWDB Hydrology Directorate today** with the duplicate-date sample (1995-04-01 through 1995-04-15) and ask: "Which of the two MDD series in our delivery is the current operational record? Are the two series labelled with provenance flags that did not export?"
2. **Provisional merge rule pending BWDB reply: MAX-per-date.** Rationale: in a slow-rise monsoonal regime, rating revisions typically *correct* an under-rated curve upwards as channel geometry shifts; the higher value is the more recent, post-revision discharge. **This is operational-defensible, not theoretically justified.** A sensitivity test is required.
3. **Sensitivity test:** re-run AMS extraction under three merge rules — `max`, `min`, `mean` — and document the AMS difference per affected year. If the FFA outputs at the 100-yr return level are robust to the merge rule (Q_100 within ±5%), the choice is non-load-bearing. If not, the BWDB clarification must arrive before D.3 FFA fits.
4. **Deviation-log entry D12** to document the merge rule and the BWDB email date.

**Decision required.** Confirm (1) BWDB email goes out today; (2) provisional MAX-per-date merge rule is acceptable for phase-β to proceed; (3) sensitivity test (max/min/mean) added to A.2 deliverables.

### F5. 2014 gap is unified across MDD and WL (informational)

**Observation.** Both MDD and WL files have identical 2014 coverage: 214 days each, covering January, June, July, August, September, October, November. Missing: February through May, and December. The 2014 AMS = 61,023 m³/s on 2014-08-29 falls within the covered window. The year **passes Q2** because the JJAS window is intact (0% JJAS missing).

**Implication.**
- The gap is in BWDB's archive itself, not an export artefact. This is a unified archive disruption.
- 2014 is usable for both AMS extraction and stage–discharge forensic scatter.
- Document the 2014 gap explicitly in Ch.4 §Data.

### F6. 2010–2013 dry-season gaps (informational)

**Observation.** Days-per-year for 2010–2013: 365, 365, 366, 365 in the calendar; MDD coverage 334, 334, 335, 304. Gaps are 30, 31, 31, 61 days respectively, all in dry-season months. JJAS coverage:
- 2010: 0% JJAS missing — passes Q2a.
- 2011: 25.4% JJAS missing — **fails Q2a**.
- 2012: 0% JJAS missing — passes Q2a.
- 2013: 24.6% JJAS missing — **fails Q2a**.

**Implication.** 2011 and 2013 fail censoring and are dropped. This is consistent with Q2 acting exactly as designed.

### F7. `WATER LEVEL(m)` column in MDD file is unreliable (informational)

**Observation.** 4,408 of 13,235 MDD rows have `WATER LEVEL(m)` = 0 exactly. All 1988–1995 rows have WL=0. After 1996 the column has plausible values, but coverage is not 1-to-1 with the dedicated WL file.

**Implication.** Do not use the `WATER LEVEL(m)` column in the MDD file. **The WL file is the only valid stage source.** The forensic stage–discharge plot must merge MDD (from MDD file) with WL (from WL file) on date, not use the MDD file's internal WL column.

### F8. ★ BLOCKING ★ 2001 MDD values ~2× too large

**Observation.** The top 10 MDD values across the entire record all fall in 2001-08-02 to 2001-09-01, ranging 163,456 to 192,906 m³/s. The 1998 mega-flood peak (the documented historical reference event) was 103,129 m³/s. **2001 was not an exceptional flood year on the Brahmaputra mainstem.** The corresponding 2001 WL values (≈19.2–19.3 m) are high but **not** unprecedented — the 1998 peak stage was ~20.6 m. A WL of 19.3 m would normally correspond to a discharge of ~90,000–100,000 m³/s. The delivered 2001 MDD is **approximately 2× the value the rating curve would produce at that WL**.

**Interpretation.** This is consistent with one of the following error modes:
- **Unit-conversion error:** an erroneous × 2 applied to the 2001 series (e.g., ft³/s mistakenly retained alongside an m³/s conversion).
- **Rating-curve transcription error:** a wrong rating coefficient applied to 2001 only.
- **Index/lookup error in BWDB's archive:** 2001 records may have been overwritten with values from a different gauge or unit basis.

A simple ÷2 on the 2001 values produces 96,453 m³/s on the top day, which is physically consistent with the 1998-era peak. But **arbitrary renormalisation is forbidden without BWDB confirmation.**

**Resolution path (recommended).**
1. **Email BWDB Hydrology Directorate today** with the 2001-08-02 to 2001-09-01 anomaly. Ask: "Are the 2001 MDD values at SW46.9L in consistent units (m³/s) with the rest of the record? The 2001 daily peak of 192,906 m³/s appears physically implausible against a stage of 19.32 m."
2. **Provisional rule pending BWDB reply: EXCLUDE 2001 from the AMS series.** Mark in the per-year completeness log as `EXCLUDED_PHYS_IMPLAUSIBLE`.
3. **Decision tree on BWDB reply:**
   - If BWDB confirms unit error and supplies corrected values → reinstate 2001 with the corrected series.
   - If BWDB confirms the values stand → escalate to supervisor; consider whether 2001 represents a genuine but anomalous rating event (very unlikely — would have been historically documented).
   - If BWDB does not reply within 5 working days → 2001 stays excluded; deviation-log entry D13.

**Decision required.** Confirm (1) BWDB email goes out today; (2) 2001 is excluded from phase-β AMS extraction provisionally; (3) reinstatement path is conditional on BWDB clarification.

### F9. Repeated identical MDD values in Feb 2019 low-flow regime (informational)

**Observation.** Multiple consecutive February 2019 days carry identical MDD values: 2,752.98 m³/s repeats for 2019-02-17 to 2019-02-19; 2,774.50 m³/s repeats for 2019-02-15 + 2019-02-23 to 2019-02-25.

**Interpretation.** This is the signature of **stage-discharge interpolation during a no-observation period at a low-flow rating-curve breakpoint**: when WL falls into a narrow band where the rating function is flat or the curve was held constant, multiple days carry identical computed discharge. Standard BWDB practice for low-flow infill.

**Implication.** No effect on AMS (peaks are in monsoon, not February). Document as a low-flow data-quality note in Ch.4 §Data only.

---

## 3. Provisional AMS — Q2 censoring applied

Assumptions for this provisional AMS:
- Duplicate-date pairs in 1995–1999: **MAX-per-date merge** (pending BWDB clarification per F4).
- 2001 **excluded** (pending BWDB clarification per F8).
- Q2 (a), (b), (c) censoring applied per year.

| Year | Days in year | Days missing | JJAS missing | JJAS miss % | Q2a | Q2b | Q2c | AMS (m³/s) | Use |
|---|---|---|---|---|---|---|---|---|---|
| 1988 | 366 | 1 | 0 | 0.0 | ✓ | ✓ | ✓ | 98,300 | ✓ |
| 1989 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 70,700 | ✓ |
| 1990 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 64,300 | ✓ |
| 1991 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 84,100 | ✓ |
| 1992 | 366 | 1 | 0 | 0.0 | ✓ | ✓ | ✓ | 67,000 | ✓ |
| 1993 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 67,000 | ✓ |
| 1994 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 40,900 | ✓ |
| 1995 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 87,000 | ✓ † |
| 1996 | 366 | 100 | 7 | 5.7 | ✓ | ✓ | ✓ | 83,800 | ✓ † |
| 1997 | 365 | 63 | 0 | 0.0 | ✓ | ✓ | ✓ | 79,219 | ✓ † |
| 1998 | 365 | 6 | 0 | 0.0 | ✓ | ✓ | ✓ | 103,129 | ✓ † |
| 1999 | 365 | 79 | 0 | 0.0 | ✓ | ✓ | ✓ | 62,787 | ✓ † |
| 2000 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 60,506 | ✓ |
| 2001 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 192,906 | ✗ (F8) |
| 2002 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 41,194 | ✓ |
| 2003 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 60,712 | ✓ |
| 2004 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 72,037 | ✓ |
| 2005 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 54,997 | ✓ |
| 2006 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 45,101 | ✓ |
| 2007 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 42,749 | ✓ |
| 2008 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 70,602 | ✓ |
| 2009 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 56,274 | ✓ |
| 2010 | 365 | 31 | 0 | 0.0 | ✓ | ✓ | ✓ | 54,096 | ✓ |
| **2011** | 365 | 31 | 31 | **25.4** | **✗** | — | — | 35,815 | ✗ (Q2a) |
| 2012 | 366 | 31 | 0 | 0.0 | ✓ | ✓ | ✓ | 55,933 | ✓ |
| **2013** | 365 | 61 | 30 | **24.6** | **✗** | — | — | 59,276 | ✗ (Q2a) |
| 2014 | 365 | 151 | 0 | 0.0 | ✓ | ✓ | ✓ | 61,023 | ✓ |
| 2015 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 66,292 | ✓ |
| 2016 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 73,227 | ✓ |
| 2017 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 63,078 | ✓ |
| 2018 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 46,243 | ✓ |
| 2019 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 50,828 | ✓ |
| 2020 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 67,869 | ✓ |
| 2021 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 55,667 | ✓ |
| 2022 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 56,883 | ✓ |
| 2023 | 365 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 46,311 | ✓ |
| 2024 | 366 | 0 | 0 | 0.0 | ✓ | ✓ | ✓ | 59,559 | ✓ |

† = duplicate-date dependency in 1995 only; AMS shown reflects provisional MAX-per-date merge per F4. 1996–1999 AMS values do not depend on the merge rule.

**Summary:**
- Total calendar years 1988–2024: **37**.
- Years failing Q2: **2** (2011, 2013).
- Years excluded for physical implausibility (F8): **1** (2001).
- Years affected by duplicate-date provenance (F4): **1** (1995 only — 275 duplicate dates spanning 1995-04-01 to 1995-12-31).
- **Provisional usable AMS years: 34.**
- **Q3 status: PASS preferred floor (≥30 yr).**
- **Months of AMS peaks across 34 years: Jun=3, Jul=19, Aug=7, Sep=7.** Distribution is physically coherent with monsoonal regime.

**Sanity check vs documented Brahmaputra mainstem floods:**

| Year | Provisional AMS (m³/s) | Literature reference | Match? |
|---|---|---|---|
| 1988 | 98,300 | Mirza 2003 mega-flood | ✓ Excellent |
| 1998 | 103,129 | Islam 2010 longest-duration mega-flood, peak ~103,000 | ✓ Excellent |
| 2017 | 63,078 | Major monsoon flood | ✓ Plausible |
| 2020 | 67,869 | Major monsoon flood | ✓ Plausible |
| 2022 | 56,883 | Lower magnitude than 2020 at Bahadurabad | ✓ Consistent |

The record's physical credibility is **high**, conditional on F4 and F8 resolutions.

---

## 4. Phase-α acceptance gate

Proposed gate from A.1 closure log (subject to in-session refinement):

| Item | Status |
|---|---|
| All 7 audit items resolved in writing | **5 of 7 resolved; F4 and F8 pending BWDB clarification** |
| Provisional post-censoring record length ≥ Q3 hard floor (20 yr) | ✓ 34 yr ≥ 20 yr |
| Provisional post-censoring record length ≥ Q3 preferred floor (30 yr) | ✓ 34 yr ≥ 30 yr |
| No silent unit inconsistencies | ✓ MDD m³/s confirmed; WL mMSL confirmed and flagged |

**Gate verdict: CONDITIONAL PASS.** Phase-α audit is structurally complete, but the two blocking findings (F4, F8) must be resolved via the BWDB email pathway before phase-β AMS extraction is finalised. Phase-β can begin in parallel with the BWDB email under the provisional rules (MAX-merge for F4; exclude 2001 for F8) on the explicit understanding that:
- The final AMS series may revise the 1995 value and may reinstate 2001.
- A merge-rule sensitivity test (max/min/mean) is added to phase-β deliverables.
- The 1995 and 2001 entries in the phase-β AMS CSV carry a `provenance_flag` column noting "PROVISIONAL pending BWDB clarification."

---

## 5. Decisions required before phase-β opens

1. **BWDB email** — supervisor confirms the email goes out today (2026-05-27) with the F4 and F8 sample tables. Both anomalies in one email to preserve goodwill.
2. **Provisional merge rule for F4** — confirm MAX-per-date as the operational default. Confirm sensitivity test (max/min/mean) is added to phase-β deliverables.
3. **Provisional 2001 exclusion for F8** — confirm 2001 stays excluded until BWDB replies.
4. **Spec text corrections (text-only deviations D9, D10, D11)** — confirm these go into `UG_Thesis-v1-locked-edit-1.txt` and userMemories.
5. **Phase-β directory** — confirm `code/chain_a_satellite/a2_bwdb_qc/` per §14.6, or new sub-tree.
6. **Phase-β scope confirmation** — apply Q2 censoring + duplicate-date merge + 2001 exclusion → emit final AMS CSV + per-year completeness CSV + forensic stage–discharge PDF.

---

## 6. Phase-α deliverables emitted this session

- `results/baseline/A2_phase_alpha_audit.md` (this document)
- `results/baseline/A2_phase_alpha_per_year_summary.csv` (companion table; emitted next)

Phase-β deliverables (next session, conditional on §5 decisions):
- `results/baseline/A2_ams_sw46p9l_1988-2024.csv`
- `results/baseline/A2_per_year_completeness.csv`
- `results/baseline/A2_stage_discharge_forensic.pdf`
- `results/baseline/A2_duplicate_merge_sensitivity.csv` (NEW — added for F4)
- `results/baseline/A2_bwdb_qc_report.md`
- `code/chain_a_satellite/a2_bwdb_qc/a2_bwdb_qc.py`
- `code/chain_a_satellite/a2_bwdb_qc/verify_a2_phase_beta.py`

---

## 7. Memory edits required

Two updates to userMemories:
- Replace "MDD + 3-hourly WL (m PWD) for SW46.9L and SW267, record 1988–2026 in Excel" with "MDD (1988–2024 daily, m³/s) and WL (1988–2026-05 in mMSL; 1 reading/day noon 1988-Q1 1996, 5 readings/day daytime 1996-Q2 onward) for SW46.9L delivered as two separate Excel files."
- Add to Approach & patterns or Key learnings: "BWDB 'frequency name' export label is a product code, not an actual cadence statement; verify temporal structure from the data itself."

---

*Phase-α complete (conditional). Awaiting six decisions in §5 before phase-β code is written.*
