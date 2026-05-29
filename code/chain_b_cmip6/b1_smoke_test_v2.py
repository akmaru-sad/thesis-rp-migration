"""
B.1 ESGF smoke test v2 — per-index query, union results.

Fixes:
  - ValueError on multi-index aggregation (query indices separately).
  - Diagnostic relaxation for GFDL-ESM4 (probe without variant_label).
"""

from __future__ import annotations
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import intake_esgf
from intake_esgf import ESGFCatalog

INDICES_ALL = ["esgf-data.dkrz.de", "esgf.nci.org.au", "esgf.ceda.ac.uk"]

LOCKED_GCMS = ["ACCESS-CM2", "MPI-ESM1-2-HR", "GFDL-ESM4"]
EXPERIMENTS = ["historical", "ssp245", "ssp585"]
VARIABLE    = "pr"
TABLE       = "day"
VARIANT     = "r1i1p1f1"
GRIDS       = ["gn", "gr"]

LOG_DIR   = Path("docs")
LOG_DIR.mkdir(exist_ok=True)
RUN_TS    = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
LOG_PATH  = LOG_DIR / f"B1_esgf_probe_v2_{RUN_TS}.log"
JSON_PATH = LOG_DIR / f"B1_esgf_probe_v2_{RUN_TS}.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("b1_smoke_v2")


def probe_single_index(index_name, source_id, experiment_id, relax_variant=False):
    """Query one index for one (GCM, experiment) tuple."""
    intake_esgf.conf.set(indices={index_name: True})
    try:
        cat = ESGFCatalog()
        kwargs = dict(
            project       = "CMIP6",
            source_id     = source_id,
            experiment_id = experiment_id,
            variable_id   = VARIABLE,
            table_id      = TABLE,
            grid_label    = GRIDS,
        )
        if not relax_variant:
            kwargs["variant_label"] = VARIANT
        sub = cat.search(**kwargs)
        df = sub.df if hasattr(sub, "df") else None
        if df is None or len(df) == 0:
            return {"status": "EMPTY", "n": 0, "variants": [], "nodes": []}
        variants = sorted(df["variant_label"].unique().tolist()) \
                   if "variant_label" in df.columns else []
        nodes = sorted(df["data_node"].unique().tolist()) \
                if "data_node" in df.columns else []
        return {"status": "OK", "n": int(len(df)),
                "variants": variants, "nodes": nodes}
    except Exception as e:
        msg = f"{type(e).__name__}: {e}"
        # NoSearchResults is an empty result, not a real error
        if "NoSearchResults" in msg:
            return {"status": "EMPTY", "n": 0, "variants": [], "nodes": []}
        return {"status": "ERROR", "n": 0, "variants": [], "nodes": [],
                "error": msg}


def probe_tuple(source_id, experiment_id):
    """Probe a tuple across all indices; relax variant if locked variant empty."""
    result = {
        "source_id": source_id,
        "experiment_id": experiment_id,
        "per_index": {},
        "union_n": 0,
        "locked_variant_present": False,
        "available_variants": [],
        "status": "UNKNOWN",
    }
    union_variants = set()
    union_n = 0
    for idx in INDICES_ALL:
        r = probe_single_index(idx, source_id, experiment_id, relax_variant=False)
        result["per_index"][idx] = r
        if r["status"] == "OK":
            union_n += r["n"]
            union_variants.update(r["variants"])
    result["union_n"] = union_n
    result["locked_variant_present"] = (VARIANT in union_variants) and union_n > 0
    result["available_variants"] = sorted(union_variants)

    # If locked variant absent, probe relaxed (any variant) for diagnostic
    if union_n == 0:
        log.warning("    relaxing variant filter for diagnostic...")
        relaxed_variants = set()
        for idx in INDICES_ALL:
            r = probe_single_index(idx, source_id, experiment_id, relax_variant=True)
            if r["status"] == "OK":
                relaxed_variants.update(r["variants"])
        result["available_variants"] = sorted(relaxed_variants)
        if relaxed_variants:
            result["status"] = "VARIANT_GAP"
        else:
            result["status"] = "TUPLE_GAP"
    else:
        result["status"] = "OK"
    return result


log.info("=" * 72)
log.info("Check 6b smoke test v2 - per-index probe with variant diagnostic")
log.info("Run timestamp (UTC): %s", RUN_TS)
log.info("Indices: %s", INDICES_ALL)
log.info("=" * 72)

results = []
for gcm in LOCKED_GCMS:
    log.info("")
    log.info("GCM: %s", gcm)
    for exp in EXPERIMENTS:
        log.info("  %s:", exp)
        r = probe_tuple(gcm, exp)
        results.append(r)
        for idx, pr in r["per_index"].items():
            log.info("    %-25s -> status=%s n=%d", idx, pr["status"], pr["n"])
        if r["status"] == "OK":
            log.info("    UNION: %d datasets, locked variant r1i1p1f1 present",
                     r["union_n"])
        elif r["status"] == "VARIANT_GAP":
            log.warning("    UNION: locked variant absent; available: %s",
                        r["available_variants"])
        else:
            log.error("    UNION: tuple absent at Level 3+ on Europe/AU domain")

log.info("")
log.info("=" * 72)
log.info("VERDICT")
log.info("=" * 72)

ok_count          = sum(1 for r in results if r["status"] == "OK")
variant_gap_count = sum(1 for r in results if r["status"] == "VARIANT_GAP")
tuple_gap_count   = sum(1 for r in results if r["status"] == "TUPLE_GAP")

log.info("OK (locked variant available)  : %d / 9", ok_count)
log.info("VARIANT_GAP (other variants ok): %d / 9", variant_gap_count)
log.info("TUPLE_GAP (no data on Eur/AU)  : %d / 9", tuple_gap_count)

if tuple_gap_count == 0 and variant_gap_count == 0:
    verdict = "PASS"
    log.info("PASS - locked variant r1i1p1f1 available for all 9 tuples.")
elif tuple_gap_count == 0:
    verdict = "VARIANT_SUBSTITUTION_REQUIRED"
    log.warning("Locked variant unavailable for some tuples; alternative variants exist.")
    log.warning("Decision required: substitute variant or invoke S3 (US-domain).")
else:
    verdict = "TUPLE_GAP"
    log.error("At least one tuple has no data on Europe/AU domain at any variant.")
    log.error("Required action: Stage S2 (add CEDA) or S3 (US-domain Globus index).")

audit = {
    "run_timestamp_utc": RUN_TS,
    "indices":           INDICES_ALL,
    "verdict":           verdict,
    "summary": {
        "ok": ok_count,
        "variant_gap": variant_gap_count,
        "tuple_gap": tuple_gap_count,
    },
    "results": results,
}
JSON_PATH.write_text(json.dumps(audit, indent=2))
log.info("")
log.info("Audit log : %s", LOG_PATH)
log.info("Audit JSON: %s", JSON_PATH)
