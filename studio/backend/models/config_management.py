# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Schemas for project configuration management APIs."""

from pydantic import BaseModel, Field


class ProviderRouteRequest(BaseModel):
    model_name: str = Field(..., description = "Model identifier")
    preferred_provider: str | None = Field(
        default = None,
        description = "Optional preferred provider: openai / ollama / vllm",
    )


class ConfigUpdateRequest(BaseModel):
    actor: str = Field(default = "system", min_length = 1)
    updates: dict[str, str] = Field(
        default_factory = dict,
        description = "Environment-variable style updates; key must start with HOWEVER_",
    )


class TenantQuotaRequest(BaseModel):
    tenant_id: str = Field(..., min_length = 1)
    tokens: int = Field(default = 0, ge = 0)
