# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Tiny in-process event bus for orchestration and audit hooks."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._subscribers[topic].append(handler)

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        for handler in self._subscribers.get(topic, []):
            handler(payload)


event_bus = EventBus()
