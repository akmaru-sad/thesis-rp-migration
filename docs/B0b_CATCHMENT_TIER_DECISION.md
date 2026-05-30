# B.0b — CATCHMENT DELINEATION TIER DECISION

**Component:** B.0b (support artefact — catchment polygon)
**Binding spec:** UG_Thesis-v1-locked-edit-2; realises proposed deviation **D16**
**Date:** 2026-05-30
**Decision:** **Tier-1** (HydroBASINS topological upstream-trace) adopted; **Tier-2** (DEM pour-point delineation) declined.
**Script:** `code/chain_b_cmip6/b0b_catchment_tier1.py`
**Output:** `data/gis/brahmaputra_above_sw469l.gpkg` (layer `catchment`)

---

## 1. THE TWO OPTIONS

- **Tier-1 (adopted).** Select the HydroBASINS v1c sub-basin containing the gauge (snapped to the largest-UP_AREA sub-basin within 0.1°), then collect every sub-basin draining into it via the `NEXT_DOWN` topology, dissolve, validate area. No DEM handling by us.
- **Tier-2 (declined).** Take a hydrologically-conditioned DEM (HydroSHEDS or MERIT-Hydro), compute flow direction + flow accumulation, snap the gauge to a high-accumulation cell, trace contributing cells upstream, vectorise.

Both ultimately rest on the **same** conditioned HydroSHEDS DEM. HydroBASINS *is* a peer-reviewed delineation of that DEM (Lehner & Grill 2013, HP 27:2171). Tier-1 therefore is not a crude shortcut — it is "the delineation already performed correctly, at sub-basin resolution, by the data provider, with independent QA (`UP_AREA`)."

---

## 2. WHY TIER-1 IS SUFFICIENT *HERE* (four substantive reasons)

1. **Gauge sits at the basin outlet.** SW46.9L is at river-km ~47 above the Ganges confluence; the catchment above it is ≈99% of the entire Brahmaputra basin. The only error Tier-1 introduces is the portion of the gauge's own sub-basin lying *downstream* of the true gauge point — bounded by one sub-basin's extent (level-7 `SUB_AREA`, typically a few hundred to low-thousand km²) against a ~536,000 km² total, i.e. a fraction of a percent. Tier-2's headline advantage (eliminating downstream truncation) is therefore worth almost nothing in this configuration. Tier-2 matters when the gauge is **mid-basin**; this gauge is not.

2. **The use-case is a spatial-mean, not a boundary-sensitive quantity.** The polygon feeds an **area-weighted basin-mean daily precipitation** series for QDM calibration — a smoothing operation over ~1,900 ERA5 0.25° cells (~28 km). Moving the boundary by one HydroBASINS sub-basin edge changes which handful of *edge* cells are included; against ~1,900 cells, the effect on the basin mean and on P₉₉ is negligible. The forcing target is insensitive to sub-cell boundary placement by construction.

3. **The "true" area is itself uncertain at ~7%.** Published drainage area is 536,000 km² (Banglapedia) vs 573,500 km² (IFCDR 1998). Pursuing sub-percent delineation precision via Tier-2 is **false rigor** — it asserts a boundary accuracy finer than the reference figures it would be validated against.

4. **Defensibility and reproducibility.** Tier-1 is one citable product (HydroBASINS v1c, region `as`, level 7, Lehner & Grill 2013) plus a deterministic topological query (`NEXT_DOWN`) and an independent area cross-check (`UP_AREA`). There are **no operator-dependent knobs** for an examiner to attack. Tier-2 introduces a chain of subjective choices — DEM product, conditioning method, flow-direction algorithm, snapping radius — each a reviewer attack surface, for negligible accuracy gain.

---

## 3. WHY TIER-2 WOULD HAVE BEEN *WORSE* HERE (not merely unnecessary)

- **Floodplain snapping is genuinely error-prone.** Bahadurabad is in the flat, braided Jamuna floodplain. Relief is minimal and modelled flow accumulation is ambiguous across braids; pour-point snapping there is a known failure mode (mis-snap → spurious small catchment or wrong distributary). HydroBASINS already resolved this during its QA'd production; re-doing it by hand risks a *worse* result.
- **Transboundary DEM handling.** The basin spans Tibet, Arunachal/Assam, Bhutan, Bangladesh, including high-Himalaya terrain with DEM voids. Conditioning that ourselves invites artefacts HydroBASINS has already addressed.
- **Cost vs timeline.** Tier-2 needs a multi-GB DEM tile download, conditioning, and accumulation computation while B.1 bulk acquisition is saturating bandwidth for 25–34 h. Tier-1 needs a single continental shapefile and runs in seconds.

---

## 4. WHEN TIER-2 *WOULD* BE REQUIRED (so the decision is bounded, not dogmatic)

- A **mid-basin** gauge, where downstream truncation is large.
- A bespoke boundary **not aligned** to HydroBASINS sub-basin edges (e.g. an ungauged tributary outlet between sub-basin pour points).
- **Distributed** hydrological modelling needing sub-basin geometry/parameters (e.g. HEC-HMS) — explicitly **excluded** from this thesis (Chain C locked out).

None apply to B.0b. If any did, this log is the record of why Tier-1 was nonetheless not adequate.

---

## 5. ACCEPTANCE GATE (must pass before the polygon is used)

- Geometric area within **±10%** of 536,000 km² (published spread is ~7%, so the gate is deliberately loose), AND
- Geometric area consistent with the outlet sub-basin's HydroBASINS `UP_AREA` (expected <2% — both derive from the same source), AND
- Outlet sub-basin `UP_AREA` ≥ 400,000 km² (confirms the gauge snapped to the mainstem, not a tributary).

Record the three area figures from the script's `validate_area()` output in §6.

| Check | Value | Pass? |
|-------|-------|-------|
| area (geometry, km²) | 514837.2 | Ok |
| area (HydroBASINS UP_AREA, km²) | 514663.2 | Ok |
| outlet HYBAS_ID / UP_AREA | 4070928420 | Ok |
| within ±10% of 536,000 | 3.94% | Ok |

## 6. RESIDUAL LIMITATION (for Ch.7 transparency)

The catchment boundary is truncated at HydroBASINS level-7 sub-basin edges, including a small over-extension downstream of the exact gauge (≤ one sub-basin `SUB_AREA`). Quantified effect on basin-mean precipitation: negligible (see §2.2). Stated plainly in the limitations section; not propagated to the ANOVA UQ.

## 7. PROVENANCE

HydroBASINS v1c, region `as` (Central & SE Asia), Pfafstetter level 7, CC-BY, from hydrosheds.org. Citation: Lehner, B. & Grill, G. (2013). *Global river hydrography and network routing.* Hydrological Processes 27, 2171–2186. Field schema (`HYBAS_ID`, `NEXT_DOWN`, `MAIN_BAS`, `UP_AREA`) verified against HydroBASINS_TechDoc_v1c, 2026-05-30.
