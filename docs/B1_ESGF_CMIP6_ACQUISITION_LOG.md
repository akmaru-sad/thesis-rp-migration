# B.1 ESGF / CMIP6 Acquisition Log

**Repo path:** `docs/B1_ESGF_CMIP6_ACQUISITION_LOG.md`
**Status:** Active record. Append entries as acquisition progresses.
**First entry:** 2026-05-29
**Maintainer:** Look Sad

This document is the authoritative operational record of how CMIP6 data was acquired for the thesis "Satellite-Constrained Return-Period Migration of Flood Hazard at Bahadurabad under CMIP6." It is intended to be read by peer reviewers, replication attempts, and the supervisor's defence committee. The binding spec (`UG_Thesis-v1-locked-edit-2.txt` plus the 2026-05-29 update log) prescribes the methodology; this document records the execution.

---

## 1. Acquisition matrix (locked)

| Source | Experiment | Variable | Table | Variant | Grid |
|---|---|---|---|---|---|
| ACCESS-CM2 | historical | pr | day | r1i1p1f1 | gn |
| ACCESS-CM2 | ssp245 | pr | day | r1i1p1f1 | gn |
| ACCESS-CM2 | ssp585 | pr | day | r1i1p1f1 | gn |
| MPI-ESM1-2-HR | historical | pr | day | r1i1p1f1 | gn |
| MPI-ESM1-2-HR | ssp245 | pr | day | r1i1p1f1 | gn |
| MPI-ESM1-2-HR | ssp585 | pr | day | r1i1p1f1 | gn |
| GFDL-ESM4 | historical | pr | day | r1i1p1f1 | gr1 |
| GFDL-ESM4 | ssp245 | pr | day | r1i1p1f1 | gr1 |
| GFDL-ESM4 | ssp585 | pr | day | r1i1p1f1 | gr1 |

Supplementary variables per m1 (tasmax, tasmin) are acquired separately and not tracked in this section. They follow the same procedure.

---

## 2. Federation state at acquisition time

Acquisition was performed during the ESGF interim partitioned-federation period, between the LLNL node shutdown (2025-07-29) and the planned ESGF Next-Gen launch (May 2026 per WCRP-CMIP announcement). The federation was structurally split:

- **Europe/AU domain (legacy SOLR index):** DKRZ, NCI, CEDA, IPSL, NSC/LIU
- **US domain (Globus / ElasticSearch index):** ORNL primary, replicas at LLNL-fed test infrastructure

Data discovery and download for this thesis used the Europe/AU SOLR partition exclusively. The US-domain Globus index was not queried; no cross-domain federation was required because all 9 locked tuples resolved within the Europe/AU partition.

Healthy nodes confirmed during the 2026-05-29 acquisition session:

- `esgf-data.dkrz.de` — federation entry point; supports `distrib=true` aggregation
- `esgf.nci.org.au` — host for ACCESS-CM2 daily fields
- `esgf.ceda.ac.uk` — host for GFDL-ESM4 daily fields
- `esgf3.dkrz.de` — DKRZ replica node, surfaces GFDL-ESM4 SSP245 mirror

---

## 3. Acquisition method

### 3.1 Discovery

Datasets were discovered via direct SOLR REST queries against the DKRZ search endpoint:

```
https://esgf-data.dkrz.de/esg-search/search
```

with the following non-default parameters:

| Parameter | Value | Purpose |
|---|---|---|
| `project` | `CMIP6` | Constrain to CMIP6 holdings |
| `distrib` | `true` | Federate query across Europe/AU SOLR partition |
| `replica` | `true` | Include replicated copies, not only original publications |
| `latest` | `true` | Restrict to current dataset versions, exclude retracted |
| `type` | `Dataset` | Return dataset-level records, not file-level |
| `format` | `application/solr+json` | Machine-readable response |

Per-tuple filters added: `source_id`, `experiment_id`, `variable_id`, `table_id`, `variant_label`.

### 3.2 wget script generation

For each discovered dataset, an auto-generated wget script was fetched from:

```
https://esgf-data.dkrz.de/esg-search/wget
```

The wget scripts contain per-file download URLs targeting the dataset's host data node, plus SHA-256 checksums published by ESGF for integrity verification.

### 3.3 Download execution

Wget scripts were executed with the `-s` flag to bypass the deprecated OpenID authentication prompt:

```bash
bash wget_<source_id>_<experiment_id>.sh -s
```

The `-s` flag is the ESGF-documented mechanism for unauthenticated CMIP6 download in the post-OpenID transition period. No authentication, no Globus identity, no eduGAIN federation membership, and no institutional account were used at any point.

### 3.4 Library tooling decision

The `intake-esgf` Python library was evaluated and rejected as the acquisition driver. Two independent failure modes were reproduced across three SOLR indices on 2026-05-29:

- `ValueError: Must have equal len keys and value when setting with an iterable` raised during DataFrame assembly for ACCESS-CM2 and MPI-ESM1-2-HR queries
- Spurious empty results returned for GFDL-ESM4 because `distrib=true` semantics are not propagated consistently to all configured indices

The library failure was confirmed against ground truth (browser-based MetaGrid inspection and direct REST queries showing `numFound > 0`). The bug is a library defect, not a data-availability finding. Direct REST querying via Python's `urllib.request` (standard library, no external dependency) was adopted as the canonical acquisition driver. This decision is documented in §4 of the 2026-05-29 binding-spec update log and codified as protocol P-REST in edit-3.

---

## 4. Acquisition session — 2026-05-29

### 4.1 Discovery session

Session timestamp (UTC): `2026-05-29T03:27Z` initial diagnostics; `2026-05-29T0X:XXZ` REST acquisition.
Script: `code/chain_b_cmip6/b1_acquisition_rest.py`
Log artefacts: `docs/B1_acquisition_<UTC-timestamp>.log`, `docs/B1_acquisition_manifest_<UTC-timestamp>.json`

Diagnostic artefacts produced during library evaluation, retained for audit:

- `docs/B1_esgf_probe_2026-05-29T025017Z.json` — intake-esgf v1 smoke test (failed)
- `docs/B1_esgf_probe_v2_2026-05-29T030144Z.json` — intake-esgf v2 per-index smoke test (failed)
- `docs/B1_diag_rest_2026-05-29T031322Z.json` — REST diagnostic across DKRZ + NCI (confirmed ACCESS-CM2 + MPI-ESM1-2-HR availability, GFDL-ESM4 gap on these two nodes)
- Federated REST query 2026-05-29T03:27Z confirming GFDL-ESM4 at CEDA via `distrib=true`

### 4.2 Pilot download

Pilot tuple: ACCESS-CM2 / historical / pr / day / r1i1p1f1
Execution: `bash wget_ACCESS-CM2_historical.sh -s -v`
Log: `docs/B1_pilot_download.log`
Status: In progress at time of this log entry. Update on completion.

The pilot confirms operational viability of the no-auth path on the local network environment before bulk acquisition.

### 4.3 Per-tuple acquisition status

To be appended as each acquisition completes. Template:

```
[YYYY-MM-DDTHHMMZ]  <source_id> / <experiment_id>
  data_node      : <data_node_hostname>
  n_files        : <count>
  bytes          : <size>
  sha256_verified: <yes / partial / no>
  wall_clock     : <duration>
  notes          : <any anomalies>
```

---

## 5. Reproducibility statement

A reader wishing to reproduce this acquisition on or before the ESGF Next-Gen migration (planned May 2026) should:

1. Confirm the Europe/AU SOLR partition remains healthy (check `https://esgf.github.io/nodes.html` for current state).
2. Use the discovery query in §3.1 against the DKRZ endpoint with the parameters listed.
3. Execute wget scripts with the `-s` flag against the data nodes returned by the discovery query.
4. Verify downloaded files against the SHA-256 checksums embedded in the wget scripts.

If the acquisition is attempted after the Next-Gen migration completes, the SOLR endpoint may be deprecated and the procedure will need to be adapted to the new ElasticSearch-backed Globus index. The data themselves are persistent across the migration per the WCRP-CMIP transition announcement; only the discovery mechanism changes.

No authentication credentials, accounts, or institutional federation memberships are required to reproduce the acquisition under the procedure documented here.

---

## 6. Integrity verification

For each downloaded file:

- File-level SHA-256 checksums are published by ESGF and embedded in the auto-generated wget scripts; verification is performed automatically by the wget script on completion.
- Dataset-level integrity is verified by opening each file with `xarray.open_dataset` and confirming: (a) the `time` coordinate covers the expected calendar range, (b) the `pr` variable has units `kg m-2 s-1`, (c) the latitude/longitude bounds cover the Brahmaputra catchment polygon used for basin-mean extraction.
- Any file failing either check is re-downloaded; failures persisting across two attempts are flagged in the per-tuple status table (§4.3) and escalated.

---

## 7. Known caveats

1. **Federation partition is interim.** The two-domain split documented in §2 is a transition state and will resolve when ESGF Next-Gen launches. The procedure documented here is dated; a replication attempt post-migration will need to adapt.
2. **CEDA is on the critical path for GFDL-ESM4.** Two of three GFDL-ESM4 experiments (historical, ssp585) are available only at CEDA in the Europe/AU partition. CEDA outages during the acquisition window would force either the DKRZ-mirror fallback (where it exists) or a US-domain Globus query as an escalation.
3. **Single-variant acquisition.** Only `r1i1p1f1` is acquired per the binding spec. Inter-variant ensemble spread is not characterised in this work. This is a deliberate scope decision documented in the binding spec, not a data limitation.
4. **No HEC-RAS coupling.** This is a binding-spec exclusion; flagged here only to pre-empt the reviewer question of why hydraulic routing is absent.

---

## 8. Change log for this file

| Date | Entry | Author |
|---|---|---|
| 2026-05-29 | Initial creation; sections 1–7 populated based on Check 6b closure session. Section 4.3 pending per-tuple acquisition completion. | Look Sad |

---

**End of acquisition log. Append per-tuple entries to §4.3 as acquisitions complete.**
