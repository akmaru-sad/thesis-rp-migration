"""Pytest gate around verify_a1.py.

Runs the A.1 verification script as a subprocess and asserts exit 0.

Failing here means A.1 has not passed; do not proceed to A.2.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFY = REPO_ROOT / "code" / "utils" / "verify_a1.py"


def test_verify_a1_exits_zero():
    assert VERIFY.exists(), f"verify_a1.py missing at {VERIFY}"
    result = subprocess.run(
        [sys.executable, str(VERIFY)],
        capture_output=True,
        text=True,
    )
    # Always print so failures surface in pytest output
    print(result.stdout)
    print(result.stderr, file=sys.stderr)
    assert result.returncode == 0, (
        f"verify_a1.py exited {result.returncode}. "
        f"A.1 acceptance gate not met. See output above."
    )
