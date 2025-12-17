# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Simple JSONL audit logging for configuration and control-plane events."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AUDIT_FILE = Path.home() / ".unsloth" / "studio" / "audit.log.jsonl"


def write_audit_event(action: str, actor: str, details: dict[str, Any]) -> None:
    AUDIT_FILE.parent.mkdir(parents = True, exist_ok = True)
    payload = {
        "timestamp": datetime.now(tz = timezone.utc).isoformat(),
        "action": action,
        "actor": actor,
        "details": details,
    }
    with AUDIT_FILE.open("a", encoding = "utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii = False) + "\n")
