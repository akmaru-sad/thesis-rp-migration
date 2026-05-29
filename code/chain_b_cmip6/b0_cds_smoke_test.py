"""
B.0 CDS API smoke test — verifies registration, licence acceptance,
and credentials by submitting a minimal ERA5 request.

A successful run downloads ~1 MB and writes era5_smoke_test.nc.
Failure modes are diagnosed inline.
"""

import sys
from pathlib import Path

try:
    import cdsapi
except ImportError:
    print("FAIL: cdsapi not installed. Run: pip install cdsapi")
    sys.exit(1)

# Check credentials file
rc = Path.home() / ".cdsapirc"
if not rc.exists():
    print(f"FAIL: {rc} does not exist. Register at "
          "https://cds.climate.copernicus.eu/ and create the file.")
    sys.exit(2)

version = getattr(cdsapi, "__version__", "unknown")
print(f"OK: cdsapi {version} installed")
print(f"OK: {rc} exists")
print()
print("Submitting minimal ERA5 request (1 hour, 1 variable, small area)...")
print("This may take 30 seconds to 5 minutes depending on CDS queue.")
print()

out = Path("era5_smoke_test.nc")

try:
    client = cdsapi.Client()
    client.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type":  ["reanalysis"],
            "variable":      ["2m_temperature"],
            "year":          ["2020"],
            "month":         ["01"],
            "day":           ["01"],
            "time":          ["00:00"],
            "area":          [26, 89, 25, 90],   # tiny box over Bangladesh
            "data_format":   "netcdf",
            "download_format": "unarchived",
        },
        str(out),
    )
except Exception as e:
    msg = f"{type(e).__name__}: {e}"
    print(f"FAIL: request errored — {msg}")
    print()
    if "403" in msg or "Forbidden" in msg:
        print("HINT: 403 usually means the ERA5 dataset licence has not been")
        print("      accepted. Visit any ERA5 dataset page on cds.climate.")
        print("      copernicus.eu while logged in, scroll to the licence")
        print("      section, and click 'Accept terms'.")
    elif "401" in msg or "Unauthorized" in msg:
        print("HINT: 401 usually means the key in ~/.cdsapirc is wrong or")
        print("      expired. Re-copy the Personal Access Token from your")
        print("      CDS profile page.")
    elif "url" in msg.lower():
        print("HINT: URL mismatch. ~/.cdsapirc should read:")
        print("      url: https://cds.climate.copernicus.eu/api")
        print("      (no /v2 suffix; that endpoint is deprecated)")
    sys.exit(3)

if out.exists() and out.stat().st_size > 1000:
    size_kb = out.stat().st_size / 1024
    print(f"PASS: downloaded {out} ({size_kb:.1f} KB)")
    print()
    print("Check 6a closed. CDS API is configured and operational.")
else:
    print(f"FAIL: {out} missing or suspiciously small")
    sys.exit(4)
