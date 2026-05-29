"""
B.1 ESGF acquisition — REST-based, no intake-esgf dependency.

Strategy
--------
1. Query DKRZ's SOLR endpoint with distrib=true + replica=true to find
   all dataset entries for each locked (GCM, experiment, variable, table,
   variant) tuple across the Europe/AU federation (DKRZ + NCI + CEDA).
2. For each dataset found, fetch its file-level wget script URL.
3. Persist wget scripts to results/cmip6_raw/wget/ for inspection.
4. Emit acquisition manifest with dataset IDs, data nodes, checksums.

Run order
---------
  1. python -m chain_b_cmip6.b1_acquisition_rest       # generates scripts
  2. inspect results/cmip6_raw/wget/                   # human review
  3. bash <script>.sh -s                               # unauthenticated DL

No authentication. No Globus. No library wrappers. Standard library only.
"""

from __future__ import annotations
import json
import logging
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — locked matrix
# ---------------------------------------------------------------------------

# DKRZ as the federation entry point with distrib=true reaches NCI + CEDA
SEARCH_ENDPOINT = "https://esgf-data.dkrz.de/esg-search/search"
WGET_ENDPOINT   = "https://esgf-data.dkrz.de/esg-search/wget"

LOCKED_TUPLES = [
    # (source_id,        experiment_id)
    ("ACCESS-CM2",       "historical"),
    ("ACCESS-CM2",       "ssp245"),
    ("ACCESS-CM2",       "ssp585"),
    ("MPI-ESM1-2-HR",    "historical"),
    ("MPI-ESM1-2-HR",    "ssp245"),
    ("MPI-ESM1-2-HR",    "ssp585"),
    ("GFDL-ESM4",        "historical"),
    ("GFDL-ESM4",        "ssp245"),
    ("GFDL-ESM4",        "ssp585"),
]
VARIABLE = "pr"
TABLE    = "day"
VARIANT  = "r1i1p1f1"

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

OUT_DIR  = Path("results/cmip6_raw/wget")
OUT_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(exist_ok=True)
RUN_TS   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
LOG_PATH = DOCS_DIR / f"B1_acquisition_{RUN_TS}.log"
MANIFEST = DOCS_DIR / f"B1_acquisition_manifest_{RUN_TS}.json"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("b1_acq")


# ---------------------------------------------------------------------------
# Dataset discovery
# ---------------------------------------------------------------------------

def find_datasets(source_id: str, experiment_id: str) -> list[dict]:
    """Return dataset records for a locked tuple, federated across Europe/AU."""
    params = {
        "project":       "CMIP6",
        "source_id":     source_id,
        "experiment_id": experiment_id,
        "variable_id":   VARIABLE,
        "table_id":      TABLE,
        "variant_label": VARIANT,
        "type":          "Dataset",
        "format":        "application/solr+json",
        "limit":         100,
        "distrib":       "true",
        "latest":        "true",
        "replica":       "true",
    }
    url = SEARCH_ENDPOINT + "?" + urllib.parse.urlencode(params)
    log.info("  Querying federation for %s / %s", source_id, experiment_id)
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            data = json.loads(resp.read())
        docs = data["response"].get("docs", [])
        n    = data["response"].get("numFound", 0)
        log.info("    numFound=%d", n)
        return docs
    except Exception as e:
        log.error("    Query failed: %s: %s", type(e).__name__, e)
        return []


def select_primary_dataset(docs: list[dict]) -> dict | None:
    """If multiple datasets returned (replicas), prefer non-replica original."""
    if not docs:
        return None
    originals = [d for d in docs if not d.get("replica", False)]
    chosen = originals[0] if originals else docs[0]
    return chosen


# ---------------------------------------------------------------------------
# wget script generation
# ---------------------------------------------------------------------------

def fetch_wget_script(dataset_id: str) -> str | None:
    """Get the auto-generated wget script for a dataset_id."""
    params = {
        "dataset_id": dataset_id,
        "download_structure": "source_id,experiment_id,variant_label",
    }
    url = WGET_ENDPOINT + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        log.error("    wget script fetch failed for %s: %s", dataset_id, e)
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

log.info("=" * 72)
log.info("B.1 ESGF acquisition — REST-based")
log.info("Run timestamp (UTC): %s", RUN_TS)
log.info("Endpoint: %s", SEARCH_ENDPOINT)
log.info("=" * 72)

manifest = {
    "run_timestamp_utc": RUN_TS,
    "endpoint":          SEARCH_ENDPOINT,
    "matrix":            {"variable": VARIABLE, "table": TABLE, "variant": VARIANT},
    "tuples":            [],
}

for source_id, experiment_id in LOCKED_TUPLES:
    log.info("")
    log.info("%s / %s", source_id, experiment_id)
    docs = find_datasets(source_id, experiment_id)
    chosen = select_primary_dataset(docs)
    record = {
        "source_id":     source_id,
        "experiment_id": experiment_id,
        "n_candidates":  len(docs),
        "chosen":        None,
        "wget_path":     None,
        "status":        "PENDING",
    }
    if not chosen:
        record["status"] = "GAP"
        log.error("    No datasets found — GAP")
    else:
        dataset_id = chosen.get("id") or chosen.get("instance_id")
        record["chosen"] = {
            "id":         chosen.get("id"),
            "instance":   chosen.get("instance_id"),
            "data_node":  chosen.get("data_node"),
            "is_replica": chosen.get("replica", False),
            "version":    chosen.get("version"),
            "number_of_files": chosen.get("number_of_files"),
        }
        log.info("    chosen: %s @ %s",
                 chosen.get("instance_id"), chosen.get("data_node"))

        script = fetch_wget_script(dataset_id)
        if script:
            safe_name = f"wget_{source_id}_{experiment_id}.sh".replace("/", "_")
            script_path = OUT_DIR / safe_name
            script_path.write_text(script)
            script_path.chmod(0o755)
            record["wget_path"] = str(script_path)
            record["status"]    = "OK"
            log.info("    wget script: %s", script_path)
        else:
            record["status"] = "WGET_FAIL"

    manifest["tuples"].append(record)

# Persist manifest
MANIFEST.write_text(json.dumps(manifest, indent=2))

# Verdict
log.info("")
log.info("=" * 72)
log.info("VERDICT")
log.info("=" * 72)
ok       = sum(1 for t in manifest["tuples"] if t["status"] == "OK")
gaps     = sum(1 for t in manifest["tuples"] if t["status"] == "GAP")
fails    = sum(1 for t in manifest["tuples"] if t["status"] == "WGET_FAIL")
log.info("OK         : %d / 9", ok)
log.info("GAP        : %d / 9", gaps)
log.info("WGET_FAIL  : %d / 9", fails)
if ok == 9:
    log.info("PASS — all 9 wget scripts generated. Inspect %s before executing.", OUT_DIR)
else:
    log.warning("PARTIAL — review manifest %s for failed tuples.", MANIFEST)
log.info("")
log.info("Log     : %s", LOG_PATH)
log.info("Manifest: %s", MANIFEST)
