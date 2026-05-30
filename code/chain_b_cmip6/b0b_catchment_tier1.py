#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
b0b_catchment_tier1.py
=====================================================================
Component B.0b (support) — Tier-1 catchment polygon for SW46.9L
Brahmaputra / Jamuna at Bahadurabad Transit (25.1303 N, 89.7346 E).

Produces the catchment polygon consumed by b0b_era5_basinmean.py
(`--polygon`). Realises decision D16, Tier-1 path.

METHOD (Tier-1, topological — NO DEM required)
----------------------------------------------
HydroBASINS v1c (Lehner & Grill 2013) sub-basins were delineated from
the hydrologically-conditioned HydroSHEDS DEM by the data provider.
Each sub-basin carries NEXT_DOWN (the id of the sub-basin it drains
into) and UP_AREA (total upstream area). We therefore:
  1. locate the sub-basin containing the gauge (snap = pick the
     largest-UP_AREA sub-basin within a small buffer -> the mainstem);
  2. trace ALL upstream sub-basins via the NEXT_DOWN topology;
  3. dissolve them into one polygon;
  4. validate the geometric area three ways (geometry vs HydroBASINS
     UP_AREA vs published ~536,000 km2);
  5. export GeoPackage.

Rationale for Tier-1 over Tier-2 (DEM pour-point delineation):
see docs/B0b_CATCHMENT_TIER_DECISION.md.

INPUT  : HydroBASINS Asia shapefile, e.g. hybas_as_lev07_v1c.shp
         (free, CC-BY, https://www.hydrosheds.org/products/hydrobasins;
         also on GEE as WWF/HydroSHEDS/v1/Basins/hybas_<level>).
OUTPUT : results/gis/brahmaputra_above_sw469l.gpkg   (tracked; derived artefact)
           layer 'catchment'  : dissolved single polygon + attributes
           layer 'subbasins'  : constituent sub-basins (QA)
         docs/B0b_catchment_tier1_summary.json

Verified (M3, 2026-05-30): HydroBASINS field schema HYBAS_ID /
NEXT_DOWN(0=outlet) / MAIN_BAS / UP_AREA / SUB_AREA / PFAF_ID per
HydroBASINS_TechDoc_v1c. Citation: Lehner & Grill 2013 HP 27:2171.

Deps: geopandas, shapely, pandas, numpy. Env: `esgf`.
=====================================================================
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
GAUGE_LON = 89.7346          # SW46.9L Bahadurabad Transit (EPSG:4326)
GAUGE_LAT = 25.1303
GAUGE_NAME = "SW46.9L Bahadurabad Transit"

DRAINAGE_AREA_KM2 = 536000.0     # Banglapedia anchor
DRAINAGE_AREA_ALT = 573500.0     # IFCDR 1998 alternative
AREA_TOLERANCE = 0.10            # accept +/-10% (published spread is ~7%)
MAINSTEM_MIN_UP_AREA = 400000.0  # outlet sub-basin sanity floor (km2)

SNAP_BUFFER_DEG = 0.10           # search radius for the gauge sub-basin
EQUAL_AREA_CRS = "EPSG:6933"     # World Cylindrical Equal Area (km2)

LOG = logging.getLogger("tier1")


# ----------------------------------------------------------------------
# PURE TOPOLOGY  (testable without geopandas)
# ----------------------------------------------------------------------
def trace_upstream(hybas_id, next_down, outlet_id: int) -> set[int]:
    """Return the set of HYBAS_IDs at or upstream of `outlet_id`,
    following the NEXT_DOWN topology (NEXT_DOWN == 0 means no
    downstream connection / basin outlet)."""
    outlet_id = int(outlet_id)
    upstream_of: dict[int, list[int]] = defaultdict(list)
    for hid, nd in zip(hybas_id, next_down):
        hid, nd = int(hid), int(nd)
        if nd != 0:
            upstream_of[nd].append(hid)
    collected: set[int] = set()
    queue = deque([outlet_id])
    while queue:
        cur = queue.popleft()
        if cur in collected:
            continue
        collected.add(cur)
        for up in upstream_of.get(cur, ()):
            if up not in collected:
                queue.append(up)
    return collected


# ----------------------------------------------------------------------
# DELINEATION
# ----------------------------------------------------------------------
def _normalise_columns(gdf):
    gdf = gdf.rename(columns={c: c.upper() for c in gdf.columns
                              if c.lower() != "geometry"})
    for col in ("HYBAS_ID", "NEXT_DOWN", "MAIN_BAS"):
        if col not in gdf.columns:
            raise KeyError(f"HydroBASINS field '{col}' missing -- is this "
                           f"a HydroBASINS v1c shapefile? cols={list(gdf.columns)}")
        gdf[col] = gdf[col].astype("int64")   # stored as double -> int keys
    if "UP_AREA" not in gdf.columns:
        raise KeyError("UP_AREA missing; required for snap + area check")
    return gdf


def locate_outlet(gdf, buffer_deg: float = SNAP_BUFFER_DEG):
    """Snap the gauge to the mainstem: among sub-basins intersecting a
    small buffer around the gauge, choose the one with the largest
    UP_AREA. Returns (outlet_row, n_candidates)."""
    from shapely.geometry import Point
    gauge_buf = Point(GAUGE_LON, GAUGE_LAT).buffer(buffer_deg)
    cand = gdf[gdf.intersects(gauge_buf)]
    if cand.empty:
        raise RuntimeError(
            f"no sub-basin within {buffer_deg} deg of the gauge -- "
            f"check coords / CRS / that the file covers region 'as'")
    outlet = cand.loc[cand["UP_AREA"].idxmax()]
    LOG.info("gauge sub-basin candidates within %.2f deg: %d",
             buffer_deg, len(cand))
    LOG.info("outlet sub-basin HYBAS_ID=%d  UP_AREA=%.0f km2  MAIN_BAS=%d",
             int(outlet["HYBAS_ID"]), float(outlet["UP_AREA"]),
             int(outlet["MAIN_BAS"]))
    if outlet["UP_AREA"] < MAINSTEM_MIN_UP_AREA:
        LOG.warning("outlet UP_AREA %.0f km2 < %.0f floor -- gauge may have "
                    "snapped OFF the mainstem; widen SNAP_BUFFER_DEG or "
                    "verify coordinates / lon convention.",
                    outlet["UP_AREA"], MAINSTEM_MIN_UP_AREA)
    return outlet, len(cand)


def delineate(gdf, outlet):
    main_bas = int(outlet["MAIN_BAS"])
    basin = gdf[gdf["MAIN_BAS"] == main_bas].copy()
    LOG.info("sub-basins in MAIN_BAS=%d: %d", main_bas, len(basin))
    ids = trace_upstream(basin["HYBAS_ID"].to_numpy(),
                         basin["NEXT_DOWN"].to_numpy(),
                         int(outlet["HYBAS_ID"]))
    catch = basin[basin["HYBAS_ID"].isin(ids)].copy()
    LOG.info("sub-basins at/above gauge: %d", len(catch))
    # repair any invalid geometries before dissolve
    catch["geometry"] = catch.geometry.buffer(0)
    return catch


def validate_area(catch, outlet):
    geom_km2 = float(catch.to_crs(EQUAL_AREA_CRS).geometry.area.sum()) / 1e6
    up_area = float(outlet["UP_AREA"])
    rel_pub = abs(geom_km2 - DRAINAGE_AREA_KM2) / DRAINAGE_AREA_KM2
    rel_up = abs(geom_km2 - up_area) / up_area
    LOG.info("AREA geometry        : %.0f km2", geom_km2)
    LOG.info("AREA HydroBASINS UP  : %.0f km2  (rel diff %.1f%%)",
             up_area, rel_up * 100)
    LOG.info("AREA published (BGpd): %.0f km2  (rel diff %.1f%%)",
             DRAINAGE_AREA_KM2, rel_pub * 100)
    LOG.info("AREA published (IFCDR alt): %.0f km2", DRAINAGE_AREA_ALT)
    if rel_pub > AREA_TOLERANCE:
        LOG.warning("geometry vs published outside +/-%.0f%% -- inspect "
                    "outlet selection / level before accepting.",
                    AREA_TOLERANCE * 100)
    else:
        LOG.info("AREA CHECK: PASS (within +/-%.0f%% of published).",
                 AREA_TOLERANCE * 100)
    return geom_km2, up_area, rel_pub, rel_up


def export(catch, outlet, geom_km2, up_area, level: int,
           out_gpkg: Path, out_json: Path):
    import geopandas as gpd
    out_gpkg.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    diss = catch.dissolve()                       # single multipolygon
    diss = diss[["geometry"]].copy()
    attrs = {
        "name": "Brahmaputra catchment above SW46.9L",
        "gauge": GAUGE_NAME,
        "gauge_lon": GAUGE_LON,
        "gauge_lat": GAUGE_LAT,
        "outlet_hybas_id": int(outlet["HYBAS_ID"]),
        "main_bas": int(outlet["MAIN_BAS"]),
        "pfaf_level": int(level),
        "n_subbasins": int(len(catch)),
        "area_km2_geom": round(geom_km2, 1),
        "up_area_km2_hydrobasins": round(up_area, 1),
        "source": "HydroBASINS v1c region 'as' (Lehner & Grill 2013, "
                  "HP 27:2171); upstream trace via NEXT_DOWN",
        "method": "Tier-1 topological delineation",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    for k, v in attrs.items():
        diss[k] = v
    diss = gpd.GeoDataFrame(diss, geometry="geometry", crs=catch.crs)

    diss.to_file(out_gpkg, layer="catchment", driver="GPKG")
    catch.to_file(out_gpkg, layer="subbasins", driver="GPKG")
    LOG.info("GeoPackage written: %s (layers: catchment, subbasins)", out_gpkg)

    with out_json.open("w") as fh:
        json.dump(attrs, fh, indent=2)
    LOG.info("summary written: %s", out_json)
    return attrs


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Tier-1 catchment delineation")
    p.add_argument("--hydrobasins", type=Path, required=True,
                   help="HydroBASINS Asia shapefile, e.g. hybas_as_lev07_v1c.shp")
    p.add_argument("--level", type=int, default=7,
                   help="Pfafstetter level of the input file (for metadata)")
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--buffer-deg", type=float, default=SNAP_BUFFER_DEG)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s")

    import geopandas as gpd
    if not args.hydrobasins.exists():
        LOG.error("HydroBASINS file not found: %s", args.hydrobasins)
        return 2

    out_gpkg = args.repo_root / "results" / "gis" / "brahmaputra_above_sw469l.gpkg"
    out_json = args.repo_root / "docs" / "B0b_catchment_tier1_summary.json"

    LOG.info("=== Tier-1 catchment delineation for %s ===", GAUGE_NAME)
    gdf = gpd.read_file(args.hydrobasins)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    gdf = gdf.to_crs("EPSG:4326")
    gdf = _normalise_columns(gdf)
    LOG.info("loaded %d sub-basins (level %d)", len(gdf), args.level)

    outlet, _ = locate_outlet(gdf, args.buffer_deg)
    catch = delineate(gdf, outlet)
    geom_km2, up_area, _, _ = validate_area(catch, outlet)
    export(catch, outlet, geom_km2, up_area, args.level, out_gpkg, out_json)
    LOG.info("=== done -> feed to b0b_era5_basinmean.py --polygon %s ===",
             out_gpkg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
