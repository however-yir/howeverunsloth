#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8888}"

echo "[preflight] checking python"
python3 --version

echo "[preflight] checking required commands"
for cmd in python3 curl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "missing command: $cmd"
    exit 1
  fi
done

echo "[preflight] checking port $PORT"
if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "port $PORT is already in use"
  exit 1
fi

echo "[preflight] checking disk"
FREE_GB=$(python3 - <<'PY'
import os
st = os.statvfs(os.path.expanduser('~'))
print(round((st.f_bavail * st.f_frsize) / (1024**3), 2))
PY
)
echo "free disk: ${FREE_GB} GB"

echo "[preflight] checking backend import"
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path('studio/backend').resolve()))
import core.project_profile as p
print('project profile module OK:', p.get_project_profile().project_name)
PY

echo "preflight checks passed"
