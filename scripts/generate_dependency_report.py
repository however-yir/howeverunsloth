#!/usr/bin/env python3
"""Generate dependency report JSON for weekly archival."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> dict:
    proc = subprocess.run(cmd, cwd = cwd, capture_output = True, text = True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = {
        "generated_at": datetime.now(tz = timezone.utc).isoformat(),
        "python": run(["python3", "-m", "pip", "list", "--outdated", "--format=json"]),
        "npm": run(["npm", "outdated", "--json"], cwd = root / "studio" / "frontend"),
    }

    out = root / "reports" / "dependency-report.json"
    out.parent.mkdir(parents = True, exist_ok = True)
    out.write_text(json.dumps(report, ensure_ascii = False, indent = 2), encoding = "utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
