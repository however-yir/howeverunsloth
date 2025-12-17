# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Generic retry policy for long-running training/export jobs."""

from __future__ import annotations

import random
import time
from typing import Callable, TypeVar


T = TypeVar("T")


def with_retry(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
) -> T:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - caller controls retry surface
            last_error = exc
            if attempt >= max_attempts:
                break
            sleep_s = min(max_delay, base_delay * (2 ** (attempt - 1)))
            sleep_s *= 1.0 + random.random() * 0.2
            time.sleep(sleep_s)
    assert last_error is not None
    raise last_error
