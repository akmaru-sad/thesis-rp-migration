"""A.1 acceptance gate.

Runs a checklist of imports + environment + repo state. Exits 0 only if every
check passes. Run from repo root:

    python code/utils/verify_a1.py

Exit codes
----------
0 : all checks pass; A.1 acceptance gate met
1 : one or more checks failed; A.1 NOT met (see report for which)
2 : unexpected exception during verification (bug in this script)
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional

# We deliberately do NOT use any local imports above utils.paths to keep this
# script runnable even if subpackages are broken. paths.py is the only
# first-party module we depend on.
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "code"))


# ---------------------------------------------------------------------------
# Reporting primitives
# ---------------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Disable colour if stdout is not a terminal (e.g. CI, pipe to file)
if not sys.stdout.isatty():
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""
    fatal: bool = True  # if False, failure is a warning, not a gate fail


def _check(name: str, fatal: bool = True) -> Callable:
    """Decorator turning a check function into a CheckResult."""

    def decorator(fn: Callable[[], str]) -> Callable[[], CheckResult]:
        def wrapper() -> CheckResult:
            try:
                detail = fn() or ""
                return CheckResult(name=name, ok=True, detail=detail, fatal=fatal)
            except Exception as exc:  # noqa: BLE001
                return CheckResult(
                    name=name,
                    ok=False,
                    detail=f"{type(exc).__name__}: {exc}",
                    fatal=fatal,
                )

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator


def _emit(result: CheckResult) -> None:
    if result.ok:
        marker = f"{GREEN}✓{RESET}"
    elif result.fatal:
        marker = f"{RED}✗{RESET}"
    else:
        marker = f"{YELLOW}!{RESET}"
    print(f"  {marker} {result.name}")
    if result.detail:
        for line in result.detail.splitlines():
            print(f"      {line}")


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


@_check("Python version >= 3.11")
def check_python_version() -> str:
    if sys.version_info < (3, 11):
        raise RuntimeError(f"Python {sys.version_info.major}.{sys.version_info.minor} < 3.11")
    return f"Python {sys.version.split()[0]}"


@_check("Running on Linux (WSL2)")
def check_platform() -> str:
    if sys.platform != "linux":
        raise RuntimeError(
            f"sys.platform = {sys.platform!r}; expected 'linux' (WSL2 Ubuntu per D-A1)."
        )
    # WSL2 detection (best effort)
    osrel = Path("/proc/sys/kernel/osrelease")
    suffix = osrel.read_text().strip() if osrel.exists() else "(osrelease unreadable)"
    return f"sys.platform=linux; kernel={suffix}"


@_check("Repo root layout sanity")
def check_repo_layout() -> str:
    required_dirs = [
        "code/chain_a_satellite",
        "code/chain_b_cmip6",
        "code/chain_d_ffa",
        "code/chain_e_uq",
        "code/utils",
        "data/observed",
        "data/satellite",
        "data/cmip6/raw",
        "results/baseline",
        "results/ffa",
        "results/migration",
        "results/uncertainty",
        "docs/chapters",
        "tests",
    ]
    missing = [d for d in required_dirs if not (REPO_ROOT / d).exists()]
    if missing:
        raise RuntimeError(f"Missing directories: {', '.join(missing)}")
    return f"All {len(required_dirs)} required directories present"


@_check(".env file present")
def check_env_file() -> str:
    p = REPO_ROOT / ".env"
    if not p.exists():
        raise RuntimeError(f".env not found at {p}. Copy from .env.example: cp .env.example .env")
    return f".env found at {p}"


@_check("DATA_ROOT resolves to an existing directory")
def check_data_root() -> str:
    from utils.paths import get_paths  # local import after sys.path setup

    P = get_paths(require_data_root=True)
    return f"DATA_ROOT = {P.data_root}"


# Library imports — grouped so a single failure does not stop the whole list
_REQUIRED_LIBS = [
    # core scientific
    ("numpy", None),
    ("pandas", None),
    ("scipy", None),
    ("xarray", None),
    ("dask", None),
    # geo
    ("rasterio", None),
    ("rioxarray", None),
    ("geopandas", None),
    ("shapely", None),
    ("pyproj", None),
    ("fiona", None),
    # climate I/O
    ("netCDF4", None),
    ("cftime", None),
    # regridding (WSL2 only)
    ("xesmf", None),
    # bias correction
    ("xclim", None),
    # GEE
    ("ee", None),
    ("geemap", None),
    # CMIP6
    ("intake_esm", None),
    # ERA5
    ("cdsapi", None),
    # FFA / stats
    ("statsmodels", None),
    ("lmoments3", None),
    ("sklearn", None),
    ("skimage", None),
    # plotting
    ("matplotlib", None),
    ("seaborn", None),
    # I/O
    ("pyarrow", None),
    ("openpyxl", None),
    # dev
    ("pytest", None),
    ("dotenv", None),  # python-dotenv exposes itself as 'dotenv'
]


@_check("All required libraries import")
def check_imports() -> str:
    failed = []
    versions = []
    for mod_name, _ in _REQUIRED_LIBS:
        try:
            m = importlib.import_module(mod_name)
            v = getattr(m, "__version__", "n/a")
            versions.append(f"{mod_name}={v}")
        except Exception as exc:  # noqa: BLE001
            failed.append(f"{mod_name} ({type(exc).__name__}: {exc})")
    if failed:
        raise RuntimeError("Failed imports:\n  " + "\n  ".join(failed))
    return f"{len(versions)} libraries imported. Versions:\n  " + "\n  ".join(versions)


@_check("Local package 'utils' importable")
def check_local_package() -> str:
    from utils.logging_config import configure_logging  # noqa: F401
    from utils.paths import get_paths  # noqa: F401

    return "utils.paths and utils.logging_config importable"


@_check("Git repository initialised and has remote 'origin'", fatal=False)
def check_git_remote() -> str:
    try:
        out = subprocess.run(
            ["git", "remote", "-v"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"git remote -v failed: {exc.stderr.strip()}")
    if "origin" not in out.stdout:
        raise RuntimeError("No remote 'origin' configured. See A1_SETUP.md Step 8.")
    return out.stdout.strip().splitlines()[0]


@_check("Pre-commit hooks installed", fatal=False)
def check_precommit() -> str:
    hook = REPO_ROOT / ".git" / "hooks" / "pre-commit"
    if not hook.exists():
        raise RuntimeError(f"Hook not at {hook}. Run: pre-commit install (see A1_SETUP.md Step 9).")
    return f"Hook present at {hook}"


@_check("GEE authentication credentials present", fatal=False)
def check_gee_auth() -> str:
    home = Path(os.environ.get("HOME", str(Path.home())))
    cred_paths = [
        home / ".config" / "earthengine" / "credentials",
        home / ".earthengine" / "credentials",  # alternative location
    ]
    found = [p for p in cred_paths if p.exists()]
    if not found:
        raise RuntimeError("No GEE credentials file found. Run `earthengine authenticate`.")
    return f"Credentials at {found[0]}"


@_check("CDS API key file present (~/.cdsapirc)", fatal=False)
def check_cds() -> str:
    p = Path(os.environ.get("HOME", str(Path.home()))) / ".cdsapirc"
    if not p.exists():
        raise RuntimeError(
            "~/.cdsapirc not present. Needed for ERA5 acquisition (Chain B.0b). "
            "Can defer until Day 4."
        )
    return f".cdsapirc at {p}"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> int:
    print(f"\n{BOLD}{CYAN}A.1 ACCEPTANCE GATE — thesis-rp-migration{RESET}")
    print(f"{CYAN}Repo: {REPO_ROOT}{RESET}\n")

    checks = [
        check_python_version,
        check_platform,
        check_repo_layout,
        check_env_file,
        check_data_root,
        check_imports,
        check_local_package,
        check_git_remote,
        check_precommit,
        check_gee_auth,
        check_cds,
    ]

    results: List[CheckResult] = []
    for chk in checks:
        try:
            r = chk()
        except Exception:  # noqa: BLE001
            print(f"{RED}INTERNAL ERROR in {chk.__name__}:{RESET}")
            traceback.print_exc()
            return 2
        results.append(r)
        _emit(r)

    n_fatal_fail = sum(1 for r in results if not r.ok and r.fatal)
    n_warn = sum(1 for r in results if not r.ok and not r.fatal)
    n_pass = sum(1 for r in results if r.ok)

    print()
    print(f"{BOLD}Summary:{RESET}  pass={n_pass}  fail(fatal)={n_fatal_fail}  warn={n_warn}")

    if n_fatal_fail == 0 and n_warn == 0:
        print(f"\n{GREEN}{BOLD}A.1 ACCEPTANCE GATE: PASS{RESET}\n")
        return 0
    if n_fatal_fail == 0:
        print(
            f"\n{YELLOW}{BOLD}A.1 ACCEPTANCE GATE: PASS WITH WARNINGS{RESET}"
            f"  ({n_warn} non-fatal item(s) — address before Chain A starts.)\n"
        )
        return 0
    print(
        f"\n{RED}{BOLD}A.1 ACCEPTANCE GATE: FAIL{RESET}"
        f"  ({n_fatal_fail} fatal check(s) failed.)  Fix and re-run.\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
