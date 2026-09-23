"""Backup / replace / restore an app.asar next to an Electron install."""

from __future__ import annotations

import shutil
from pathlib import Path


def install_asar(target_asar: Path, new_asar: Path) -> Path:
    """Copy new_asar over target; keep target.asar.bak once."""
    target_asar = target_asar.resolve()
    new_asar = new_asar.resolve()
    if not new_asar.is_file():
        raise FileNotFoundError(new_asar)
    bak = target_asar.with_suffix(target_asar.suffix + ".bak")
    if target_asar.is_file() and not bak.exists():
        shutil.copy2(target_asar, bak)
    shutil.copy2(new_asar, target_asar)
    return bak


def restore_asar(target_asar: Path) -> None:
    bak = target_asar.with_suffix(target_asar.suffix + ".bak")
    if not bak.is_file():
        raise FileNotFoundError(f"no backup at {bak}")
    shutil.copy2(bak, target_asar)
