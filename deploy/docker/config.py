"""
Single source of truth for env-based config. API base URL = host URL + API path
so Sonarr/Radarr v3 work without hardcoding /api/v3.
"""
import os


def _get(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()


def _api_base(prefix: str, default_path: str = "/api/v3") -> str:
    """Build full API base URL: SONARR_0_URL + SONARR_0_API_PATH (default /api/v3)."""
    url = _get(f"{prefix}_0_URL") or _get(f"{prefix}_URL")
    if not url:
        return ""
    path = _get(f"{prefix}_0_API_PATH") or _get(f"{prefix}_API_PATH") or default_path
    path = path if path.startswith("/") else f"/{path}"
    return f"{url.rstrip('/')}{path}"


# --- App paths ---
def config_root() -> str:
    return _get("PLEX_LINKER", "")


def logs_dir() -> str:
    return _get("LOGS", "")


def config_archives() -> str:
    return _get("CONFIG_ARCHIVES", "")


def media_root() -> str:
    return _get("MEDIA_ROOT") or _get("DOCKER_MEDIA_PATH") or _get("HOST_MEDIA_PATH", "")


def docker_media_path() -> str:
    return _get("DOCKER_MEDIA_PATH", "")


# --- Sonarr (index 0 or legacy) ---
def sonarr_api_base() -> str:
    return _api_base("SONARR")


def sonarr_api_key() -> str:
    return _get("SONARR_0_API_KEY") or _get("SONARR_API_KEY")


def sonarr_root_path_prefix() -> str:
    return _get("SONARR_ROOT_PATH_PREFIX", "/")


# --- Radarr ---
def radarr_api_base() -> str:
    return _api_base("RADARR")


def radarr_api_key() -> str:
    return _get("RADARR_0_API_KEY") or _get("RADARR_API_KEY")


def database_url() -> str:
    """When set, app uses DB for rules/settings and serves the web UI."""
    return _get("DATABASE_URL", "")
