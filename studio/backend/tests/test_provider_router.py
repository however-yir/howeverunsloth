# SPDX-License-Identifier: AGPL-3.0-only

from core.inference.provider_router import route_provider


def test_route_provider_ollama_by_prefix():
    route = route_provider("ollama:qwen2.5")
    assert route.provider == "ollama"


def test_route_provider_openai_by_namespace():
    route = route_provider("openai/gpt-oss-20b")
    assert route.provider == "openai"


def test_route_provider_preferred_overrides():
    route = route_provider("qwen2.5", preferred = "vllm")
    assert route.provider == "vllm"
