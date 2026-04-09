# SPDX-License-Identifier: AGPL-3.0-only

from core.project_profile import (
    ProjectProfile,
    validate_project_profile,
    get_public_profile_dict,
)


def test_validate_project_profile_ok():
    profile = ProjectProfile(
        project_name = "demo",
        project_display_name = "Demo",
        project_description = "desc",
        repo_description = "repo",
        github_topics = ("demo",),
        database_url = "sqlite:///tmp/demo.db",
        redis_url = "redis://127.0.0.1:6379/0",
        ollama_base_url = "http://127.0.0.1:11434",
        openai_base_url = "https://api.openai.com/v1",
    )
    result = validate_project_profile(profile)
    assert result.ok is True
    assert result.errors == ()


def test_validate_project_profile_invalid_scheme():
    profile = ProjectProfile(
        project_name = "demo",
        project_display_name = "Demo",
        project_description = "desc",
        repo_description = "repo",
        github_topics = (),
        database_url = "ftp://not-supported",
        redis_url = "redis://127.0.0.1:6379/0",
        ollama_base_url = "http:///missing-host",
        openai_base_url = "https://api.openai.com/v1",
    )
    result = validate_project_profile(profile)
    assert result.ok is False
    assert any("unsupported scheme" in e or "missing host" in e for e in result.errors)


def test_public_profile_masks_secrets():
    profile = ProjectProfile(
        project_name = "demo",
        project_display_name = "Demo",
        project_description = "desc",
        repo_description = "repo",
        github_topics = ("demo",),
        database_url = "postgresql://user:secret@localhost:5432/db",
        redis_url = "redis://:password@127.0.0.1:6379/0",
        ollama_base_url = "http://127.0.0.1:11434",
        openai_base_url = "https://api.openai.com/v1",
    )
    public = get_public_profile_dict(profile)
    assert "****" in public["database_url"]
    assert "****" in public["redis_url"]
