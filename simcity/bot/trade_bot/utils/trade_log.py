from __future__ import annotations

import logging
from typing import Optional

_TRADE_BOT_LOGGER = "trade_bot"


def city_slug(device_id: Optional[str]) -> str:
    if device_id is None:
        return "unknown"
    return f"city_{device_id}"


def trade_log(
    device_id: Optional[str],
    phase: str,
    message: str,
    *args,
    level: int = logging.INFO,
) -> None:
    """Structured log line for continuous-buy workflow."""
    prefix = f"[CONTINUOUS_BUY][{phase}][{city_slug(device_id)}]"
    logger = logging.getLogger(_TRADE_BOT_LOGGER)
    if args:
        logger.log(level, "%s %s", prefix, message % args)
    else:
        logger.log(level, "%s %s", prefix, message)
