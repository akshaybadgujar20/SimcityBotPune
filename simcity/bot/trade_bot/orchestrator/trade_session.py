from __future__ import annotations

import logging
import time
from threading import Event
from typing import Dict, Optional, Sequence, Set

from simcity.bot.automation.city_utility_actions import (
    click_on_best_value_menu,
    click_on_global_trade_hq,
    click_on_purchase_menu,
)
from simcity.bot.main import manager
from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.services.city_depot_service import CityDepotService
from simcity.bot.trade_bot.services.detection_service import DetectionService
from simcity.bot.trade_bot.services.global_trade_service import GlobalTradeService
from simcity.bot.trade_bot.services.navigation_wrapper import NavigationWrapper
from simcity.bot.trade_bot.utils.device_scope import global_trade_hq_timer_key
from simcity.bot.trade_bot.utils.trade_log import trade_log

logger = logging.getLogger("trade_bot")


class TradeSessionState:
    """Tracks target names for an optional higher-level orchestration layer."""

    def __init__(self, purchase_items: list[PurchaseItem]) -> None:
        self._all_names: Set[str] = {p.name for p in purchase_items}

    @property
    def target_names(self) -> Set[str]:
        return set(self._all_names)


def _ensure_trade_hq_timer(device_id: str) -> None:
    manager.create_timer(global_trade_hq_timer_key(device_id), interval=1)


def _log_session_buy_totals(device_id: str, buy_counts: Dict[str, int]) -> None:
    parts = [f'"{name}": {buy_counts[name]}' for name in sorted(buy_counts.keys())]
    total = sum(buy_counts.values())
    trade_log(
        device_id,
        "SESSION",
        "Cycle buy totals — %s (grand total: %s)",
        ", ".join(parts),
        total,
    )


def run_trade_session(
    device_id: str,
    purchase_items: Sequence[PurchaseItem],
    stop_event: Optional[Event] = None,
    *,
    config: Optional[TradeBotConfig] = None,
    max_session_iterations: int = 10_000,
) -> None:
    """
    Open the purchase menu and Global Trade HQ, refresh listings, and scan the
    trade depot across ``hq_trade_views`` pages per pass. Meant to be called from
    the API or a script.

    ``stop_event`` may be passed positionally (Flask ``start_action`` thread) or
    as a keyword argument.
    """
    cfg = config or TradeBotConfig()
    if cfg.capture_device_id is None:
        cfg.capture_device_id = device_id
    _ensure_trade_hq_timer(device_id)
    purchase_list = list(purchase_items)
    if not purchase_list:
        trade_log(device_id, "SESSION", "Shopping list empty — nothing to do")
        return
    purchase_by_name = {p.name: p for p in purchase_list}
    buy_counts: Dict[str, int] = {p.name: 0 for p in purchase_list}

    def stop_check() -> bool:
        return bool(stop_event and stop_event.is_set())

    ordered = sorted(purchase_list, key=lambda x: (x.priority, x.name))
    trade_log(
        device_id,
        "SESSION",
        "Session start — up to %s cycles, hq_trade_views=%s",
        max_session_iterations,
        cfg.hq_trade_views,
    )
    trade_log(
        device_id,
        "SESSION",
        "Shopping for %s item(s) in parallel on each HQ page",
        len(purchase_list),
    )
    for p in ordered:
        trade_log(device_id, "SESSION", '  • "%s" (list order %s)', p.name, p.priority)

    detection = DetectionService(cfg, device_id=device_id)
    navigation = NavigationWrapper(device_id)
    city_depot = CityDepotService(
        device_id, cfg, detection, navigation, buy_counts_by_item=buy_counts
    )
    global_trade = GlobalTradeService(
        device_id,
        cfg,
        detection,
        navigation,
        city_depot,
        buy_counts_by_item=buy_counts,
    )

    trade_log(device_id, "SESSION", "Opening purchase menu")
    click_on_purchase_menu(device_id)
    time.sleep(1)
    trade_log(device_id, "SESSION", "Opening Global Trade HQ")
    click_on_global_trade_hq(device_id)

    for outer_i in range(max_session_iterations):
        if stop_check():
            trade_log(
                device_id,
                "STOP",
                "Stop requested — ending session on cycle %s",
                outer_i + 1,
            )
            _log_session_buy_totals(device_id, buy_counts)
            return

        trade_log(
            device_id,
            "SESSION",
            "Cycle %s of %s — Best Value + reopen GTHQ",
            outer_i + 1,
            max_session_iterations,
        )
        click_on_best_value_menu(device_id)
        time.sleep(1)
        if stop_check():
            trade_log(device_id, "STOP", "Stop requested after Best Value tap")
            return
        click_on_global_trade_hq(device_id)
        time.sleep(1)

        global_trade.scan_trade_depot_views_and_visit(
            purchase_list,
            purchase_by_name,
            stop_check=stop_check,
            apply_refresh_timer=True,
        )
        _log_session_buy_totals(device_id, buy_counts)
