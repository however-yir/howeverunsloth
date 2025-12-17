# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""Shared application errors and API error responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


@dataclass(frozen = True)
class AppErrorCode:
    code: str
    message: str
    status_code: int


CONFIG_INVALID = AppErrorCode(
    code = "CONFIG_INVALID",
    message = "Project configuration is invalid",
    status_code = 422,
)
CONFIG_UPDATE_FORBIDDEN = AppErrorCode(
    code = "CONFIG_UPDATE_FORBIDDEN",
    message = "Configuration update is forbidden in this environment",
    status_code = 403,
)
QUOTA_EXCEEDED = AppErrorCode(
    code = "QUOTA_EXCEEDED",
    message = "Tenant quota exceeded",
    status_code = 429,
)
INTERNAL_ERROR = AppErrorCode(
    code = "INTERNAL_ERROR",
    message = "Internal server error",
    status_code = 500,
)


class AppError(Exception):
    def __init__(self, error: AppErrorCode, details: Any = None):
        super().__init__(error.message)
        self.error = error
        self.details = details


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError):
        payload = {
            "error": {
                "code": exc.error.code,
                "message": exc.error.message,
                "details": exc.details,
            }
        }
        return JSONResponse(status_code = exc.error.status_code, content = payload)

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception):
        payload = {
            "error": {
                "code": INTERNAL_ERROR.code,
                "message": INTERNAL_ERROR.message,
                "details": str(exc),
            }
        }
        return JSONResponse(status_code = INTERNAL_ERROR.status_code, content = payload)
