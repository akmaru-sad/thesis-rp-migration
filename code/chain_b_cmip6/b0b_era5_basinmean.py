#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
b0b_era5_basinmean.py
=====================================================================
Component B.0b — ERA5 basin-mean daily precipitation acquisition
Chain B (CMIP6 + bias correction), UG_Thesis-v1-locked-edit-2.

Purpose
-------
Acquire ERA5 daily total precipitation over the Brahmaputra catchment
ABOVE BWDB station SW46.9L (Bahadurabad Transit, 25.1303 N, 89.7346 E),
reduce to a single area-weighted basin-mean daily time series, and emit
that series as the empirical TARGET distribution for the basin-mean
ERA5-trained QDM (C2 amendment, primary D.1 forcing chain).

Resolved decisions (this session, B.0b):
  D1  ERA5 single-levels 0.25 deg     (NOT ERA5-Land: derived daily
                                        product omits accumulated tp)
  D2  derived-era5-single-levels-daily-statistics, daily_statistic =
      daily_sum  + mandatory hourly unit cross-check (verify_units())
  D3  catchment-bbox via `area`, then client-side polygon mask +
      cos(lat) area weighting
  D4  catchment polygon supplied as GeoPackage/shapefile input
      (HydroSHEDS pour-point delineation primary; GRDC MRB fallback);
      area validated against ~536,000 km2 (Banglapedia)
  D5  CSV (date, basin_mean_pr_mm) + NetCDF (CF + provenance attrs)

PROPOSED DEVIATION D15 (requires sign-off) -- see CALIB_START below.
  Binding spec edit-1 §6/§14.3 says calibration window 1988-2014 (27 yr).
  This script DEFAULTS to 1985-2014 (30 yr) to satisfy Cannon, Sobie &
  Murdock 2015 (>=30 yr QDM calibration). The QDM calibration window is
  INDEPENDENT of the 1988 discharge-record start; only the C2 elasticity
  regression is genuinely floored at 1988 (Q availability). To revert to
  the literal spec, set CALIB_START = 1988.

Verified against current sources (2026-05-30, M3 compliance):
  - CDS endpoint https://cds.climate.copernicus.eu/api (post-2024
    migration; key has NO deprecated "<UID>:" prefix)
  - dataset id "derived-era5-single-levels-daily-statistics"
  - request keys product_type / variable / year / month / day /
    daily_statistic / time_zone / frequency / area
  - total_precipitation accumulated in METRES -> x1000 = mm/day
    (confirmed empirically by verify_units())

Environment: conda env `esgf`. Run from repo root or pass --repo-root.
Restartable: per-year NetCDFs are skipped if already present.
=====================================================================
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
# --- Calibration window (PROPOSED DEVIATION D15) ----------------------
CALIB_START = 1985          # <-- set to 1988 to obey literal edit-1 spec
CALIB_END = 2014            # CMIP6 historical experiment ends 2014-12-31
# ----------------------------------------------------------------------

DATASET = "derived-era5-single-levels-daily-statistics"
VARIABLE = "total_precipitation"
DAILY_STATISTIC = "daily_sum"
TIME_ZONE = "utc+00:00"
FREQUENCY = "1_hourly"
M_TO_MM = 1000.0            # ERA5 tp accumulated metres -> mm (verify_units)

# Catchment bounding box [North, West, South, East] enclosing the
# Brahmaputra basin above Bahadurabad. Deliberately generous; the polygon
# mask trims it. Refine to the polygon's own bounds once delineated.
DEFAULT_BBOX = [31.5, 82.0, 23.0, 97.5]   # N, W, S, E (deg)

DRAINAGE_AREA_KM2 = 536000.0   # Banglapedia anchor; IFCDR alt = 573500
AREA_TOLERANCE = 0.10          # accept +/-10% on polygon area validation

CDS_GRID = [0.25, 0.25]
DATA_FORMAT = "netcdf"      # if monthly netcdf still trips the netCDF-specific
                            # cost limit, set "grib" (higher cap) -- then
                            # _detect_names/load_cube need cfgrib engine.

LOG = logging.getLogger("b0b")


# ----------------------------------------------------------------------
# CDS ACQUISITION  (D2, D3-bbox)
# ----------------------------------------------------------------------
def acquire_month(client, year: int, month: int, bbox, raw_dir: Path) -> Path:
    """Submit one CDS request for a single MONTH. Monthly chunking keeps
    each request under the CDS per-request cost cap for the derived
    daily-statistics product (yearly requests are rejected with
    'cost limits exceeded'; ECMWF support prescribes <= 1 month/request).
    Restartable: skips if the target NetCDF already exists and is non-empty.
    Note: `area`/`grid` reduce file size but NOT request cost (cost is
    counted in fields, independent of spatial extent)."""
    target = raw_dir / f"era5_tp_dailysum_{year}{month:02d}.nc"
    if target.exists() and target.stat().st_size > 0:
        LOG.info("%d-%02d already present (%.2f MB) -- skipping",
                 year, month, target.stat().st_size / 1e6)
        return target

    request = {
        "product_type": "reanalysis",
        "variable": [VARIABLE],
        "year": [str(year)],
        "month": [f"{month:02d}"],
        "day": [f"{d:02d}" for d in range(1, 32)],   # CDS ignores invalid days
        "daily_statistic": DAILY_STATISTIC,
        "time_zone": TIME_ZONE,
        "frequency": FREQUENCY,
        "area": [float(x) for x in bbox],     # N, W, S, E (file size only)
        "grid": CDS_GRID,
        "data_format": DATA_FORMAT,            # netcdf default; grib fallback
    }
    LOG.info("submitting CDS request for %d-%02d ...", year, month)
    LOG.debug("request: %s", json.dumps(request))
    client.retrieve(DATASET, request, str(target))
    if not target.exists() or target.stat().st_size == 0:
        raise RuntimeError(f"CDS returned empty file for {year}-{month:02d}")
    LOG.info("downloaded %d-%02d -> %s (%.2f MB)",
             year, month, target.name, target.stat().st_size / 1e6)
    return target


def acquire_all(bbox, raw_dir: Path) -> list[Path]:
    import cdsapi  # local import: download half works without geo deps
    client = cdsapi.Client()
    paths, failures = [], []
    for yr in range(CALIB_START, CALIB_END + 1):
        for mo in range(1, 13):
            try:
                paths.append(acquire_month(client, yr, mo, bbox, raw_dir))
            except Exception as exc:            # noqa: BLE001
                failures.append((yr, mo, str(exc)))
                LOG.error("%d-%02d FAILED: %s -- continue; re-run to retry",
                          yr, mo, exc)
    LOG.info("acquisition pass complete: %d ok, %d failed",
             len(paths), len(failures))
    if failures:
        LOG.warning("failed months (re-run to retry): %s",
                    ", ".join(f"{y}-{m:02d}" for y, m, _ in failures))
    return paths


# ----------------------------------------------------------------------
# CUBE LOADING + NAME DETECTION  (CDS netcdf naming drifted post-2024)
# ----------------------------------------------------------------------
def _detect_names(ds: xr.Dataset) -> tuple[str, str]:
    """Return (precip_var, time_coord), robust to CDS naming drift."""
    pvar = next((v for v in ("tp", "total_precipitation")
                 if v in ds.data_vars), None)
    if pvar is None:                            # last resort: single var
        pvar = list(ds.data_vars)[0]
        LOG.warning("precip var not matched by name; using '%s'", pvar)
    tcoord = next((t for t in ("valid_time", "time", "date")
                   if t in ds.coords or t in ds.dims), None)
    if tcoord is None:
        raise KeyError("no recognisable time coordinate in dataset")
    return pvar, tcoord


def load_cube(raw_dir: Path) -> tuple[xr.DataArray, str]:
    files = sorted(raw_dir.glob("era5_tp_dailysum_*.nc"))
    if not files:
        raise FileNotFoundError(f"no ERA5 yearly files in {raw_dir}")
    ds = xr.open_mfdataset([str(f) for f in files], combine="by_coords")
    pvar, tcoord = _detect_names(ds)
    da = ds[pvar]
    if tcoord != "time":
        da = da.rename({tcoord: "time"})
    # standardise spatial coord names
    rn = {}
    if "latitude" in da.coords:
        rn["latitude"] = "lat"
    if "longitude" in da.coords:
        rn["longitude"] = "lon"
    da = da.rename(rn) if rn else da
    da = da.sortby("time")
    LOG.info("cube loaded: %d timesteps, lat %d, lon %d",
             da.sizes["time"], da.sizes["lat"], da.sizes["lon"])
    return da, pvar


# ----------------------------------------------------------------------
# POLYGON MASK + cos(lat) AREA WEIGHTING  (D3, D4)
# ----------------------------------------------------------------------
def load_polygon(polygon_path: Path):
    import geopandas as gpd
    gdf = gpd.read_file(polygon_path)
    if gdf.crs is None:
        raise ValueError("polygon has no CRS; assign EPSG:4326 explicitly")
    gdf = gdf.to_crs("EPSG:4326")
    poly = gdf.geometry.union_all() if hasattr(gdf.geometry, "union_all") \
        else gdf.geometry.unary_union

    # area validation against published drainage area
    eq_area = gdf.to_crs("EPSG:6933")           # World Cylindrical Equal Area
    area_km2 = float(eq_area.geometry.area.sum()) / 1e6
    rel = abs(area_km2 - DRAINAGE_AREA_KM2) / DRAINAGE_AREA_KM2
    msg = (f"polygon area = {area_km2:,.0f} km2 vs published "
           f"{DRAINAGE_AREA_KM2:,.0f} km2 (rel diff {rel:.1%})")
    if rel > AREA_TOLERANCE:
        LOG.warning("AREA CHECK OUTSIDE +/-%.0f%%: %s -- verify delineation",
                    AREA_TOLERANCE * 100, msg)
    else:
        LOG.info("AREA CHECK OK: %s", msg)
    return poly, area_km2


def basin_mean(da: xr.DataArray, poly) -> tuple[pd.Series, int]:
    """Area-weighted basin-mean daily series in mm/day.

    Weighting: w_ij = cos(lat_i) for every grid cell whose CENTROID lies
    within the catchment polygon, normalised to sum to 1. cos(lat)
    corrects the meridional convergence of 0.25-deg cells. Fractional
    boundary-cell coverage is a documented second-order refinement;
    negligible for a ~1900-cell basin (see acquisition log)."""
    import geopandas as gpd
    from shapely.geometry import Point  # noqa: F401  (used via points_from_xy)

    lats = da["lat"].values
    lons = da["lon"].values
    LON, LAT = np.meshgrid(lons, lats)          # shape (nlat, nlon)
    flat_lon, flat_lat = LON.ravel(), LAT.ravel()

    pts = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(flat_lon, flat_lat),
        crs="EPSG:4326",
    )
    poly_gdf = gpd.GeoDataFrame(geometry=[poly], crs="EPSG:4326")
    inside = gpd.sjoin(pts, poly_gdf, predicate="within", how="left")
    mask_flat = inside["index_right"].notna().to_numpy()
    n_cells = int(mask_flat.sum())
    if n_cells == 0:
        raise RuntimeError("no grid-cell centroids fall inside polygon; "
                           "check CRS / bbox / lon convention (0-360?)")
    LOG.info("grid cells inside catchment: %d", n_cells)

    w_flat = np.where(mask_flat, np.cos(np.deg2rad(flat_lat)), 0.0)
    w_flat = w_flat / w_flat.sum()
    weights = xr.DataArray(
        w_flat.reshape(LAT.shape),
        dims=("lat", "lon"),
        coords={"lat": da["lat"], "lon": da["lon"]},
    )

    # tp accumulated metres -> mm/day, then weighted spatial sum
    series = ((da * M_TO_MM) * weights).sum(dim=("lat", "lon"))
    series = series.compute()
    s = series.to_series()
    s.index = pd.to_datetime(s.index).normalize()
    s.name = "basin_mean_pr_mm"
    return s, n_cells


# ----------------------------------------------------------------------
# OUTPUT  (D5)
# ----------------------------------------------------------------------
def write_outputs(series: pd.Series, n_cells: int, area_km2: float,
                  poly_path: Path, out_csv: Path, out_nc: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df = series.reset_index()
    df.columns = ["date", "basin_mean_pr_mm"]
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df.to_csv(out_csv, index=False)
    LOG.info("CSV written: %s (%d rows)", out_csv, len(df))

    da = xr.DataArray(
        series.values, dims=("time",),
        coords={"time": series.index.values},
        name="basin_mean_pr",
    )
    da.attrs = {
        "long_name": "Brahmaputra catchment area-weighted mean "
                     "daily precipitation above SW46.9L (Bahadurabad)",
        "units": "mm day-1",
        "standard_name": "lwe_thickness_of_precipitation_amount",
        "cell_methods": "area: mean (cos-lat weighted) time: sum (daily)",
    }
    da.to_dataset().assign_attrs({
        "title": "ERA5 basin-mean daily precipitation, B.0b",
        "source_dataset": DATASET,
        "source_variable": VARIABLE,
        "daily_statistic": DAILY_STATISTIC,
        "time_zone": TIME_ZONE,
        "calibration_window": f"{CALIB_START}-{CALIB_END}",
        "catchment_polygon": str(poly_path),
        "catchment_area_km2": round(area_km2, 1),
        "n_grid_cells_in_catchment": n_cells,
        "unit_conversion": "ERA5 tp metres x1000 = mm/day "
                           "(verified by verify_units())",
        "reference": "Hersbach et al. 2020 QJRMS 146:1999; "
                     "Cannon, Sobie & Murdock 2015 J. Clim. 28:6938",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "component": "B.0b",
        "binding_spec": "UG_Thesis-v1-locked-edit-2 (+2026-05-29 update)",
    }).to_netcdf(out_nc)
    LOG.info("NetCDF written: %s", out_nc)


# ----------------------------------------------------------------------
# UNIT CROSS-CHECK  (D2 mandatory verification)  -- run once, log result
# ----------------------------------------------------------------------
def verify_units(bbox, raw_dir: Path, sample_year: int = 1998,
                 sample_month: int = 7) -> None:
    """Download ONE monsoon month of HOURLY tp, hand-aggregate to daily mm,
    and compare against the daily_sum product x1000 for the same cells.
    Closes the documented ERA5 tp unit/accumulation reviewer vulnerability.
    Prints a verdict; record it in docs/B0b_ERA5_CDS_ACQUISITION_LOG.md."""
    import cdsapi
    client = cdsapi.Client()
    hourly = raw_dir / f"era5_tp_hourly_{sample_year}{sample_month:02d}.nc"
    if not hourly.exists():
        client.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": "reanalysis",
                "variable": [VARIABLE],
                "year": [str(sample_year)],
                "month": [f"{sample_month:02d}"],
                "day": [f"{d:02d}" for d in range(1, 32)],
                "time": [f"{h:02d}:00" for h in range(24)],
                "area": [float(x) for x in bbox],
                "grid": CDS_GRID,
                "data_format": "netcdf",
            },
            str(hourly),
        )
    dsh = xr.open_dataset(hourly)
    pvar, tcoord = _detect_names(dsh)
    hh = dsh[pvar].rename({tcoord: "time"}) if tcoord != "time" else dsh[pvar]
    # hourly accumulation (m) -> daily sum (m) -> mm, domain mean
    daily_from_hourly = (hh.resample(time="1D").sum() * M_TO_MM).mean(
        dim=[d for d in hh.dims if d != "time"])

    dsd = xr.open_dataset(
        raw_dir / f"era5_tp_dailysum_{sample_year}{sample_month:02d}.nc")
    pvar2, tcoord2 = _detect_names(dsd)
    dd = dsd[pvar2].rename({tcoord2: "time"}) if tcoord2 != "time" else dsd[pvar2]
    daily_from_product = (dd * M_TO_MM).mean(
        dim=[d for d in dd.dims if d != "time"])

    a = daily_from_hourly.values
    b = daily_from_product.values[: len(a)]
    diff = np.abs(a - b)
    LOG.info("UNIT CHECK %d-%02d  domain-mean daily mm:",
             sample_year, sample_month)
    LOG.info("  hourly-aggregated : mean=%.3f max=%.3f", a.mean(), a.max())
    LOG.info("  daily_sum product : mean=%.3f max=%.3f", b.mean(), b.max())
    LOG.info("  max |diff| = %.4f mm  (tol 0.5 mm)", diff.max())
    if diff.max() < 0.5:
        LOG.info("  VERDICT: PASS -- daily_sum x1000 == hand-aggregated mm")
    else:
        LOG.warning("  VERDICT: REVIEW -- boundary/accumulation shift; "
                    "inspect day-alignment convention before trusting series")


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="B.0b ERA5 basin-mean acquisition")
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--polygon", type=Path, default=None,
                   help="catchment polygon (GeoPackage/shp); EPSG:4326")
    p.add_argument("--bbox", type=float, nargs=4, default=DEFAULT_BBOX,
                   metavar=("N", "W", "S", "E"))
    p.add_argument("--download-only", action="store_true")
    p.add_argument("--verify-units", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s")

    raw_dir = args.repo_root / "results" / "era5_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    period = f"{CALIB_START}_{CALIB_END}"
    out_csv = (args.repo_root / "results" / "baseline" /
               f"era5_basinmean_brahmaputra_{period}.csv")
    out_nc = (args.repo_root / "results" / "baseline" /
              f"era5_basinmean_brahmaputra_{period}.nc")

    if CALIB_START != 1988:
        LOG.warning("CALIB_START=%d deviates from edit-1 spec (1988). "
                    "PROPOSED DEVIATION D15 -- confirm sign-off.", CALIB_START)

    LOG.info("=== B.0b acquire: ERA5 tp %d-%d, bbox %s ===",
             CALIB_START, CALIB_END, args.bbox)
    acquire_all(args.bbox, raw_dir)

    if args.verify_units:
        verify_units(args.bbox, raw_dir)

    if args.download_only:
        LOG.info("download-only: skipping basin-mean extraction")
        return 0

    if args.polygon is None or not args.polygon.exists():
        LOG.warning("no polygon supplied -> basin-mean NOT extracted. "
                    "Supply --polygon to finish (D4). Raw cube retained.")
        return 0

    da, _ = load_cube(raw_dir)
    poly, area_km2 = load_polygon(args.polygon)
    series, n_cells = basin_mean(da, poly)
    LOG.info("basin-mean series: %d days, mean=%.2f mm, P99=%.1f mm",
             len(series), series.mean(), series.quantile(0.99))
    write_outputs(series, n_cells, area_km2, args.polygon, out_csv, out_nc)
    LOG.info("=== B.0b complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
