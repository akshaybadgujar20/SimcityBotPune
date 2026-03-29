from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import cv2

if TYPE_CHECKING:
    from simcity.bot.trade_bot.config.defaults import TradeBotConfig

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def captures_root(config: Optional["TradeBotConfig"] = None) -> Path:
    from simcity.bot.trade_bot.utils.device_scope import device_id_slug

    if config is not None and config.captures_root_override is not None:
        base = Path(config.captures_root_override)
    else:
        base = _PACKAGE_ROOT / "captures"
    if config is not None and config.capture_device_id:
        return base / device_id_slug(config.capture_device_id)
    return base


def ensure_capture_subdir(config: Optional["TradeBotConfig"], *parts: str) -> Path:
    root = captures_root(config)
    path = root.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _slug(s: Optional[str]) -> str:
    if not s:
        return "na"
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", s.strip())
    return cleaned or "na"


def build_capture_name(
    session_id: Optional[str],
    phase: str,
    index: int,
    item_slug: Optional[str],
    kind: str,
) -> str:
    """``index`` is a trade-depot **view** (``hq``) or mayor-depot **page** (``depot``)."""
    sid = session_id or "nosession"
    prefix = "v" if phase == "hq" else "p"
    return f"{sid}_{phase}_{prefix}{index}_{kind}_{_slug(item_slug)}"


def _relative_parts(relative_dir: str) -> list[str]:
    return [p for p in relative_dir.replace("\\", "/").split("/") if p]


def save_scanned_image(
    image: Any,
    *,
    config: Optional["TradeBotConfig"],
    relative_dir: str,
    filename_stem: str,
    ext: str = ".png",
) -> Path:
    parts = _relative_parts(relative_dir)
    ensure_capture_subdir(config, *parts)
    root = captures_root(config)
    if not ext.startswith("."):
        ext = f".{ext}"
    full = root.joinpath(*parts, f"{filename_stem}{ext}")
    full.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(full), image)
    return full
