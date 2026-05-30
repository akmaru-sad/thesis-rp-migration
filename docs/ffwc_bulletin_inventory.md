# FFWC Bulletin Inventory for A.7 Validation

**Document ID:** docs/ffwc_bulletin_inventory.md
**Thesis binding spec:** UG_Thesis-v1-locked-edit-2 (2026-05-27)
**Component:** A.7 — FFWC bulletin validation on 1988, 1998, 2017, 2020, 2022 events at SW46.9L Bahadurabad Transit
**F4 dependency:** Multi-event flood-extent composite (1998 + 2017 + 2020 + 2022)
**Author / status:** Compiled 2026-05-29; pre-A.7-opening (Day 6) inventory closure
**Pre-session check:** Check 6c (carried-forward dependency block from A.1 closure 2026-05-27)

---

## 1. Executive summary

Three facts emerged from the 2026-05-29 portal audit that change the design assumption stated in the session brief:

1. **The FFWC daily flood bulletin is not systematically archived online for any year.** The legacy portal (`old.ffwc.gov.bd`) overwrites the live bulletin PDF (`ffb.pdf`, `fsumm.pdf`) on each issuance cycle; no per-date archive exists. The new portal (`ffwc.bwdb.gov.bd`) advertises "historical data" but exposes it via API for water-level time series, not as bulletin PDFs. **Daily bulletins for every historical year — 2017 and 2020 included — are paper-only or per-day Wayback snapshots.**

2. **What IS systematically archived online is the Annual Flood Report (AFR).** Legacy portal hosts AFR 2008–2021 as direct PDFs. AFRs are post-event consolidated narrative documents with event chronologies, peak water-level tables, station-by-station flood-day counts, and forecaster commentary — i.e. they contain the validation content A.7 actually needs, and are arguably the more rigorous citation than daily real-time bulletins (which get superseded by AFRs).

3. **For 1988 and 1998, peer-reviewed secondary sources documenting the FFWC bulletin content already exist** (Chowdhury 2000 *Natural Hazards*; Mirza 2003; Hofer & Messerli 2006; Islam & Chowdhury 1999). A direct paper-archive visit to FFWC HQ remains the gold standard for 1988/1998 but is not strictly required if A.7's role is satellite-validation context rather than independent flood-event reconstruction.

**Operational consequence.** The session brief framed A.7 around "year-by-year recoverability of FFWC daily flood-bulletin PDFs." That framing was based on a stale assumption. The recoverability question is now reframed as: *for each of the five A.7 validation years, what is the best available FFWC-derived flood-event reference document?* The matrix in §3 answers this.

**Status against acceptance criterion:** Acceptance is "docs/ffwc_bulletin_inventory.md exists with per-event-year status (recoverable / pending FFWC / using secondary citation / dropped from F4)." This document satisfies that, with an additional column documenting the AFR-vs-daily distinction.

---

## 2. Source-portal audit (verified 2026-05-29)

| Portal | URL | Function | Bulletin archive? | AFR archive? |
|---|---|---|---|---|
| Legacy FFWC | http://old.ffwc.gov.bd/ | Real-time WL ticker; current-day bulletin links overwrite daily | None (live PDF only) | **Yes: 2008–2021 as direct PDFs at `/images/annual{YY}.pdf`** |
| New FFWC (API) | https://ffwc.bwdb.gov.bd/ | API for current + historical WL; robots-blocked from automated scraping | Implied via API; no PDF archive visible | Not visible on landing page |
| FFWC Flash-Flood | http://old.ffwc.gov.bd/flashflood/ | Flash-flood bulletin (current day overwrite) | None | N/A |
| Library of Congress Web Archives | https://www.loc.gov/item/lcwaN0044257/ | Periodic snapshots of ffwc.gov.bd | Possible per-snapshot capture of daily bulletins; full access restricted to LoC reading rooms | Limited |
| Internet Archive Wayback | https://web.archive.org/ | Periodic public crawl of ffwc.gov.bd | Possible per-snapshot capture; coverage gaps before ~2014 are heavy | Limited |
| WAPDA Bhaban (BWDB/FFWC HQ, 8th floor) | Physical, Dhaka | Master paper archive of daily bulletins | **All years, paper** | All years, paper |

**Authoritative AFR list (legacy portal, verified 2026-05-29):** 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021. **No AFR online for 2022, 2023, 2024, 2025 as of 2026-05-29** — AFRs run 12–24 months behind the flood year; 2022 AFR may exist on internal servers but is not yet published online.

---

## 3. Per-event-year status matrix

| Event year | Online AFR? | Daily bulletin online? | Primary recoverable source (preferred) | Secondary citation (fallback) | A.7 status | F4 inclusion |
|---|---|---|---|---|---|---|
| **1988** | No (pre-2008 archive) | No | FFWC HQ paper archive (physical visit required) | Mirza 2003 *Climatic Change*; Hofer & Messerli 2006 *Floods in Bangladesh* | **Secondary citation primary; HQ visit optional** | **Dropped from F4** (Sentinel-1 not available 1988; Landsat-5 TM partial scenes only; satellite-extent reconstruction unreliable). FFWC narrative retained for Ch.4 historical-context paragraph only. |
| **1998** | No (pre-2008 archive) | No | FFWC HQ paper archive (physical visit required) | **Chowdhury 2000 *Natural Hazards* 22:139–163** (peer-reviewed analytical paper that explicitly examines the FFWC 1998 daily bulletins, forecasting procedure, three-river peak synchronisation); Islam & Chowdhury 1999 | **Secondary citation primary; HQ visit recommended (one morning) for direct citation of bulletin text** | **Retained in F4** if Landsat-5 TM coverage acceptable for peak-event dates (verify in A.5 phase); else demoted to narrative-only |
| **2017** | **Yes — AFR 2017 at `old.ffwc.gov.bd/images/annual17.pdf`** | No | **AFR 2017 (online PDF, recoverable now)** | None needed | **RECOVERABLE NOW** | **Retained in F4** (Sentinel-1 IW available 2014+; AFR provides event chronology and peak WL for cross-reference) |
| **2020** | **Yes — AFR 2020 at `old.ffwc.gov.bd/images/annual20.pdf`** | No | **AFR 2020 (online PDF, recoverable now)** | None needed | **RECOVERABLE NOW** | **Retained in F4** (Sentinel-1 + Landsat-8/9 available; AFR provides event chronology) |
| **2022** | No (2022 AFR not yet published online as of 2026-05-29) | No | **PENDING FFWC** — inquire whether AFR 2022 is internally available; physical visit may suffice | AFR 2021 referenced as adjacent-year context; CEGIS 2022 monsoon flood reports; ReliefWeb situation reports | **PENDING (inquiry needed Day 2–3)** | **Retained in F4** (event is well-documented in satellite record regardless of AFR availability; AFR is corroborative not constitutive) |

### Status codes (per acceptance criterion)

- **Recoverable now (online):** 2017, 2020
- **Recoverable via secondary citation (peer-reviewed):** 1988, 1998
- **Pending FFWC inquiry:** 2022 (AFR online absence; check physical/internal availability)
- **Dropped from F4 (satellite composite):** 1988 (kept for narrative context only)

---

## 4. Recommended action sequence (low-cost-first)

### Step 1 — Immediate (today, 30 min): Download the four online AFRs

The 2017 and 2020 AFRs are the only directly required online documents. Pulling adjacent years (2018, 2019, 2021) is cheap context insurance for cross-checking event chronologies. Use the bundled helper script `scripts/fetch_ffwc_afrs.sh` (see §5).

Acceptance: `data/ffwc/AFR_2017.pdf`, `AFR_2018.pdf`, `AFR_2019.pdf`, `AFR_2020.pdf`, `AFR_2021.pdf` exist locally with non-zero size and SHA-256 logged.

### Step 2 — Within 2–3 days: Phone/email inquiry to FFWC for 2022 AFR

Direct contact path (verified 2026-05-29):
- **Email:** ffwcbwdb@gmail.com, ffwc05@yahoo.com
- **Phone:** +880-2-9553118, +880-2-9550755
- **Fax:** +880-2-9557386
- **Postal/physical:** WAPDA Building, 8th Floor, Motijheel Commercial Area, Dhaka

Inquiry script (email template in §6). The 2022 AFR is the only material online-gap item; secondary corroboration (CEGIS, ReliefWeb, peer-reviewed papers on the 2022 north-east flash flood event at Bahadurabad/Sunamganj) is sufficient if the AFR is unavailable.

### Step 3 — Within 2–3 days (if planning HQ visit): Physical visit to WAPDA Bhaban

Only if you choose to obtain primary-source citations for 1988 and 1998 daily bulletins. Half-day budget. Bring: ID, written request letter (FFWC requires a formal request slip for paper-archive access), USB drive, phone-camera. Specifically request: daily flood bulletins for Bahadurabad station SW46.9L for the periods 15-July to 15-September 1988 and 15-July to 15-September 1998. **Verify in advance by phone that the archivist is available; the 8th floor is not staffed daily.**

This visit is **defensible-to-skip** if you are willing to rely on Chowdhury 2000 and Mirza 2003 as secondary citations, which is the more time-economical and equally defensible choice for an undergraduate thesis. The peer-reviewed secondary citation is arguably MORE rigorous than a paper bulletin photographed by the student, in examiner terms.

### Step 4 — Pre-A.7-opening (Day 5): Final F4 composite decision

Before A.7 opens on Day 6, decide and document in Appendix B:

- F4 composite years: **{1998 (if Landsat-5 TM OK), 2017, 2020, 2022}** = 4 events expected; **{2017, 2020, 2022}** = 3 events minimum acceptable
- 1988 is dropped from F4 satellite composite regardless of FFWC bulletin availability — the limiting factor is satellite imagery, not bulletin recoverability. Document this explicitly so it cannot be reopened.

---

## 5. Download helper script

`scripts/fetch_ffwc_afrs.sh` (bundled with this deliverable) — bash one-shot to fetch AFR 2017–2021 to `data/ffwc/`, with retry, SHA-256 logging, and verification of non-zero PDF magic bytes.

---

## 6. Inquiry email template (Step 2)

```
To: ffwcbwdb@gmail.com; ffwc05@yahoo.com
Subject: Annual Flood Report 2022 — availability inquiry (undergraduate research)

Dear FFWC,

I am an undergraduate Environmental Engineering thesis student conducting research on
flood-hazard return-period migration at Bahadurabad station SW46.9L on the Jamuna river,
under CMIP6 climate scenarios. My methodology requires cross-referencing Annual Flood
Reports (AFR) for the 1988, 1998, 2017, 2020 and 2022 flood events.

I have been able to access AFR 2017 and AFR 2020 directly from the FFWC website at
http://old.ffwc.gov.bd/index.php/reports/annual-flood-reports. However, AFR 2022 does
not appear to be published online as of today.

Could you please advise whether:
  (1) AFR 2022 is available in any internal or in-print form that can be released to
      a student researcher; and
  (2) Whether a brief physical-archive consultation appointment can be arranged for
      daily flood bulletin records for the 1988 and 1998 monsoon seasons at Bahadurabad
      station SW46.9L.

I have a written request letter ready on request and can present my student ID and
supervisor's letter at the WAPDA Bhaban office.

Thank you for your time.

Sincerely,
[Name]
[Student ID]
[Department], [University]
[Email]  [Phone]
```

Send a copy CC to your supervisor's institutional email so the request is on file.

---

## 7. Defensibility note for Ch.4 §Data

When A.7 is written up, the methodology section must explicitly state:

> "FFWC flood-event documentation for the validation years 2017 and 2020 was obtained from the FFWC Annual Flood Reports (FFWC 2018, 2021), publicly downloadable from http://old.ffwc.gov.bd/index.php/reports/annual-flood-reports. For the 2022 north-east monsoon flash-flood event the AFR was not yet publicly released as of 2026-05-29; corroborative documentation was drawn from [CEGIS 2022 / ReliefWeb / peer-reviewed paper] and is treated as secondary support to the primary Sentinel-1 SAR + Landsat MNDWI satellite record. For the 1988 and 1998 historical events, daily FFWC bulletin content was drawn from peer-reviewed analytical sources (Chowdhury 2000; Mirza 2003) rather than the primary paper archive at FFWC HQ, on the grounds that A.7's role for these years is satellite-context narrative and the 1988 event predates the Sentinel-1 IW record (2014+) such that no satellite-flood-extent composite is constructed for 1988."

This pre-empts the examiner question "did you go to FFWC HQ?" with a defensible scope rationale rather than an evasion.

---

## 8. Open items / risks

- **R-FFWC-1:** If FFWC does not respond within 5 working days of the Step 2 email, escalate via supervisor's institutional contact at IWFM or BWDB.
- **R-FFWC-2:** If the 2022 AFR is unavailable in any form, log the substitution in Appendix B and proceed with secondary corroborative sources. This is not a rollback trigger for the locked design.
- **R-FFWC-3:** If a physical visit reveals that the 1988 or 1998 bulletins are partially missing (paper deterioration, archive culling), the secondary citation path is preserved as primary and the visit becomes confirmatory only. No methodological retreat is needed.

**None of R-FFWC-1/2/3 blocks A.7 opening on Day 6.** A.7 can open with whatever subset of {2017 AFR, 2020 AFR, 2022 substitute, 1988/1998 secondary} is in hand by Day 5.

---

*End of FFWC bulletin inventory.*
