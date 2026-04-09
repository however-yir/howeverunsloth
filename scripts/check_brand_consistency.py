#!/usr/bin/env python3
"""Check whether disallowed branding strings still exist in custom docs/files."""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_PATHS = [
    Path("README.md"),
    Path("docs"),
    Path(".env.project.example"),
]

# Strings that should not appear in the customized project docs.
DISALLOWED = [
    "Autoware 平台",
    "如果你愿意",
    "如果你需要",
    "结论先说清楚",
    "狠狠稳住",
]


def iter_files(paths: list[Path]):
    for p in paths:
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".example", ""}:
                    yield f


def main() -> int:
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("paths", nargs = "*", help = "Files/directories to scan")
    args = parser.parse_args()

    scan_paths = [Path(p) for p in args.paths] if args.paths else DEFAULT_PATHS
    violations: list[tuple[Path, str, int]] = []

    for file in iter_files(scan_paths):
        try:
            text = file.read_text(encoding = "utf-8")
        except UnicodeDecodeError:
            continue
        for term in DISALLOWED:
            idx = text.find(term)
            if idx >= 0:
                violations.append((file, term, idx))

    if violations:
        for file, term, _ in violations:
            print(f"[FAIL] {file}: found disallowed term -> {term}")
        return 1

    print("Brand consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
