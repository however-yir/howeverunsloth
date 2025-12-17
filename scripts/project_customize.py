#!/usr/bin/env python3
"""Batch customization helper for turning this repo into your own project."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".java",
    ".kt",
    ".kts",
    ".xml",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".gradle",
    ".properties",
    ".sh",
    ".bat",
    ".ps1",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".env",
    "",
}

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".pytest_cache",
}


@dataclass
class Replacement:
    old: str
    new: str


def _is_text_candidate(path: Path) -> bool:
    name = path.name
    if name in {"pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle"}:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if _is_text_candidate(path):
            yield path


def _safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding = "utf-8")
    except UnicodeDecodeError:
        return None


def _replace_tag(text: str, tag: str, old: str, new: str) -> str:
    pattern = re.compile(rf"(<{tag}>){re.escape(old)}(</{tag}>)")
    return pattern.sub(rf"\1{new}\2", text)


def main() -> int:
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("--root", default = ".", help = "Repository root")
    parser.add_argument("--old-name", help = "Old project name")
    parser.add_argument("--new-name", help = "New project name")
    parser.add_argument("--old-namespace", help = "Old package/namespace")
    parser.add_argument("--new-namespace", help = "New package/namespace")
    parser.add_argument("--old-group-id", help = "Old Maven groupId")
    parser.add_argument("--new-group-id", help = "New Maven groupId")
    parser.add_argument("--old-artifact-id", help = "Old Maven artifactId")
    parser.add_argument("--new-artifact-id", help = "New Maven artifactId")
    parser.add_argument(
        "--replace",
        action = "append",
        default = [],
        metavar = "OLD=NEW",
        help = "Additional literal replacement pair",
    )
    parser.add_argument("--dry-run", action = "store_true", help = "Preview only")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    replacements: list[Replacement] = []
    if args.old_name and args.new_name:
        replacements.append(Replacement(args.old_name, args.new_name))
    if args.old_namespace and args.new_namespace:
        replacements.append(Replacement(args.old_namespace, args.new_namespace))

    for item in args.replace:
        if "=" not in item:
            raise SystemExit(f"Invalid --replace pair: {item}")
        old, new = item.split("=", 1)
        replacements.append(Replacement(old, new))

    if not replacements and not any(
        [args.old_group_id and args.new_group_id, args.old_artifact_id and args.new_artifact_id]
    ):
        raise SystemExit("No replacement rules specified.")

    changed_files = 0
    changed_lines = 0

    for file_path in _iter_files(root):
        original = _safe_read(file_path)
        if original is None:
            continue

        updated = original
        for rule in replacements:
            updated = updated.replace(rule.old, rule.new)

        if args.old_group_id and args.new_group_id:
            updated = _replace_tag(updated, "groupId", args.old_group_id, args.new_group_id)
        if args.old_artifact_id and args.new_artifact_id:
            updated = _replace_tag(
                updated, "artifactId", args.old_artifact_id, args.new_artifact_id
            )

        if updated != original:
            changed_files += 1
            changed_lines += sum(
                1 for old_line, new_line in zip(original.splitlines(), updated.splitlines()) if old_line != new_line
            )
            if not args.dry_run:
                file_path.write_text(updated, encoding = "utf-8")
            rel = file_path.relative_to(root)
            print(f"updated: {rel}")

    mode = "[dry-run] " if args.dry_run else ""
    print(f"{mode}changed files: {changed_files}, changed lines (approx): {changed_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
