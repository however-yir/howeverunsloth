#!/usr/bin/env bash
set -euo pipefail

PROFILE_FILE="${1:-.env.project}"
HOST="${HOWEVER_STUDIO_HOST:-0.0.0.0}"
PORT="${HOWEVER_STUDIO_PORT:-8888}"

if [[ -f "$PROFILE_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$PROFILE_FILE"
  set +a
fi

python3 studio/backend/run.py --host "$HOST" --port "$PORT"
