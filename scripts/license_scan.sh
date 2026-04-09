#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT_DIR/reports"
mkdir -p "$REPORT_DIR"

echo "[Python licenses]"
if command -v pip-licenses >/dev/null 2>&1; then
  pip-licenses --format=json > "$REPORT_DIR/python-licenses.json"
  echo "wrote $REPORT_DIR/python-licenses.json"
else
  echo "pip-licenses not found; skipping python license scan"
fi

echo "[Frontend licenses]"
if command -v npx >/dev/null 2>&1; then
  (cd "$ROOT_DIR/studio/frontend" && npx --yes license-checker --json > "$REPORT_DIR/frontend-licenses.json" || true)
  echo "wrote $REPORT_DIR/frontend-licenses.json (if license-checker succeeded)"
else
  echo "npx not found; skipping frontend license scan"
fi
