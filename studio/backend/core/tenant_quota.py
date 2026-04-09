# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""In-memory tenant quota manager."""

from __future__ import annotations

import os
from dataclasses import dataclass
from threading import Lock


@dataclass
class TenantQuota:
    max_requests_per_minute: int
    max_concurrent_jobs: int
    max_tokens_per_day: int


@dataclass
class TenantUsage:
    requests_in_current_window: int = 0
    concurrent_jobs: int = 0
    tokens_today: int = 0


class TenantQuotaManager:
    def __init__(self):
        self._lock = Lock()
        self._default_quota = TenantQuota(
            max_requests_per_minute = int(os.getenv("HOWEVER_QUOTA_REQ_PER_MIN", "120")),
            max_concurrent_jobs = int(os.getenv("HOWEVER_QUOTA_CONCURRENT_JOBS", "4")),
            max_tokens_per_day = int(os.getenv("HOWEVER_QUOTA_TOKENS_PER_DAY", "2000000")),
        )
        self._usage: dict[str, TenantUsage] = {}

    def _tenant_usage(self, tenant_id: str) -> TenantUsage:
        if tenant_id not in self._usage:
            self._usage[tenant_id] = TenantUsage()
        return self._usage[tenant_id]

    def check_and_consume_request(self, tenant_id: str) -> bool:
        with self._lock:
            usage = self._tenant_usage(tenant_id)
            if usage.requests_in_current_window >= self._default_quota.max_requests_per_minute:
                return False
            usage.requests_in_current_window += 1
            return True

    def check_and_consume_tokens(self, tenant_id: str, tokens: int) -> bool:
        with self._lock:
            usage = self._tenant_usage(tenant_id)
            if usage.tokens_today + max(tokens, 0) > self._default_quota.max_tokens_per_day:
                return False
            usage.tokens_today += max(tokens, 0)
            return True

    def try_start_job(self, tenant_id: str) -> bool:
        with self._lock:
            usage = self._tenant_usage(tenant_id)
            if usage.concurrent_jobs >= self._default_quota.max_concurrent_jobs:
                return False
            usage.concurrent_jobs += 1
            return True

    def finish_job(self, tenant_id: str) -> None:
        with self._lock:
            usage = self._tenant_usage(tenant_id)
            usage.concurrent_jobs = max(usage.concurrent_jobs - 1, 0)

    def reset_window(self) -> None:
        with self._lock:
            for usage in self._usage.values():
                usage.requests_in_current_window = 0

    def reset_day(self) -> None:
        with self._lock:
            for usage in self._usage.values():
                usage.tokens_today = 0

    def get_snapshot(self, tenant_id: str) -> dict:
        with self._lock:
            usage = self._tenant_usage(tenant_id)
            quota = self._default_quota
            return {
                "tenant_id": tenant_id,
                "quota": quota.__dict__,
                "usage": usage.__dict__,
            }


tenant_quota_manager = TenantQuotaManager()
