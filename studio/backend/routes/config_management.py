# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Configuration, quota and control-plane management APIs."""

from __future__ import annotations

import os
import json
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter

from core.audit import AUDIT_FILE, write_audit_event
from core.errors import AppError, CONFIG_INVALID, CONFIG_UPDATE_FORBIDDEN, QUOTA_EXCEEDED
from core.events import event_bus
from core.inference.provider_router import route_provider
from core.project_profile import (
    clear_project_profile_cache,
    get_project_profile,
    get_public_profile_dict,
    validate_project_profile,
)
from core.tenant_quota import tenant_quota_manager
from models.config_management import (
    ConfigUpdateRequest,
    ProviderRouteRequest,
    TenantQuotaRequest,
)

router = APIRouter()


@router.get("/profile")
def get_profile():
    return get_public_profile_dict(get_project_profile())


@router.get("/validate")
def validate_profile():
    result = validate_project_profile(get_project_profile())
    if not result.ok:
        raise AppError(CONFIG_INVALID, {"errors": list(result.errors)})
    return {"ok": True, "errors": []}


@router.post("/reload")
def reload_profile():
    clear_project_profile_cache()
    profile = get_project_profile()
    result = validate_project_profile(profile)
    if not result.ok:
        raise AppError(CONFIG_INVALID, {"errors": list(result.errors)})
    event_bus.publish("config.reloaded", {"project_name": profile.project_name})
    write_audit_event("config.reload", "system", {"project_name": profile.project_name})
    return {"ok": True, "profile": get_public_profile_dict(profile)}


@router.post("/update")
def update_profile(req: ConfigUpdateRequest):
    if os.getenv("HOWEVER_ALLOW_RUNTIME_CONFIG_UPDATE", "0") != "1":
        raise AppError(CONFIG_UPDATE_FORBIDDEN, "Set HOWEVER_ALLOW_RUNTIME_CONFIG_UPDATE=1 to enable")

    blocked = [k for k in req.updates if not k.startswith("HOWEVER_")]
    if blocked:
        raise AppError(CONFIG_UPDATE_FORBIDDEN, {"blocked_keys": blocked})

    for key, value in req.updates.items():
        os.environ[key] = value

    clear_project_profile_cache()
    profile = get_project_profile()
    result = validate_project_profile(profile)
    if not result.ok:
        raise AppError(CONFIG_INVALID, {"errors": list(result.errors)})

    event_bus.publish("config.updated", {"actor": req.actor, "keys": list(req.updates.keys())})
    write_audit_event("config.update", req.actor, {"keys": list(req.updates.keys())})
    return {"ok": True, "profile": get_public_profile_dict(profile)}


@router.post("/provider/route")
def route_model_provider(req: ProviderRouteRequest):
    route = route_provider(req.model_name, req.preferred_provider)
    return {
        "provider": route.provider,
        "base_url": route.base_url,
        "reason": route.reason,
    }


@router.get("/tenant/{tenant_id}/quota")
def quota_snapshot(tenant_id: str):
    return tenant_quota_manager.get_snapshot(tenant_id)


@router.post("/tenant/quota/consume")
def quota_consume(req: TenantQuotaRequest):
    if not tenant_quota_manager.check_and_consume_request(req.tenant_id):
        raise AppError(QUOTA_EXCEEDED, {"tenant_id": req.tenant_id, "dimension": "requests_per_minute"})
    if req.tokens and not tenant_quota_manager.check_and_consume_tokens(req.tenant_id, req.tokens):
        raise AppError(QUOTA_EXCEEDED, {"tenant_id": req.tenant_id, "dimension": "tokens_per_day"})
    return {"ok": True, "snapshot": tenant_quota_manager.get_snapshot(req.tenant_id)}


@router.get("/preflight")
def preflight_check():
    profile = get_project_profile()
    validation = validate_project_profile(profile)
    home = Path.home()
    disk = os.statvfs(str(home))
    free_gb = round((disk.f_bavail * disk.f_frsize) / (1024 ** 3), 2)
    return {
        "config_ok": validation.ok,
        "config_errors": list(validation.errors),
        "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "free_disk_gb": free_gb,
        "required_env": {
            "HF_TOKEN": bool(os.getenv("HF_TOKEN")),
            "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY")),
            "WANDB_API_KEY": bool(os.getenv("WANDB_API_KEY")),
        },
    }


@router.get("/audit/recent")
def recent_audit_events(limit: int = 30):
    if not AUDIT_FILE.exists():
        return {"events": []}
    rows = AUDIT_FILE.read_text(encoding = "utf-8").splitlines()
    tail = rows[-max(limit, 0) :]
    return {"events": tail}


@router.get("/data-recipe/market")
def recipe_market():
    market_file = Path(__file__).resolve().parents[1] / "assets" / "configs" / "data_recipe_market.json"
    if not market_file.exists():
        return {"items": []}
    return {"items": json.loads(market_file.read_text(encoding = "utf-8"))}


@router.get("/model-compare")
def model_compare(left: str, right: str):
    # Lightweight placeholder for dashboard integration.
    # Real metrics should come from benchmark pipelines.
    return {
        "left": left,
        "right": right,
        "summary": {
            "latency_ms": {"left": 0, "right": 0, "winner": "tbd"},
            "tokens_per_second": {"left": 0, "right": 0, "winner": "tbd"},
            "estimated_vram_gb": {"left": 0, "right": 0, "winner": "tbd"},
        },
        "generated_at": datetime.now(tz = timezone.utc).isoformat(),
    }


@router.post("/export/webhook-preview")
def export_webhook_preview(url: str, status: str = "completed"):
    payload = {
        "event": "export.status",
        "status": status,
        "target_url": url,
        "timestamp": datetime.now(tz = timezone.utc).isoformat(),
    }
    return {"ok": True, "payload": payload}
