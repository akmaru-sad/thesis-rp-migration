# FFWC Bulletin Inventory for A.7 Validation — v2.1 (CLOSEOUT, URL-verified)

**Document ID:** docs/ffwc_bulletin_inventory.md
**Version:** v2.1 — closeout state, no-inquiry workaround, FFWC sat-URL availability verified
**Supersedes:** v2 (2026-05-29, sat URLs listed from portal nav without HTTP verification); v1 (2026-05-29, contained PENDING items requiring FFWC inquiry)
**Thesis binding spec:** UG_Thesis-v1-locked-edit-2 (2026-05-27)
**Component:** A.7 — FFWC bulletin validation on 1988, 1998, 2017, 2020, 2022 events at SW46.9L Bahadurabad Transit
**F4 dependency:** Multi-event flood-extent composite (1998 + 2017 + 2020 + 2022)
**Author / status:** Closed 2026-05-29; URL-verified patch 2026-05-30
**Pre-session check 6c:** CLOSED

### Changelog v2 → v2.1 (2026-05-30)

Triggered by user-reported 404 on `sat_2017_ff.pdf`. v2 had listed five FFWC Sentinel-1 inundation-map URLs extracted from the portal navigation listing without per-URL HTTP verification — an M3 (verify-before-recommend) failure. Each URL probed individually 2026-05-30:

| URL | v2 assumption | v2.1 verified status |
|---|---|---|
| `sat_2022.pdf` | available | **200 OK** — valid PDF, national extent |
| `sat_2022_06_NE.pdf` | available | **200 OK** — valid PDF, NE region |
| `sat_2021.pdf` | available | **200 OK** — valid PDF, national extent |
| `sat_2020.pdf` | available | **200 OK** but **machine-readable text empty** — likely vector-rendered map, requires visual browser inspection to confirm cartographic content |
| `sat_2017_ff.pdf` | available | **404 Not Found** — dead nav link; file removed from server while portal navigation template retained |

Patches applied:
- §4 manual-fetch list reduced from 5 URLs to 4 URLs (`sat_2017_ff.pdf` removed).
- §3.5 (2022 substitute composite) — no change; this URL did not appear in §3.5 table.
- §3.3 (2017) — clarifying note added: the FFWC `sat_2017_ff.pdf` product (when it existed) covered the *pre-monsoon haor/Sylhet flash flood of March–April 2017*, geographically distinct from the 2017 monsoon Jamuna event at SW46.9L. AFR 2017 remains the sole and sufficient primary source for 2017 A.7 validation.
- §4 — `sat_2020.pdf` annotated to require visual browser inspection due to empty machine-readable text stream.
- New §8 added: FFWC sat-URL audit table (consolidated reference).

No per-event-year status changes. Acceptance criterion satisfaction unchanged. Check 6c remains CLOSED.

---

## 1. Closeout summary

Inquiry path to FFWC/BWDB is unavailable for this thesis. All five A.7 validation
years must be closed using publicly recoverable artefacts plus peer-reviewed
secondary citations. As of 2026-05-29 this is achievable for every year. No
PENDING state remains.

**Verified-recoverable primary sources, all five years:**

| Year | Primary source | Recoverable as |
|---|---|---|
| 1988 | Mirza 2003 *Nat. Hazards* 28(1):35–64; Brammer 1990 *Geographical Journal* 156:12–22 | DOI-indexed peer-reviewed papers, university library / ResearchGate |
| 1998 | Chowdhury 2000 *Nat. Hazards* 22:139–163; Mirza 2003 *Nat. Hazards* 28(1):35–64 | DOI-indexed peer-reviewed papers, university library / ResearchGate |
| 2017 | FFWC Annual Flood Report 2017 (downloaded 2026-05-29) | `data/ffwc/AFR_2017.pdf` |
| 2020 | FFWC Annual Flood Report 2020 (downloaded 2026-05-29) | `data/ffwc/AFR_2020.pdf` |
| 2022 | FFWC Sentinel-1 inundation map `sat_2022.pdf` + peer-reviewed papers on 2022 NE event + ReliefWeb/NASA Earth Observatory | URLs in §3.5 |

**F4 satellite-extent composite final scope:** {2017, 2020, 2022} confirmed. 1998 promoted from "if Landsat-5 TM OK" to **confirmed in F4** if Landsat-5 TM coverage of monsoon dates passes A.5 phase QC (see §3.2). 1988 dropped from F4 per V1 satellite-availability constraint.

---

## 2. Empirical findings closed since v1

| Finding | v1 status | v2 status | Source |
|---|---|---|---|
| Daily flood bulletin online archive | Assumed available 2017+ | **Confirmed not archived for any year** | Direct portal audit `old.ffwc.gov.bd/images/ffb.pdf` (overwrite-daily PDF) |
| FFWC Annual Flood Reports online | Unknown coverage | **Confirmed 2008–2021** | `old.ffwc.gov.bd/index.php/reports/annual-flood-reports` directory listing |
| AFR 2017/2020 content scope | Assumed | **Confirmed Brahmaputra basin coverage incl. monthly rainfall + river situation chapters** | Direct PDF TOC inspection 2026-05-29 |
| AFR 2022 availability | Unknown | **Confirmed not online; not yet published as of 2026-05-29** | Portal directory absence |
| 2022 Bahadurabad event severity | Unknown | **Confirmed moderate-magnitude event: Jamuna at Bahadurabad +23 cm above DL during June 2022 monsoon** | FFWC bulletin via Prothom Alo 2022-06-20 |
| FFWC Sentinel-1 inundation products | Not catalogued | **Confirmed published for 2017 FF, 2020, 2021, 2022, 2022 NE** | `old.ffwc.gov.bd/images/sat_*.pdf` |
| Chowdhury 2000 access | Cited but unverified | **DOI 10.1023/A:1008151023157 confirmed; Springer-indexed; cited by 2025 Springer paper** | Springer Nature; ResearchGate |
| Mirza 2003 access | Cited but unverified | **Three Recent Extreme Floods in Bangladesh: A Hydro-Meteorological Analysis** covers 1987+1988+1998 in single paper; Nat. Hazards 28(1):35–64; DOI 10.1023/A:1021169731325 | Springer Nature |

---

## 3. Per-event-year final closure

### 3.1  1988 — secondary citation, dropped from F4

- **Primary citation:** Mirza MMQ (2003) "Three recent extreme floods in Bangladesh: a hydro-meteorological analysis." *Nat. Hazards* 28(1):35–64. DOI: 10.1023/A:1021169731325.
- **Supporting citation:** Brammer H (1990) "Floods in Bangladesh: geographical background to the 1987 and 1988 Floods." *Geographical Journal* 156(1):12–22.
- **Tertiary context:** Hofer & Messerli (2006) *Floods in Bangladesh* (Brown Walker / UNU Press monograph) — useful for narrative chapter context.
- **A.7 role:** Narrative-context only for Ch.4 §Historical-Floods paragraph. No satellite-extent reconstruction (Sentinel-1 first IW launch 2014; Landsat-5 TM 1984–2013 coverage exists but radiometric/geometric quality at 1988 monsoon dates not validated by your A.5 pipeline against this remote-sensing record).
- **F4 inclusion:** **No.**
- **Defensibility framing:** "The 1988 event predates the Sentinel-1 IW record and therefore cannot enter the F4 SAR-Landsat satellite composite. FFWC documentation for 1988 is drawn from the peer-reviewed hydro-meteorological analysis of Mirza (2003), which explicitly compares the 1987, 1988 and 1998 floods on magnitude, extent, depth and duration metrics."

### 3.2  1998 — secondary citation, conditional F4 inclusion

- **Primary citation:** Chowdhury MR (2000) "An assessment of flood forecasting in Bangladesh: the experience of the 1998 flood." *Nat. Hazards* 22:139–163. DOI: 10.1023/A:1008151023157.
- **Supporting citation:** Mirza MMQ (2003) *Nat. Hazards* 28(1):35–64 (as above).
- **A.7 role:** Bulletin-content surrogate. Chowdhury 2000 explicitly examines the FFWC 1998 daily bulletins, the forecasting procedure, three-river peak synchronisation, and bulletin adequacy — exactly the validation content A.7 needs.
- **F4 inclusion:** **Conditional on Landsat-5 TM scene-availability passing A.5 phase QC.** If usable Landsat-5 scenes exist for the 1998 monsoon peak window (Jul-3 to Sep-3, 1998) with <30% cloud cover and adequate path/row coverage at the SW46.9L AOI, retain 1998 in F4 composite. If not, demote to narrative-only.
- **Decision deadline:** End of A.5 phase, before A.7 opens on Day 6.
- **Defensibility framing:** "FFWC documentation for the 1998 event is drawn from Chowdhury (2000), a peer-reviewed analytical paper that explicitly examines the FFWC daily bulletin content, forecasting procedure, and three-river peak synchronisation during the most prolonged flood in Bangladesh's recorded history. The use of a peer-reviewed analytical source rather than the primary paper bulletin archive is methodologically equivalent or superior for the validation context A.7 requires."

### 3.3  2017 — FFWC AFR direct, F4 confirmed

- **Primary source:** FFWC Annual Flood Report 2017. Editor: FFWC Processing and Flood Forecasting Circle. Local path: `data/ffwc/AFR_2017.pdf`. Verified URL: `http://old.ffwc.gov.bd/images/annual17.pdf`.
- **Content scope (verified):** Chapter 2 monthly rainfall (March–October 2017), Chapter 3 River Situation including The Brahmaputra Basin, peak WL tables for major stations.
- **Specific 2017 Jamuna context:** Two distinct flood peaks (1st week July, 2nd week August), second peak more severe; ~42% of country inundated; matches Sentinel-1 IW availability (Sentinel-1A launched 2014, 1B 2016).
- **Note on FFWC `sat_2017_ff.pdf`:** The FFWC portal navigation references a "Sentinel-1 Satellite Based Inundation (2017 Flash Flood)" product at `old.ffwc.gov.bd/images/sat_2017_ff.pdf`. **The file returns 404 as of 2026-05-30** — the navigation entry remained in the portal template after the file was removed from the server. Independent of availability, this product documented the **pre-monsoon haor/Sylhet flash flood of March–April 2017** (a distinct hydrological event that affected Sunamganj/Habiganj/Moulvibazar boro rice production), not the 2017 monsoon Brahmaputra/Jamuna event at SW46.9L. AFR 2017 is therefore the sole and sufficient primary source for 2017 A.7 validation at this station.
- **F4 inclusion:** **Yes — primary anchor event.**
- **Citation form:** FFWC (2018). *Annual Flood Report 2017*. Flood Forecasting and Warning Centre, Bangladesh Water Development Board, Dhaka. Available: http://old.ffwc.gov.bd/images/annual17.pdf [accessed 2026-05-29].

### 3.4  2020 — FFWC AFR direct, F4 confirmed

- **Primary source:** FFWC Annual Flood Report 2020. Editors: Md. Arifuzzaman Bhuyan (Executive Engineer) and Sarder Udoy Raihan (Sub-Divisional Engineer), FFWC, BWDB. Local path: `data/ffwc/AFR_2020.pdf`. Verified URL: `http://old.ffwc.gov.bd/images/annual20.pdf`.
- **Content scope (verified):** Chapter 1 Introduction (physical setting, river system, FFWC activities, operational stages, nature/causes/statistics of flooding), Chapter 2 Rainfall Situation (monthly March–October 2020), Chapter 3 River Situation opening with Brahmaputra Basin.
- **F4 inclusion:** **Yes — primary anchor event.** Strong satellite coverage from Sentinel-1A/1B + Landsat 8/9.
- **Citation form:** FFWC (2021). *Annual Flood Report 2020*. Editors: M.A. Bhuyan and S.U. Raihan. Flood Forecasting and Warning Centre, Bangladesh Water Development Board, Pani Bhaban, Dhaka-1205. Available: http://old.ffwc.gov.bd/images/annual20.pdf [accessed 2026-05-29].

### 3.5  2022 — substitute composite, F4 retained

AFR 2022 not yet published online. Substitute corpus (all publicly recoverable, no FFWC inquiry needed):

| Source | Type | Role | URL / DOI |
|---|---|---|---|
| FFWC Sentinel-1 Satellite Inundation 2022 (national) | Institutional satellite product | Direct FFWC artefact for 2022; cross-reference for A.5 SAR-Otsu pipeline | http://old.ffwc.gov.bd/images/sat_2022.pdf |
| FFWC Sentinel-1 Satellite Inundation 2022 Monsoon NE | Institutional satellite product | NE region detail (less relevant for SW46.9L but complete record) | http://old.ffwc.gov.bd/images/sat_2022_06_NE.pdf |
| Tariq et al. 2026 *Geomatics, Natural Hazards and Risk* | Peer-reviewed Sentinel-1 + Otsu | Methodologically aligned; precedent for your pipeline | DOI: 10.1080/19475705.2026.2614729 |
| Rahman et al. 2024 *MethodsX* / ScienceDirect | Peer-reviewed S1 GEE assessment | NE flood damage assessment | ScienceDirect: pii/S2590061724000929 |
| Tahmid et al. 2024 *Modeling Earth Systems and Environment* | Peer-reviewed Sentinel-1 GEE | Sylhet + Sunamganj composite | ADS: 2024MCarS..12...47T |
| Prothom Alo 2022-06-20 | Journalism (FFWC bulletin quoted) | **Specific Bahadurabad +23 cm above DL data point** | en.prothomalo.com (search: "Flood situation worsens further") |
| NASA Earth Observatory 2022-06-22 | Institutional remote-sensing | MODIS Aqua false-colour before/after imagery | earthobservatory.nasa.gov/images/150014 |
| Wikipedia "2022 India–Bangladesh floods" | Encyclopaedic context | Context only, do not cite as primary | en.wikipedia.org/wiki/2022_India%E2%80%93Bangladesh_floods |

- **F4 inclusion:** **Yes — primary anchor event.** Sentinel-1, Landsat 8/9, MODIS all available.
- **Critical defensibility point:** The 2022 event at SW46.9L was *moderate magnitude* (~23 cm above DL), not catastrophic. The headline 2022 Bangladesh flood was the Sylhet/NE flash-flood event on the Surma-Kushiyara, geographically distinct from your study station. **A.7 must explicitly frame 2022 as a moderate-magnitude test case** — this is a methodological strength (tests SAR-Otsu and Landsat-MNDWI in the regime where water/saturated-soil/flooded-vegetation discrimination is hardest) and not a weakness.
- **Citation form:** FFWC (2022). *Sentinel-1 Satellite-Based Inundation Map 2022*. Flood Forecasting and Warning Centre, BWDB, Dhaka. Available: http://old.ffwc.gov.bd/images/sat_2022.pdf. Supplemented by Tariq et al. (2026) DOI: 10.1080/19475705.2026.2614729 and event-window FFWC daily-bulletin quotations republished in Prothom Alo (2022-06-20).

---

## 4. Files in `data/ffwc/` (local)

After running `scripts/fetch_ffwc_afrs.sh data/ffwc`:

```
data/ffwc/
├── AFR_2017.pdf            # PRIMARY — 2017 event
├── AFR_2018.pdf            # context
├── AFR_2019.pdf            # context
├── AFR_2020.pdf            # PRIMARY — 2020 event
├── AFR_2021.pdf            # context (closest to 2022 narrative)
└── fetch_log_*.txt         # provenance log with SHA-256 of each PDF
```

Additionally to fetch manually in browser (single-click each, no script needed; all URLs HTTP-verified 2026-05-30):
- `http://old.ffwc.gov.bd/images/sat_2022.pdf` → `data/ffwc/sat_2022.pdf` — **DIRECT** for 2022 Jamuna event; valid PDF, national-extent Sentinel-1 inundation
- `http://old.ffwc.gov.bd/images/sat_2022_06_NE.pdf` → `data/ffwc/sat_2022_06_NE.pdf` — context (NE region only)
- `http://old.ffwc.gov.bd/images/sat_2021.pdf` → `data/ffwc/sat_2021.pdf` — context; valid PDF, national extent
- `http://old.ffwc.gov.bd/images/sat_2020.pdf` → `data/ffwc/sat_2020.pdf` — **DIRECT** for 2020 monsoon event; PDF returns 200 OK but has empty machine-readable text stream (likely vector-only cartographic content). **Open in browser to visually confirm the map renders before relying on it** — if blank or corrupted, treat as missing and rely on AFR 2020 narrative tables alone.

**Removed from list (was in v2):** `http://old.ffwc.gov.bd/images/sat_2017_ff.pdf` — confirmed 404 on 2026-05-30; the underlying flash-flood event is geographically distinct from SW46.9L (see §3.3 note).

For peer-reviewed papers — Chowdhury 2000, Mirza 2003, Brammer 1990, Tariq et al. 2026 — use university library SSO (most likely available via Springer Nature subscription) or send ResearchGate request to the corresponding author. Save to `data/literature/` not `data/ffwc/`.

---

## 5. Ch.4 §Data — recommended methodology paragraph

> "FFWC flood-event documentation for the validation years 2017 and 2020 was obtained from the FFWC Annual Flood Reports (FFWC 2018; FFWC 2021), publicly downloadable from the FFWC legacy portal at `old.ffwc.gov.bd/index.php/reports/annual-flood-reports`. For the 2022 north-east monsoon event, the FFWC Sentinel-1-derived national inundation map (FFWC 2022) was used as the direct institutional reference, supplemented by the peer-reviewed Sentinel-1 + Otsu thresholding analysis of Tariq et al. (2026) which adopts a methodology directly comparable to the A.5 pipeline used here. The 2022 event at SW46.9L Bahadurabad was a moderate-magnitude flood (Jamuna stage +23 cm above danger level in June 2022), providing a methodologically valuable test of the satellite-flood-extent pipeline in the regime where discrimination of standing water from saturated soil and flooded vegetation is most challenging. For the 1988 and 1998 historical events, daily FFWC bulletin content was sourced through the peer-reviewed analytical literature — Mirza (2003) and Chowdhury (2000) respectively — rather than from the primary FFWC paper-archive at WAPDA Bhaban, on the grounds that (a) the 1988 event predates the Sentinel-1 IW record and is included for narrative context only, and (b) peer-reviewed analytical sources provide methodologically equivalent or stronger documentation of bulletin content than student transcription of paper records."

---

## 6. Acceptance criterion check

> Acceptance: docs/ffwc_bulletin_inventory.md exists with per-event-year status (recoverable / pending FFWC / using secondary citation / dropped from F4).

| Year | Status |
|---|---|
| 1988 | **Using secondary citation** (Mirza 2003, Brammer 1990); **dropped from F4** |
| 1998 | **Using secondary citation** (Chowdhury 2000, Mirza 2003); **F4 conditional on Landsat-5 TM QC** |
| 2017 | **Recoverable — primary** (AFR 2017 in hand) |
| 2020 | **Recoverable — primary** (AFR 2020 in hand) |
| 2022 | **Recoverable — substitute composite** (FFWC sat_2022.pdf + Tariq 2026 + Prothom Alo bulletin republication); **F4 retained** |

**No "pending FFWC" status remaining. Acceptance satisfied. Check 6c CLOSED.**

---

## 7. Outstanding A.5-dependent decision

**Single carry-over to A.5 phase:** the 1998 F4 inclusion decision. If A.5 phase produces a Landsat-5 TM scene catalogue for the 1998 monsoon (Jul–Sep) and at least 2 cloud-free scenes at the SW46.9L AOI pass radiometric QC, retain 1998 in F4. Otherwise demote to narrative-only.

This is not a Check 6c blocker. It is a Phase-α-style decision that opens during A.5 and must close before A.7 opens on Day 6.

---

## 8. FFWC Sentinel-1 inundation-map URL audit (added v2.1, 2026-05-30)

The FFWC legacy portal navigation template (`old.ffwc.gov.bd`, applied across all sub-pages) lists five Sentinel-1 satellite-based inundation products. The navigation entries persist as a template artefact regardless of whether the underlying files exist on the server. The audit below records the HTTP status verified 2026-05-30 for each, and the verdict on whether the product should be retained in the A.7 source corpus.

| URL | HTTP | PDF magic-bytes? | Machine-text? | Geographic scope | A.7 verdict |
|---|---|---|---|---|---|
| `sat_2022.pdf` | 200 OK | Yes | Yes (sparse raster glyphs) | National extent | **Retain — direct for 2022** |
| `sat_2022_06_NE.pdf` | 200 OK | Yes | Yes (NE rivers: Surma/Kushiyara/Sutia/Juri/Manu/Khowai/Titas) | NE region only | Retain — context |
| `sat_2021.pdf` | 200 OK | Yes | Yes (lat/lon ticks 88–92°E, 20–27°N) | National extent | Retain — context |
| `sat_2020.pdf` | 200 OK | Yes | **No** | National extent (vector-only assumed) | **Retain conditional on visual inspection** |
| `sat_2017_ff.pdf` | **404** | n/a | n/a | (Would have been) pre-monsoon haor/Sylhet flash flood, March–April 2017 | **Drop — wrong event for SW46.9L regardless of availability** |

### Reproducibility / future-audit note

If a reviewer asks how this audit was performed: each URL was probed via HTTP GET with PDF magic-byte verification (`%PDF-` header check) on 2026-05-30. The `sat_2020.pdf` empty-text result was treated as inconclusive (could be a valid vector-rendered cartographic product with no embedded text stream, or could be a partial-file corruption); browser visual inspection is the correct disambiguating test. The `sat_2017_ff.pdf` 404 was verified twice (direct fetch and screenshot from user browser).

### Process lesson recorded against M3

v2 of this document treated FFWC portal navigation entries as availability claims and propagated five URLs into §4 without per-URL HTTP verification. This is a category-mistake against M3 (no link/function hallucination): a navigation entry is a *claim* about availability, not availability itself. The corrective discipline going forward is the *verify-before-recommend* rule — any URL list emitted to a user must have each URL HTTP-probed in the same session. Probe outcomes carry the verification claim, navigation listings do not. This rule applies equally to BWDB/IWM/CEGIS/MoEFCC portals during Chain B and Chain D acquisition phases.

---

*End of FFWC bulletin inventory v2.1. Check 6c closed; URL audit reconciled.*
