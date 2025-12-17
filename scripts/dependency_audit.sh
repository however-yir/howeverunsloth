#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

printf "[1/3] Python metadata quick check\n"
python3 - <<'PY'
from pathlib import Path
import tomllib
pp = Path("pyproject.toml")
if not pp.exists():
    print("pyproject.toml not found")
    raise SystemExit(0)
obj = tomllib.loads(pp.read_text(encoding="utf-8"))
project = obj.get("project", {})
print("project:", project.get("name"))
print("python:", project.get("requires-python"))
print("dependencies:", len(project.get("dependencies", [])))
PY

printf "\n[2/3] Frontend dependency report\n"
if command -v npm >/dev/null 2>&1; then
  (cd "$ROOT_DIR/studio/frontend" && npm outdated || true)
else
  echo "npm not found, skip frontend outdated check"
fi

printf "\n[3/3] Suggested upgrade workflow\n"
cat <<'SUGGEST'
1. Review breaking changes for runtime-critical libs (react/vite/fastapi/torch stack)
2. Upgrade in batches (infra deps -> ui deps -> tooling deps)
3. Run tests and smoke checks after each batch
4. Record rollback point with git tag before production deploy
SUGGEST
