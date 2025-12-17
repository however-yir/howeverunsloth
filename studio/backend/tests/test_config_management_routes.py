# SPDX-License-Identifier: AGPL-3.0-only

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.errors import install_error_handlers

_MODULE_PATH = Path(__file__).resolve().parents[1] / "routes" / "config_management.py"
_SPEC = spec_from_file_location("config_management_route", _MODULE_PATH)
assert _SPEC and _SPEC.loader
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
router = _MODULE.router


def build_client() -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix = "/api/config")
    install_error_handlers(app)
    return TestClient(app)


def test_validate_endpoint_exists():
    client = build_client()
    response = client.get("/api/config/validate")
    assert response.status_code in {200, 422}


def test_provider_route_endpoint():
    client = build_client()
    response = client.post(
        "/api/config/provider/route",
        json = {"model_name": "qwen2.5", "preferred_provider": "ollama"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "ollama"


def test_quota_snapshot_endpoint():
    client = build_client()
    response = client.get("/api/config/tenant/demo/quota")
    assert response.status_code == 200
    assert response.json()["tenant_id"] == "demo"
