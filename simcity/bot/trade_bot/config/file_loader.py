from __future__ import annotations

import json
import logging
from dataclasses import fields
from pathlib import Path
from threading import Event
from typing import Any, Mapping, Optional, Union

from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.purchase_item import (
    PurchaseItem,
    purchase_items_from_specs,
)

PathLike = Union[str, Path]
logger = logging.getLogger("trade_bot")


def _load_json_or_yaml(path: Path) -> Any:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError(
                "Install PyYAML to load .yaml/.yml files: pip install pyyaml"
            ) from e
        return yaml.safe_load(text)
    return json.loads(text)


def load_trade_bot_config(path: PathLike) -> TradeBotConfig:
    """
    Load bot settings from a JSON or YAML file.

    Root must be an object. Unknown keys are ignored.
    ``captures_root_override`` may be a string path.
    Omit ``capture_session_id`` to auto-generate one.
    """
    p = Path(path)
    data = _load_json_or_yaml(p)
    if not isinstance(data, dict):
        raise ValueError("Config file must start with a JSON/YAML object `{ ... }`, not a list.")
    allowed = {f.name for f in fields(TradeBotConfig)}
    kwargs: dict[str, Any] = {}
    for key, value in data.items():
        if key not in allowed:
            continue
        if key == "captures_root_override" and value is not None:
            kwargs[key] = Path(str(value))
        else:
            kwargs[key] = value
    if "hq_trade_views" not in kwargs and "max_hq_pages" in data:
        try:
            kwargs["hq_trade_views"] = int(data["max_hq_pages"])
        except (TypeError, ValueError):
            pass
    if "hq_empty_pass_wait_seconds" not in kwargs and "hq_carousel_empty_wait_seconds" in data:
        try:
            kwargs["hq_empty_pass_wait_seconds"] = float(
                data["hq_carousel_empty_wait_seconds"]
            )
        except (TypeError, ValueError):
            pass
    return TradeBotConfig(**kwargs)


def load_purchase_items_file(path: PathLike) -> list[PurchaseItem]:
    """
    Load purchase rows from JSON or YAML.

    Accepts either:

    * A **list** of objects (``material``, ``priority``; optional ``name``, ``template_path``)
    * An **object** with key ``purchase_items`` containing that list
    """
    p = Path(path)
    data = _load_json_or_yaml(p)
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("purchase_items")
        if not isinstance(rows, list):
            raise ValueError(
                "Expected a list root, or an object with 'purchase_items': [ ... ]"
            )
    else:
        raise ValueError("Shopping list file must be a list or an object with a purchase_items array.")
    specs: list[Mapping[str, Any]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Each shopping list entry must be a `{ ... }` object (problem at index {i}).")
        specs.append(row)
    return purchase_items_from_specs(specs)


def run_trade_session_from_files(
    device_id: str,
    *,
    config_path: PathLike,
    purchase_items_path: PathLike,
    stop_event: Optional[Event] = None,
    max_session_iterations: int = 10_000,
) -> None:
    """
    Load config and purchase items from disk, then start a shopping run.
    """
    from simcity.bot.trade_bot.orchestrator.trade_session import run_trade_session

    logger.info(
        "Starting from your settings file and shopping list (device %s).",
        device_id,
    )
    logger.debug("Settings: %s | List: %s", Path(config_path).resolve(), Path(purchase_items_path).resolve())
    cfg = load_trade_bot_config(config_path)
    items = load_purchase_items_file(purchase_items_path)
    logger.info("Loaded %s item(s) from your shopping list file.", len(items))
    run_trade_session(
        device_id,
        items,
        config=cfg,
        stop_event=stop_event,
        max_session_iterations=max_session_iterations,
    )
