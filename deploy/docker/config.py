"""Environment-based configuration. Single source of truth for all settings."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache


def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()


@dataclass(frozen=True)
class Settings:
    app_root: str = field(default_factory=lambda: _env("PLEX_LINKER", ""))
    config_archives: str = field(default_factory=lambda: _env("CONFIG_ARCHIVES", ""))
    media_root: str = field(
        default_factory=lambda: _env("MEDIA_ROOT") or _env("DOCKER_MEDIA_PATH") or _env("HOST_MEDIA_PATH", "")
    )
    docker_media_path: str = field(default_factory=lambda: _env("DOCKER_MEDIA_PATH", ""))

    database_url: str = field(default_factory=lambda: _env("DATABASE_URL", ""))

    sonarr_url: str = field(default_factory=lambda: _env("SONARR_0_URL") or _env("SONARR_URL"))
    sonarr_api_path: str = field(
        default_factory=lambda: _env("SONARR_0_API_PATH") or _env("SONARR_API_PATH") or "/api/v3"
    )
    sonarr_api_key: str = field(default_factory=lambda: _env("SONARR_0_API_KEY") or _env("SONARR_API_KEY"))
    sonarr_root_path_prefix: str = field(default_factory=lambda: _env("SONARR_ROOT_PATH_PREFIX", "/"))

    radarr_url: str = field(default_factory=lambda: _env("RADARR_0_URL") or _env("RADARR_URL"))
    radarr_api_path: str = field(
        default_factory=lambda: _env("RADARR_0_API_PATH") or _env("RADARR_API_PATH") or "/api/v3"
    )
    radarr_api_key: str = field(default_factory=lambda: _env("RADARR_0_API_KEY") or _env("RADARR_API_KEY"))

    scan_interval_minutes: int = field(
        default_factory=lambda: int(_env("PLEX_LINKER_SCAN_INTERVAL_MINUTES", "15"))
    )

    @property
    def sonarr_api_base(self) -> str:
        if not self.sonarr_url:
            return ""
        path = self.sonarr_api_path if self.sonarr_api_path.startswith("/") else f"/{self.sonarr_api_path}"
        return f"{self.sonarr_url.rstrip('/')}{path}"

    @property
    def radarr_api_base(self) -> str:
        if not self.radarr_url:
            return ""
        path = self.radarr_api_path if self.radarr_api_path.startswith("/") else f"/{self.radarr_api_path}"
        return f"{self.radarr_url.rstrip('/')}{path}"

    @property
    def use_db(self) -> bool:
        return bool(self.database_url)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
