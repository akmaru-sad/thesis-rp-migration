#!/usr/bin/env bash
# fetch_ffwc_afrs.sh
# ---------------------------------------------------------------------------
# Purpose : Download FFWC Annual Flood Reports for the years required by A.7
#           (and adjacent-year context), with retry, SHA-256 logging, and
#           PDF magic-byte verification.
# Project : UG_Thesis-v1-locked-edit-2  (A.7 / Check 6c)
# Author  : <to be filled by user>
# Verified portal state: 2026-05-29
# Source  : http://old.ffwc.gov.bd/index.php/reports/annual-flood-reports
# ---------------------------------------------------------------------------
# Usage   : bash scripts/fetch_ffwc_afrs.sh [OUTPUT_DIR]
#           Default OUTPUT_DIR = data/ffwc
# ---------------------------------------------------------------------------
# Exit codes:
#   0  All required years fetched and verified.
#   1  One or more required-year fetches failed after retries.
#   2  PDF magic-byte verification failed for one or more files.
#   3  curl/wget not available.
# ---------------------------------------------------------------------------

set -euo pipefail

OUTPUT_DIR="${1:-data/ffwc}"
LOG_FILE="${OUTPUT_DIR}/fetch_log_$(date -u +%Y%m%dT%H%M%SZ).txt"

# Years to fetch. 2017 and 2020 are REQUIRED by A.7. 2018, 2019, 2021 are
# adjacent-year context (cheap insurance). 2022+ are not online as of
# 2026-05-29; do not attempt.
REQUIRED_YEARS=("17" "20")
CONTEXT_YEARS=("18" "19" "21")

BASE_URL="http://old.ffwc.gov.bd/images"
MAX_RETRY=3
RETRY_SLEEP=5  # seconds

# -- Preflight --------------------------------------------------------------
if ! command -v curl >/dev/null 2>&1; then
    echo "ERROR: curl not found. Install curl and re-run." >&2
    exit 3
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "ERROR: sha256sum not found. Install coreutils and re-run." >&2
    exit 3
fi

mkdir -p "${OUTPUT_DIR}"
: > "${LOG_FILE}"

log() {
    local msg="[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
    echo "${msg}" | tee -a "${LOG_FILE}"
}

# -- PDF magic-byte verification --------------------------------------------
# A valid PDF begins with the bytes 0x25 0x50 0x44 0x46 0x2D ("%PDF-").
# This catches the common failure mode where a portal returns an HTML
# error page with .pdf in the URL and a 200 status code.
verify_pdf() {
    local f="$1"
    if [ ! -s "${f}" ]; then
        return 1
    fi
    local magic
    magic=$(head -c 5 "${f}" | od -An -c | tr -d ' ')
    if [ "${magic}" = "%PDF-" ]; then
        return 0
    fi
    return 2
}

# -- Fetch with retry -------------------------------------------------------
fetch_one() {
    local yr="$1"        # two-digit year, e.g. "17"
    local label="$2"     # "REQUIRED" or "CONTEXT"
    local url="${BASE_URL}/annual${yr}.pdf"
    local out="${OUTPUT_DIR}/AFR_20${yr}.pdf"
    local attempt=0
    local rc

    log "FETCH ${label} year=20${yr}  url=${url}"

    while [ ${attempt} -lt ${MAX_RETRY} ]; do
        attempt=$((attempt + 1))
        rc=0
        curl --silent --show-error --fail --location \
             --connect-timeout 30 --max-time 300 \
             --user-agent "Mozilla/5.0 (research; thesis A.7 validation)" \
             --output "${out}" "${url}" || rc=$?

        if [ ${rc} -eq 0 ]; then
            verify_pdf "${out}"
            local vrc=$?
            if [ ${vrc} -eq 0 ]; then
                local sha
                sha=$(sha256sum "${out}" | awk '{print $1}')
                local sz
                sz=$(stat -c %s "${out}")
                log "  OK       attempt=${attempt} bytes=${sz} sha256=${sha}"
                return 0
            else
                log "  FAIL_PDF attempt=${attempt} (file present but not a valid PDF; removing)"
                rm -f "${out}"
            fi
        else
            log "  FAIL     attempt=${attempt} curl_rc=${rc}"
        fi

        if [ ${attempt} -lt ${MAX_RETRY} ]; then
            log "  sleep ${RETRY_SLEEP}s before retry"
            sleep ${RETRY_SLEEP}
        fi
    done

    log "  GIVE_UP year=20${yr} after ${MAX_RETRY} attempts"
    return 1
}

# -- Main -------------------------------------------------------------------
log "=== FFWC AFR fetch session start ==="
log "Output dir : ${OUTPUT_DIR}"
log "Log file   : ${LOG_FILE}"

required_failed=0
context_failed=0

for yr in "${REQUIRED_YEARS[@]}"; do
    fetch_one "${yr}" "REQUIRED" || required_failed=$((required_failed + 1))
done

for yr in "${CONTEXT_YEARS[@]}"; do
    fetch_one "${yr}" "CONTEXT"  || context_failed=$((context_failed + 1))
done

log "--- Summary ---"
log "REQUIRED fetched : $(( ${#REQUIRED_YEARS[@]} - required_failed ))/${#REQUIRED_YEARS[@]}"
log "CONTEXT  fetched : $(( ${#CONTEXT_YEARS[@]}  - context_failed  ))/${#CONTEXT_YEARS[@]}"

if [ ${required_failed} -gt 0 ]; then
    log "FAIL: required years incomplete; investigate portal state and re-run."
    log "      Fallback: open http://old.ffwc.gov.bd/index.php/reports/annual-flood-reports"
    log "      in a browser and download missing AFRs manually."
    exit 1
fi

if [ ${context_failed} -gt 0 ]; then
    log "WARN: context years incomplete (non-blocking for A.7)."
fi

log "=== FFWC AFR fetch session OK ==="
exit 0
