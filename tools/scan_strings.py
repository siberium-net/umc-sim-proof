#!/usr/bin/env python3
"""
Scan binary/text files (e.g., Source/Source2 map exports: .vpk, .vmap_c, .bsp, .nav) for ASCII/UTF-8 strings
and report lines containing given patterns. Useful if only compiled assets are available.

Usage:
  python3 tools/scan_strings.py --root /path/to/assets --ext .vpk,.vmap_c,.bsp,.nav --terms nigga,retard

Notes:
- This is a best-effort strings extractor; for exact decompilation use engine tools, but this is fast triage.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
from typing import Iterable


def iter_strings(data: bytes, min_len: int = 4) -> Iterable[str]:
    buf = []
    for b in data:
        if 32 <= b < 127 or b in (9, 10, 13):
            buf.append(chr(b))
        else:
            if len(buf) >= min_len:
                yield ''.join(buf)
            buf = []
    if len(buf) >= min_len:
        yield ''.join(buf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--ext', default='.vpk,.vmap_c,.bsp,.nav,.pak,.bin,.dat')
    ap.add_argument('--terms', required=True, help='Comma-separated search terms (case-insensitive)')
    ap.add_argument('--min-len', type=int, default=4)
    args = ap.parse_args()

    root = Path(args.root)
    exts = {e.strip().lower() for e in args.ext.split(',') if e.strip()}
    terms = [t.strip().lower() for t in args.terms.split(',') if t.strip()]

    hits = 0
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        try:
            data = p.read_bytes()
        except Exception:
            continue
        for s in iter_strings(data, args.min_len):
            sl = s.lower()
            if any(t in sl for t in terms):
                print(f"{p}: {s[:200]}")
                hits += 1
                break
    if hits:
        print(f"\n[HITS] {hits} file(s) matched.")
    else:
        print('[OK] No matches found.')


if __name__ == '__main__':
    main()

