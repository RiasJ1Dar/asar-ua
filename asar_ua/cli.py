#!/usr/bin/env python3
"""asar-ua CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from asar_ua.apply import apply_map, load_map
from asar_ua.asar_format import pack_asar, unpack_asar
from asar_ua.install import install_asar, restore_asar


def main(argv: list[str] | None = None) -> int:
    # Help and status lines contain "→". A console or pipe in a legacy code page
    # (cp1251, cp866) cannot encode it and argparse crashes with
    # UnicodeEncodeError; print "?" instead of failing.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    p = argparse.ArgumentParser(prog="asar-ua", description="Electron asar locale patcher")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="Unpack app.asar to a directory")
    e.add_argument("asar")
    e.add_argument("out")

    a = sub.add_parser("apply", help="Apply JSON string map to an extracted tree")
    a.add_argument("tree")
    a.add_argument("map_json")

    pk = sub.add_parser("pack", help="Pack a directory into app.asar")
    pk.add_argument("tree")
    pk.add_argument("out_asar")

    i = sub.add_parser("install", help="Install patched asar (creates .bak once)")
    i.add_argument("target_asar")
    i.add_argument("new_asar")

    r = sub.add_parser("restore", help="Restore target from .bak")
    r.add_argument("target_asar")

    pipe = sub.add_parser(
        "patch",
        help="extract → apply map → pack (writes out_asar)",
    )
    pipe.add_argument("asar")
    pipe.add_argument("map_json")
    pipe.add_argument("out_asar")
    pipe.add_argument("--work", default=None, help="Work directory (default: temp beside out)")

    args = p.parse_args(argv)

    if args.cmd == "extract":
        unpack_asar(args.asar, args.out)
        print(f"extracted → {args.out}")
        return 0
    if args.cmd == "apply":
        mapping = load_map(Path(args.map_json))
        files, reps = apply_map(Path(args.tree), mapping)
        print(f"touched {files} files, {reps} replacements")
        return 0
    if args.cmd == "pack":
        pack_asar(args.tree, args.out_asar)
        print(f"packed → {args.out_asar}")
        return 0
    if args.cmd == "install":
        bak = install_asar(Path(args.target_asar), Path(args.new_asar))
        print(f"installed; backup {bak}")
        return 0
    if args.cmd == "restore":
        restore_asar(Path(args.target_asar))
        print("restored from .bak")
        return 0
    if args.cmd == "patch":
        out = Path(args.out_asar)
        work = Path(args.work) if args.work else out.parent / (out.stem + "_work")
        if work.exists():
            import shutil

            shutil.rmtree(work)
        work.mkdir(parents=True)
        unpack_asar(args.asar, str(work))
        mapping = load_map(Path(args.map_json))
        files, reps = apply_map(work, mapping)
        pack_asar(str(work), str(out))
        print(f"patch done: touched {files} files, {reps} replacements → {out}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
