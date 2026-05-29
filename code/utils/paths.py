"""Central path resolver for thesis-rp-migration.

Reads DATA_ROOT from .env (loaded via python-dotenv) and exposes a single
get_paths() function returning a frozen dataclass of every project path.

Rationale: per D-A1-3 the repo uses relative paths under DATA_ROOT so the
thesis is portable to the supervisor's machine without code changes.

NEVER hardcode an absolute path elsewhere in the codebase. Always import:

    from utils.paths import get_paths
    P = get_paths()
    df = pd.read_excel(P.bwdb_primary)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Repo root = parent of code/ (this file lives at code/utils/paths.py)
_THIS_FILE = Path(__file__).resolve()
REPO_ROOT = _THIS_FILE.parents[2]

# Load .env from repo root (idempotent; safe to call repeatedly)
load_dotenv(REPO_ROOT / ".env", override=False)


def _required_env(key: str) -> str:
    """Fetch an environment variable or raise with a helpful message."""
    val = os.environ.get(key)
    if val is None or val.strip() == "" or val.startswith("CHANGE_ME"):
        raise RuntimeError(
            f"Environment variable {key!r} is not set or still contains 'CHANGE_ME'. "
            f"Copy .env.example to .env and fill it in. See A1_SETUP.md Step 6."
        )
    return val.strip()


def _optional_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Fetch an environment variable; return default if unset or placeholder."""
    val = os.environ.get(key, default)
    if val is None:
        return None
    val = val.strip()
    if val == "" or val.startswith("CHANGE_ME"):
        return default
    return val


@dataclass(frozen=True)
class ProjectPaths:
    """All project paths, resolved once at import time."""

    # Repo
    repo_root: Path
    code: Path
    docs: Path
    results: Path
    tests: Path
    notebooks: Path

    # External data root
    data_root: Path

    # Observed
    bwdb_primary: Path
    bwdb_fallback: Path
    bmd_dir: Path

    # Processed data buckets
    satellite_dir: Path
    cmip6_raw_dir: Path
    cmip6_bc_dir: Path
    reference_dir: Path

    # Results buckets
    res_baseline: Path
    res_validation: Path
    res_cmip6_bc: Path
    res_projections: Path
    res_ffa: Path
    res_migration: Path
    res_uncertainty: Path
    res_figures: Path

    # Station metadata (locked)
    station_id: str = "SW46.9L"
    station_name: str = "Bahadurabad_Transit"
    station_lat: float = 25.1303
    station_lon: float = 89.7346
    river: str = "Brahmaputra-Jamuna"
    drainage_area_km2: float = 536_000.0


def get_paths(require_data_root: bool = True) -> ProjectPaths:
    """Resolve all project paths.

    Parameters
    ----------
    require_data_root : bool
        If True (default) raise if DATA_ROOT is unset. Set False for
        environment-only checks (e.g. inside verify_a1.py before .env exists).
    """

    if require_data_root:
        data_root = Path(_required_env("DATA_ROOT")).expanduser().resolve()
        if not data_root.exists():
            raise RuntimeError(
                f"DATA_ROOT path {data_root} does not exist. "
                f"Create it with:  mkdir -p {data_root}"
            )
    else:
        raw = _optional_env("DATA_ROOT")
        data_root = Path(raw).expanduser().resolve() if raw else Path("/tmp/UNRESOLVED-DATA-ROOT")

    bwdb_rel = _optional_env("BWDB_PATH", "observed/bwdb_sw46p9l_bahadurabad_1988-2026.xlsx")
    bwdb_fallback_rel = _optional_env(
        "BWDB_FALLBACK_PATH", "observed/bwdb_sw267_sylhet_1988-2026.xlsx"
    )
    bmd_rel = _optional_env("BMD_PATH", "observed/bmd_daily_p_national/")

    return ProjectPaths(
        repo_root=REPO_ROOT,
        code=REPO_ROOT / "code",
        docs=REPO_ROOT / "docs",
        results=REPO_ROOT / "results",
        tests=REPO_ROOT / "tests",
        notebooks=REPO_ROOT / "notebooks",
        data_root=data_root,
        bwdb_primary=data_root / bwdb_rel,
        bwdb_fallback=data_root / bwdb_fallback_rel,
        bmd_dir=data_root / bmd_rel,
        satellite_dir=data_root / "satellite",
        cmip6_raw_dir=data_root / "cmip6" / "raw",
        cmip6_bc_dir=data_root / "cmip6" / "bias_corrected",
        reference_dir=data_root / "reference",
        res_baseline=REPO_ROOT / "results" / "baseline",
        res_validation=REPO_ROOT / "results" / "validation",
        res_cmip6_bc=REPO_ROOT / "results" / "cmip6_bc",
        res_projections=REPO_ROOT / "results" / "projections",
        res_ffa=REPO_ROOT / "results" / "ffa",
        res_migration=REPO_ROOT / "results" / "migration",
        res_uncertainty=REPO_ROOT / "results" / "uncertainty",
        res_figures=REPO_ROOT / "results" / "figures",
        station_id=_optional_env("STATION_ID", "SW46.9L"),
        station_name=_optional_env("STATION_NAME", "Bahadurabad_Transit"),
        station_lat=float(_optional_env("STATION_LAT", "25.1303")),
        station_lon=float(_optional_env("STATION_LON", "89.7346")),
        river=_optional_env("RIVER", "Brahmaputra-Jamuna"),
        drainage_area_km2=float(_optional_env("DRAINAGE_AREA_KM2", "536000")),
    )


# Convenience module-level constant; resolves lazily on first access via property pattern
# would be cleaner, but for simple import-time use this is fine.
try:
    DATA_ROOT = Path(_optional_env("DATA_ROOT", "/tmp/UNRESOLVED")).expanduser().resolve()
except Exception:
    DATA_ROOT = Path("/tmp/UNRESOLVED")
