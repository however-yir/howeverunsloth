# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Provider routing helper for OpenAI-compatible / Ollama / vLLM backends."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen = True)
class ProviderRoute:
    provider: str
    base_url: str
    reason: str


def route_provider(model_name: str, preferred: str | None = None) -> ProviderRoute:
    model = (model_name or "").lower()
    preferred_norm = (preferred or os.getenv("HOWEVER_PROVIDER_DEFAULT", "")).lower()

    if preferred_norm in {"openai", "ollama", "vllm"}:
        return _by_provider(preferred_norm, "preferred provider")

    if "/" in model and model.split("/", 1)[0] in {"openai", "gpt"}:
        return _by_provider("openai", "model namespace indicates OpenAI-compatible")

    if model.startswith("ollama:"):
        return _by_provider("ollama", "model prefix indicates Ollama")

    if any(tag in model for tag in ("gguf", "qwen", "llama", "mistral", "gemma")):
        # Local-first default.
        return _by_provider("ollama", "local model family routed to Ollama-compatible runtime")

    return _by_provider("openai", "fallback to OpenAI-compatible provider")


def _by_provider(provider: str, reason: str) -> ProviderRoute:
    if provider == "ollama":
        return ProviderRoute(
            provider = provider,
            base_url = os.getenv("HOWEVER_OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
            reason = reason,
        )
    if provider == "vllm":
        return ProviderRoute(
            provider = provider,
            base_url = os.getenv("HOWEVER_VLLM_BASE_URL", "http://127.0.0.1:8000"),
            reason = reason,
        )
    return ProviderRoute(
        provider = "openai",
        base_url = os.getenv("HOWEVER_OPENAI_BASE_URL", "https://api.openai.com/v1"),
        reason = reason,
    )
