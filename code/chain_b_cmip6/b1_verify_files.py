"""B.1 file integrity verification — opens each .nc file with xarray and reports time coverage + units."""

import glob
import xarray as xr
from pathlib import Path

NC_FILES = sorted(glob.glob("results/cmip6_raw/**/*.nc", recursive=True))

if not NC_FILES:
    print("No .nc files found under results/cmip6_raw/")
    raise SystemExit(1)

print(f"Found {len(NC_FILES)} NetCDF file(s).\n")
print(f"{'File':<70s}  {'Time steps':>10s}  {'Units':>15s}  {'Calendar':>15s}")
print("-" * 115)

issues = []
for f in NC_FILES:
    try:
        ds = xr.open_dataset(f)
        name = Path(f).name
        n_time = ds.time.size
        units = ds.pr.attrs.get("units", "?")
        calendar = ds.time.encoding.get("calendar", ds.time.attrs.get("calendar", "?"))
        print(f"{name:<70s}  {n_time:>10d}  {units:>15s}  {calendar:>15s}")
        if units != "kg m-2 s-1":
            issues.append(f"{name}: unexpected units '{units}'")
        if n_time == 0:
            issues.append(f"{name}: zero time steps")
        ds.close()
    except Exception as e:
        print(f"{Path(f).name:<70s}  ERROR: {type(e).__name__}: {e}")
        issues.append(f"{Path(f).name}: open failed")

print()
if issues:
    print(f"ISSUES FOUND ({len(issues)}):")
    for i in issues:
        print(f"  {i}")
    raise SystemExit(2)
else:
    print("All files verified clean.")
