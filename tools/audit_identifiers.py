#!/usr/bin/env python3
"""
Content-safety audit for text-based game assets.

Scans a directory tree for offensive or disallowed identifiers/strings
and prints exact file:line references with short context. Intended for
pre-submission QA for Workshop/official-pool candidates.

Usage:
  python3 tools/audit_identifiers.py --root . --include ".vmf,.vmap,.nut,.lua,.cfg,.txt,.json,.xml,.kv,.kv3,.py,.js,.ts"

Notes:
- The default dictionary is intentionally small and conservative.
- You can extend via a file: --terms-file banned_terms.txt (one term per line).
- This tool does not modify files. It only reports.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import sys


DEFAULT_TERMS = [
    # core slur stems (case-insensitive); token-boundary matched where possible
    r"\bnigg[aer]\b",           # n-word variants
    r"\bkike\b",
    r"\bchink\b",
    r"\bspic\b",
    r"\bretard(ed|s)?\b",
    r"\bfag(got)?\b",
    r"\btrann(y|ie)\b",
]


def load_terms(path: Path | None) -> list[re.Pattern]:
    patterns: list[str] = []
    if path and path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            # treat as raw regex, otherwise escape word and add word boundaries
            if s.startswith("re:"):
                patterns.append(s[3:])
            else:
                patterns.append(rf"\b{re.escape(s)}\b")
    else:
        patterns.extend(DEFAULT_TERMS)
    return [re.compile(p, re.IGNORECASE) for p in patterns]


def looks_binary(chunk: bytes) -> bool:
    return b"\x00" in chunk


def scan_file(path: Path, patterns: list[re.Pattern]) -> list[tuple[int, str, str]]:
    """Returns list of (line_no, pattern, line_text)"""
    out = []
    try:
        with path.open("rb") as f:
            head = f.read(2048)
            if looks_binary(head):
                return out
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            for pat in patterns:
                if pat.search(line):
                    out.append((i, pat.pattern, line.strip()))
    except Exception as e:
        print(f"[warn] could not read {path}: {e}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Root directory to scan")
    ap.add_argument("--include", default=".vmf,.vmap,.nut,.lua,.cfg,.txt,.json,.xml,.kv,.kv3,.py,.js,.ts",
                    help="Comma-separated list of file extensions to include")
    ap.add_argument("--terms-file", type=str, default=None, help="Optional custom terms file")
    args = ap.parse_args()

    root = Path(args.root)
    allowed_ext = {s.strip().lower() for s in args.include.split(',') if s.strip()}
    patterns = load_terms(Path(args.terms_file) if args.terms_file else None)

    found = 0
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if p.suffix.lower() not in allowed_ext:
            continue
        matches = scan_file(p, patterns)
        if matches:
            for (ln, pat, text) in matches:
                print(f"{p}:{ln}: pattern={pat} :: {text}")
                found += 1

    if found:
        print(f"\n[FAIL] flagged {found} occurrence(s). Review and rename/remove before submission.")
        sys.exit(2)
    else:
        print("[OK] no flagged terms found in scanned text files.")


if __name__ == "__main__":
    main()

