"""Apply exact-string translation maps to extracted asar trees."""

from __future__ import annotations

import json
from pathlib import Path

SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".mp4",
    ".wasm",
    ".node",
    ".dll",
    ".exe",
    ".bin",
}


def load_map(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("locale map must be a JSON object of string → string")
    out: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, str) and k:
            out[k] = v
    return out


def apply_map(tree: Path, mapping: dict[str, str]) -> tuple[int, int]:
    """Replace exact substrings in text-ish files. Longest keys first.

    Returns (files_touched, replacements).
    """
    if not mapping:
        return 0, 0
    keys = sorted(mapping.keys(), key=len, reverse=True)
    files_touched = 0
    replacements = 0
    for path in tree.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        original = text
        for k in keys:
            if k in text:
                n = text.count(k)
                text = text.replace(k, mapping[k])
                replacements += n
        if text != original:
            path.write_text(text, encoding="utf-8")
            files_touched += 1
    return files_touched, replacements
