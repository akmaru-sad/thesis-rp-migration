"""
B.1 ESGF smoke test — Check 6b (revised post-Level-3 confirmation).

Purpose
-------
Verify Level 4 dataset availability (variant_label + grid_label) for the
locked GCM × experiment × variable matrix on the two confirmed-healthy
Europe/AU-domain ESGF SOLR indices (DKRZ, NCI), and emit a dated audit
log usable as the D14 reproducibility artefact.

Locked matrix
-------------
  GCMs        : ACCESS-CM2, MPI-ESM1-2-HR, GFDL-ESM4
  Experiments : historical, ssp245, ssp585
  Variable    : pr (daily, primary per m1)
  Table       : day
  Variant     : r1i1p1f1
  Grid        : gn OR gr (accept either; flag if only gr)

Verdict logic
-------------
  PASS    — all 9 tuples return >=1 dataset on at least one index.
  GAP     — any tuple returns 0; trigger Stage S2 (add CEDA) per Check 6b.
  ERROR   — exception during query; capture and re-run with --verbose.
"""

from __future__ import annotations
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import intake_esgf
from intake_esgf import ESGFCatalog

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INDICES = {
    "esgf-data.dkrz.de": True,
    "esgf.nci.org.au":   True,
}

LOCKED_GCMS   = ["ACCESS-CM2", "MPI-ESM1-2-HR", "GFDL-ESM4"]
EXPERIMENTS   = ["historical", "ssp245", "ssp585"]
VARIABLE      = "pr"
TABLE         = "day"
VARIANT       = "r1i1p1f1"
GRIDS         = ["gn", "gr"]

LOG_DIR  = Path("docs")
LOG_DIR.mkdir(exist_ok=True)
RUN_TS   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
LOG_PATH = LOG_DIR / f"B1_esgf_probe_{RUN_TS}.log"
JSON_PATH = LOG_DIR / f"B1_esgf_probe_{RUN_TS}.json"

# ---------------------------------------------------------------------------
# Logging — stdout + file, both captured
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("b1_smoke")

# ---------------------------------------------------------------------------
# Index configuration — explicit whitelist
# ---------------------------------------------------------------------------

intake_esgf.conf.set(indices=INDICES)
log.info("Indices configured: %s", list(INDICES.keys()))

# ---------------------------------------------------------------------------
# Probe routine
# ---------------------------------------------------------------------------

def probe(source_id: str, experiment_id: str) -> dict:
    """Return a structured probe result for one (GCM, experiment) tuple."""
    result = {
        "source_id":     source_id,
        "experiment_id": experiment_id,
        "n_datasets":    0,
        "grid_labels":   [],
        "data_nodes":    [],
        "status":        "UNKNOWN",
        "error":         None,
    }
    try:
        cat = ESGFCatalog()
        sub = cat.search(
            project       = "CMIP6",
            source_id     = source_id,
            experiment_id = experiment_id,
            variable_id   = VARIABLE,
            table_id      = TABLE,
            variant_label = VARIANT,
            grid_label    = GRIDS,
        )
        df = sub.df if hasattr(sub, "df") else None
        if df is not None and len(df) > 0:
            result["n_datasets"]  = int(len(df))
            result["grid_labels"] = sorted(df["grid_label"].unique().tolist()) \
                                    if "grid_label" in df.columns else []
            if "data_node" in df.columns:
                result["data_nodes"] = sorted(df["data_node"].unique().tolist())
            result["status"] = "OK"
        else:
            result["status"] = "EMPTY"
    except Exception as e:
        result["status"] = "ERROR"
        result["error"]  = f"{type(e).__name__}: {e}"
    return result

# ---------------------------------------------------------------------------
# Execute matrix
# ---------------------------------------------------------------------------

log.info("=" * 72)
log.info("Check 6b smoke test - Level 4 integrity probe")
log.info("Run timestamp (UTC): %s", RUN_TS)
log.info("=" * 72)

results = []
for gcm in LOCKED_GCMS:
    log.info("")
    log.info("GCM: %s", gcm)
    for exp in EXPERIMENTS:
        r = probe(gcm, exp)
        results.append(r)
        if r["status"] == "OK":
            log.info("  %-12s -> %d dataset(s) | grids=%s | nodes=%d",
                     exp, r["n_datasets"], r["grid_labels"],
                     len(r["data_nodes"]))
        elif r["status"] == "EMPTY":
            log.warning("  %-12s -> 0 datasets (GAP)", exp)
        else:
            log.error("  %-12s -> ERROR: %s", exp, r["error"])

# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

log.info("")
log.info("=" * 72)
log.info("VERDICT")
log.info("=" * 72)

gaps   = [r for r in results if r["status"] == "EMPTY"]
errors = [r for r in results if r["status"] == "ERROR"]

if not gaps and not errors:
    verdict = "PASS"
    log.info("PASS - all 9 tuples returned >=1 dataset at Level 4.")
    log.info("Next step: generate wget scripts per dataset (bash <script>.sh -s).")
    log.info("Concurrent: begin Check 6a (CDS API registration).")
elif errors:
    verdict = "ERROR"
    log.error("ERROR - %d tuple(s) failed with exception; re-run required.", len(errors))
    for r in errors:
        log.error("  %s / %s: %s", r["source_id"], r["experiment_id"], r["error"])
elif gaps:
    verdict = "GAP"
    log.warning("GAP - %d of 9 tuples returned 0 datasets.", len(gaps))
    log.warning("Trigger Stage S2: add 'esgf.ceda.ac.uk' to indices and re-run.")
    for r in gaps:
        log.warning("  MISSING: %s / %s", r["source_id"], r["experiment_id"])

# ---------------------------------------------------------------------------
# Persist JSON for downstream audit
# ---------------------------------------------------------------------------

audit = {
    "run_timestamp_utc": RUN_TS,
    "indices":           list(INDICES.keys()),
    "matrix": {
        "gcms":        LOCKED_GCMS,
        "experiments": EXPERIMENTS,
        "variable":    VARIABLE,
        "table":       TABLE,
        "variant":     VARIANT,
        "grids":       GRIDS,
    },
    "verdict": verdict,
    "results": results,
}
JSON_PATH.write_text(json.dumps(audit, indent=2))
log.info("")
log.info("Audit log : %s", LOG_PATH)
log.info("Audit JSON: %s", JSON_PATH)
