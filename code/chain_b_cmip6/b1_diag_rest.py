"""
B.1 diagnostic — direct ESGF SOLR REST query, bypasses intake-esgf.
Confirms whether ACCESS-CM2 / MPI-ESM1-2-HR / GFDL-ESM4 daily pr
are actually present at DKRZ and NCI indices, independent of any
Python library aggregation logic.
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

INDICES = {
    "DKRZ": "https://esgf-data.dkrz.de/esg-search/search",
    "NCI":  "https://esgf.nci.org.au/esg-search/search",
}

GCMS        = ["ACCESS-CM2", "MPI-ESM1-2-HR", "GFDL-ESM4"]
EXPERIMENTS = ["historical", "ssp245", "ssp585"]

def query(base_url, source_id, experiment_id):
    params = {
        "project":       "CMIP6",
        "source_id":     source_id,
        "experiment_id": experiment_id,
        "variable_id":   "pr",
        "table_id":      "day",
        "variant_label": "r1i1p1f1",
        "type":          "Dataset",
        "format":        "application/solr+json",
        "limit":         0,                # we only need the count
        "distrib":       "false",          # this index only, no federation
        "latest":        "true",
        "replica":       "false",
    }
    url = base_url + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())
        return data.get("response", {}).get("numFound", -1)
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"

print(f"{'INDEX':<6} {'GCM':<18} {'EXPERIMENT':<12} {'numFound'}")
print("-" * 60)
results = []
for idx_name, idx_url in INDICES.items():
    for gcm in GCMS:
        for exp in EXPERIMENTS:
            n = query(idx_url, gcm, exp)
            print(f"{idx_name:<6} {gcm:<18} {exp:<12} {n}")
            results.append({"index": idx_name, "gcm": gcm, "exp": exp, "n": n})

# Save audit artefact
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
out = Path(f"docs/B1_diag_rest_{ts}.json")
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2))
print(f"\nWritten: {out}")
