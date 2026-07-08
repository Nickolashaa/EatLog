import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import httpx

from ..config import GITHUB_REPO

_PACKAGE_NAME = "eat_log_desktop"


def current_version() -> str:
    """Version the app was built with, per pyproject.toml."""
    try:
        return version(_PACKAGE_NAME)
    except PackageNotFoundError:
        pass

    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        return str(data["project"]["version"])
    except OSError, KeyError, tomllib.TOMLDecodeError:
        return "0.0.0"


def latest_version() -> str | None:
    """Latest release tag on GitHub, or None if it can't be fetched."""
    try:
        response = httpx.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
            timeout=5.0,
            follow_redirects=True,
        )
        response.raise_for_status()
        tag = str(response.json()["tag_name"])
    except httpx.HTTPError, KeyError, ValueError:
        return None
    return tag.lstrip("vV")


def update_available() -> str | None:
    """Return the newer version string if an update is available, else None."""
    latest = latest_version()
    if latest is None:
        return None
    if latest.strip() == current_version().strip():
        return None
    return latest
