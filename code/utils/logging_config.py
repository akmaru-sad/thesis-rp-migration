"""Logging configuration for thesis-rp-migration.

Per M6: every script uses Python `logging`, with rotating file handlers
written under <repo_root>/logs/, and exit codes propagated cleanly.

Usage:
    from utils.logging_config import configure_logging
    log = configure_logging("A.2_bwdb_qc")
    log.info("starting QC")
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from .paths import REPO_ROOT

_DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    component_id: str,
    level: int = logging.INFO,
    log_dir: Optional[Path] = None,
) -> logging.Logger:
    """Set up console + rotating-file logging for a component run.

    Parameters
    ----------
    component_id : str
        Logical component name (e.g. "A.2_bwdb_qc", "B.4a_qdm_train"). Used
        as logger name and log filename.
    level : int
        Log level for both handlers.
    log_dir : Path, optional
        Override log directory (default: <repo_root>/logs/).

    Returns
    -------
    logging.Logger
        Configured logger ready for `.info()`, `.warning()`, `.error()`.
    """
    if log_dir is None:
        log_dir = REPO_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log = logging.getLogger(component_id)
    log.setLevel(level)
    # If re-imported, clear previous handlers to avoid duplicate emission
    log.handlers.clear()
    log.propagate = False

    fmt = logging.Formatter(_DEFAULT_FORMAT, datefmt=_DATE_FORMAT)

    # Console
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    log.addHandler(ch)

    # Rotating file (5 MB × 5 files)
    fh = RotatingFileHandler(
        log_dir / f"{component_id}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
    )
    fh.setLevel(level)
    fh.setFormatter(fmt)
    log.addHandler(fh)

    log.info("=" * 72)
    log.info("Logger %s initialised", component_id)
    log.info("=" * 72)

    return log
