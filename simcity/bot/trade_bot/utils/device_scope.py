"""Per-device identifiers for concurrent trade-bot sessions (N cities / N ADB devices)."""

from __future__ import annotations

import re


def device_id_slug(device_id: str) -> str:
    """Filesystem- and timer-key-safe token for ``device_id`` (e.g. ADB port ``5554``)."""
    s = str(device_id).strip()
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "_", s)
    return cleaned or "device"


def global_trade_hq_timer_key(device_id: str) -> str:
    """TimerManager key unique per device so N sessions do not share one HQ timer."""
    return f"global_trade_hq_timer_{device_id_slug(device_id)}"
