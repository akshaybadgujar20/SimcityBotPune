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
from simcity.bot.city_actions.buy_items import global_trade_hq_timer, manager
from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.services.city_depot_service import CityDepotService
from simcity.bot.trade_bot.services.detection_service import DetectionService
from simcity.bot.trade_bot.services.global_trade_service import GlobalTradeService
from simcity.bot.trade_bot.services.navigation_wrapper import NavigationWrapper

logger = logging.getLogger("trade_bot")


class TradeSessionState:
    """Tracks target names for an optional higher-level orchestration layer."""

    def __init__(self, purchase_items: list[PurchaseItem]) -> None:
        self._all_names: Set[str] = {p.name for p in purchase_items}

    @property
    def target_names(self) -> Set[str]:
        return set(self._all_names)


def _ensure_trade_hq_timer() -> None:
    manager.create_timer(global_trade_hq_timer, interval=1)


def _log_session_buy_totals(buy_counts: Dict[str, int]) -> None:
    parts = [f'"{name}": {buy_counts[name]}' for name in sorted(buy_counts.keys())]
    total = sum(buy_counts.values())
    logger.info(
        "Session buy totals after this iteration: %s (grand total: %s)",
        ", ".join(parts),
        total,
    )


def run_trade_session(
    device_id: str,
    purchase_items: Sequence[PurchaseItem],
    *,
    config: Optional[TradeBotConfig] = None,
    stop_event: Optional[Event] = None,
    max_session_iterations: int = 10_000,
) -> None:
    """
    Open the purchase menu and Global Trade HQ, refresh listings, and scan the
    trade depot: 1st view when HQ opens, then swipe right for the 2nd and 3rd views
    (count set by ``hq_trade_views``). Meant to be called from
    your API or a script.
    """
    cfg = config or TradeBotConfig()
    _ensure_trade_hq_timer()
    purchase_list = list(purchase_items)
    if not purchase_list:
        logger.info("Your shopping list is empty — nothing to do.")
        return
    purchase_by_name = {p.name: p for p in purchase_list}
    buy_counts: Dict[str, int] = {p.name: 0 for p in purchase_list}

    def stop_check() -> bool:
        return bool(stop_event and stop_event.is_set())

    ordered = sorted(purchase_list, key=lambda x: (x.priority, x.name))
    logger.info(
        "Starting a shopping run on your city (device %s). We’ll try up to %s full refresh cycles.",
        device_id,
        max_session_iterations,
    )
    logger.info(
        "You’re looking for %s item(s). Lower priority number = we try to get it first.",
        len(purchase_list),
    )
    for p in ordered:
        logger.info('  • "%s" (priority %s)', p.name, p.priority)

    detection = DetectionService(cfg)
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

    logger.info("Opening the purchase menu…")
    click_on_purchase_menu(device_id)
    logger.info("Pausing a second so the menu can appear…")
    time.sleep(1)
    logger.info("Opening Global Trade HQ (trade depot)…")
    click_on_global_trade_hq(device_id)

    for outer_i in range(max_session_iterations):
        if stop_check():
            logger.info("Stop requested — ending the shopping run (was on cycle %s).", outer_i + 1)
            return

        logger.info(
            "Cycle %s of %s: refreshing listings, then browsing the trade depot again.",
            outer_i + 1,
            max_session_iterations,
        )
        logger.info("Tapping Best Value so new offers can load…")
        click_on_best_value_menu(device_id)
        logger.info("Short pause while the game updates…")
        time.sleep(1)
        logger.info("Opening Global Trade HQ again…")
        click_on_global_trade_hq(device_id)
        logger.info("Waiting a moment for the trade screen to finish loading…")
        time.sleep(1)

        global_trade.scan_trade_depot_views_and_visit(
            purchase_list,
            purchase_by_name,
            stop_check=stop_check,
            apply_refresh_timer=True,
        )
        _log_session_buy_totals(buy_counts)
