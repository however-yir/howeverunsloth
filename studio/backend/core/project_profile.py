# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026-present the Unsloth AI Inc. team. All rights reserved. See /studio/LICENSE.AGPL-3.0

"""
Centralized project-level branding and deployment profile.

This keeps "make it my own project" settings in one place so startup banner,
health checks, and docs can use the same values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen = True)
class ProjectProfile:
    project_name: str
    project_display_name: str
    project_description: str
    repo_description: str
    github_topics: tuple[str, ...]
    database_url: str
    redis_url: str
    ollama_base_url: str
    openai_base_url: str


@dataclass(frozen = True)
class ProfileValidationResult:
    ok: bool
    errors: tuple[str, ...]


def _env(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    return value if value else default


def _topics(raw: str) -> tuple[str, ...]:
    parts = []
    for chunk in raw.replace(" ", ",").split(","):
        item = chunk.strip().lower()
        if item:
            parts.append(item)
    # keep order and remove duplicates
    deduped = []
    seen = set()
    for item in parts:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return tuple(deduped)


def _mask_url_secret(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return url

    # Non-URL strings (like sqlite:///...) still return a parsed object;
    # only mask when auth credentials exist.
    if "@" not in parsed.netloc:
        return url

    creds, host = parsed.netloc.rsplit("@", 1)
    if ":" in creds:
        username, _ = creds.split(":", 1)
        safe_netloc = f"{username}:****@{host}" if username else f"****@{host}"
    else:
        safe_netloc = f"{creds}@{host}"
    return urlunsplit((parsed.scheme, safe_netloc, parsed.path, parsed.query, parsed.fragment))


def _normalize_sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///~/"):
        return "sqlite:///" + str(os.path.expanduser(url[len("sqlite:///") :]))
    return url


def _validate_url(name: str, value: str, allowed_schemes: tuple[str, ...]) -> list[str]:
    value = value.strip()
    if not value:
        return [f"{name} is empty"]
    parsed = urlsplit(value)
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        return [f"{name} uses unsupported scheme '{parsed.scheme}'"]
    if parsed.scheme in {"http", "https", "redis"} and not parsed.netloc:
        return [f"{name} is missing host"]
    return []


@lru_cache(maxsize = 1)
def get_project_profile() -> ProjectProfile:
    return ProjectProfile(
        project_name = _env("HOWEVER_PROJECT_NAME", "howeverunsloth"),
        project_display_name = _env("HOWEVER_PROJECT_DISPLAY_NAME", "HoweverUnsloth Studio"),
        project_description = _env(
            "HOWEVER_PROJECT_DESCRIPTION",
            "面向私有化部署的本地模型训练与推理平台",
        ),
        repo_description = _env(
            "HOWEVER_REPO_DESCRIPTION",
            "私有化模型训练、推理与数据配方平台（基于 Unsloth 二次工程化）",
        ),
        github_topics = _topics(
            _env(
                "HOWEVER_GITHUB_TOPICS",
                "llm,finetuning,inference,ollama,local-llm,however",
            )
        ),
        database_url = _normalize_sqlite_url(
            _env(
            "HOWEVER_DATABASE_URL",
            "sqlite:///~/.howeverunsloth/studio/studio.db",
            )
        ),
        redis_url = _env("HOWEVER_REDIS_URL", "redis://127.0.0.1:6379/0"),
        ollama_base_url = _env("HOWEVER_OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        openai_base_url = _env("HOWEVER_OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def validate_project_profile(profile: ProjectProfile | None = None) -> ProfileValidationResult:
    p = profile or get_project_profile()
    errors: list[str] = []
    errors.extend(_validate_url("HOWEVER_DATABASE_URL", p.database_url, ("sqlite", "postgresql", "mysql", "mariadb")))
    errors.extend(_validate_url("HOWEVER_REDIS_URL", p.redis_url, ("redis", "rediss")))
    errors.extend(_validate_url("HOWEVER_OLLAMA_BASE_URL", p.ollama_base_url, ("http", "https")))
    errors.extend(_validate_url("HOWEVER_OPENAI_BASE_URL", p.openai_base_url, ("http", "https")))
    if not p.github_topics:
        errors.append("HOWEVER_GITHUB_TOPICS must contain at least one topic")
    return ProfileValidationResult(ok = len(errors) == 0, errors = tuple(errors))


def clear_project_profile_cache() -> None:
    get_project_profile.cache_clear()


def get_public_profile_dict(profile: ProjectProfile | None = None) -> dict:
    p = profile or get_project_profile()
    return {
        "project_name": p.project_name,
        "project_display_name": p.project_display_name,
        "project_description": p.project_description,
        "repo_description": p.repo_description,
        "github_topics": list(p.github_topics),
        "database_url": _mask_url_secret(p.database_url),
        "redis_url": _mask_url_secret(p.redis_url),
        "ollama_base_url": _mask_url_secret(p.ollama_base_url),
        "openai_base_url": _mask_url_secret(p.openai_base_url),
    }
