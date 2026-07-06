from __future__ import annotations

import logging
import time
from typing import Callable, MutableMapping, Optional, Sequence

from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.city_actions.buy_items import (
    buy_item_from_visiting_city_trade_depot,
    manager,
)
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.automation.find_material import find_miscellaneous_material

from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.material_facade import material_facade_for
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.services.city_depot_service import CityDepotService
from simcity.bot.trade_bot.services.detection_service import DetectionService
from simcity.bot.trade_bot.services.navigation_wrapper import NavigationWrapper
from simcity.bot.trade_bot.utils.device_scope import global_trade_hq_timer_key
from simcity.bot.trade_bot.utils.trade_log import trade_log

logger = logging.getLogger("trade_bot")


def _sleep_interruptible(
    seconds: float,
    stop_check: Optional[Callable[[], bool]],
    device_id: str,
    *,
    reason: str,
) -> bool:
    """Sleep up to ``seconds``, checking ``stop_check`` every second. Returns False if stopped."""
    if seconds <= 0:
        return True
    trade_log(device_id, "TIMER", "Waiting %.1f seconds — %s", seconds, reason)
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if stop_check and stop_check():
            trade_log(device_id, "STOP", "Stop requested — ending wait early (%s)", reason)
            return False
        time.sleep(min(1.0, deadline - time.monotonic()))
    return True


class GlobalTradeService:
    def __init__(
        self,
        device_id: str,
        config: TradeBotConfig,
        detection: DetectionService,
        navigation: NavigationWrapper,
        city_depot: CityDepotService,
        *,
        buy_counts_by_item: Optional[MutableMapping[str, int]] = None,
    ) -> None:
        self._device_id = device_id
        self._config = config
        self._detection = detection
        self._nav = navigation
        self._city_depot = city_depot
        self._buy_counts = buy_counts_by_item
        self._hq_timer_key = global_trade_hq_timer_key(device_id)

    def _record_buy(self, item_name: str) -> None:
        if self._buy_counts is None:
            return
        self._buy_counts[item_name] = self._buy_counts.get(item_name, 0) + 1

    def wait_until_hq_ready(self, stop_check: Optional[Callable[[], bool]] = None) -> bool:
        manager.reset_timer(self._hq_timer_key)
        interval = max(0.05, self._config.hq_coin_poll_interval_seconds)
        max_attempts = max(1, self._config.hq_coin_max_poll_attempts)
        trade_log(
            self._device_id,
            "HQ",
            "Waiting for coin offers (HQ view ready signal)…",
        )
        for attempt in range(1, max_attempts + 1):
            if stop_check and stop_check():
                trade_log(self._device_id, "STOP", "Stop requested while waiting for HQ ready")
                return False
            coin, _ = find_miscellaneous_material(
                Miscellaneous.COIN,
                self._device_id,
                log_empty_match=False,
            )
            if len(coin) > 0:
                manager.start_timer(self._hq_timer_key)
                trade_log(self._device_id, "HQ", "Coin offers visible — HQ view ready")
                return True
            if attempt in (1, max_attempts) or (
                max_attempts > 5 and attempt in (5, 10)
            ):
                trade_log(
                    self._device_id,
                    "HQ",
                    "HQ still loading — retry in %.2fs (attempt %s of %s)",
                    interval,
                    attempt,
                    max_attempts,
                )
            if attempt < max_attempts:
                time.sleep(interval)
        trade_log(
            self._device_id,
            "HQ",
            "No coin offers after %s checks — HQ may be empty or still loading",
            max_attempts,
        )
        return False

    def _pick_on_current_page(
        self,
        items_list: list[PurchaseItem],
        view_index: int,
        stop_check: Optional[Callable[[], bool]],
    ):
        screenshot = take_bw_screenshot(self._device_id)
        detected = self._detection.detect_parallel_hq(
            items_list,
            screenshot,
            stop_check,
            view_index=view_index,
        )
        return self._detection.pick_first_by_screen_position(detected)

    def _visit_depot_for_hit(
        self,
        hit_item: PurchaseItem,
        hit_rect: list[int],
        items_list: list[PurchaseItem],
        purchase_by_name: dict[str, PurchaseItem],
        stop_check: Optional[Callable[[], bool]],
    ) -> bool:
        facade = material_facade_for(hit_item)
        trade_log(
            self._device_id,
            "DEPOT",
            'Entering mayor depot for "%s" (HQ listing click)',
            hit_item.name,
        )
        buy_item_from_visiting_city_trade_depot(
            facade, [hit_rect], self._device_id
        )
        self._record_buy(hit_item.name)

        others = {p.name for p in items_list} - {hit_item.name}
        if others:
            trade_log(
                self._device_id,
                "DEPOT",
                "Sweeping depot for other requested items: %s",
                ", ".join(sorted(others)),
            )
            self._city_depot.sweep_depot_for_targets(
                others, purchase_by_name, stop_check
            )
        else:
            trade_log(
                self._device_id,
                "DEPOT",
                "No other items from shopping list to check in this depot",
            )

        trade_log(self._device_id, "NAV", "Leaving mayor depot — returning to Global Trade HQ")
        self._city_depot.return_to_global_trade_hq(stop_check)
        return not (stop_check and stop_check())

    def scan_trade_depot_views_and_visit(
        self,
        purchase_items: Sequence[PurchaseItem],
        purchase_by_name: dict[str, PurchaseItem],
        stop_check: Optional[Callable[[], bool]] = None,
        apply_refresh_timer: bool = True,
    ) -> None:
        if not purchase_items:
            trade_log(self._device_id, "HQ", "Shopping list empty — skipping HQ scan")
            return

        items_list = list(purchase_items)
        num_views = self._config.hq_trade_views
        item_names = ", ".join(p.name for p in items_list)
        pass_started_monotonic = time.monotonic()
        hq_pass_started_monotonic: Optional[float] = None

        trade_log(
            self._device_id,
            "HQ",
            "HQ pass start — scanning pages 1..%s for: %s",
            num_views,
            item_names,
        )

        view_index = 0
        while view_index < num_views:
            if stop_check and stop_check():
                trade_log(self._device_id, "STOP", "Stop requested during HQ pass")
                return

            if view_index == 0:
                if not self.wait_until_hq_ready(stop_check):
                    trade_log(
                        self._device_id,
                        "HQ",
                        "Could not confirm HQ ready — treating as empty pass",
                    )
                    if not self._wait_hq_empty_pass_budget(
                        pass_started_monotonic,
                        stop_check,
                        lead_in="HQ not ready",
                    ):
                        return
                    return
                hq_pass_started_monotonic = time.monotonic()
            else:
                trade_log(
                    self._device_id,
                    "HQ",
                    "Page %s/%s — pausing %.1fs after swipe",
                    view_index + 1,
                    num_views,
                    self._config.swipe_after_seconds,
                )
                time.sleep(self._config.swipe_after_seconds)

            trade_log(
                self._device_id,
                "HQ",
                "Page %s/%s — scanning for: %s",
                view_index + 1,
                num_views,
                item_names,
            )

            while True:
                if stop_check and stop_check():
                    trade_log(self._device_id, "STOP", "Stop requested during page scan")
                    return

                choice = self._pick_on_current_page(items_list, view_index, stop_check)
                if choice is None:
                    trade_log(
                        self._device_id,
                        "HQ",
                        "Page %s/%s — no more matches on this page",
                        view_index + 1,
                        num_views,
                    )
                    break

                hit_item, hit_rect = choice
                if not self._visit_depot_for_hit(
                    hit_item,
                    hit_rect,
                    items_list,
                    purchase_by_name,
                    stop_check,
                ):
                    return

                trade_log(
                    self._device_id,
                    "HQ",
                    "Page %s/%s — rescan after depot visit",
                    view_index + 1,
                    num_views,
                )
                self._nav.navigate_to_hq_view(view_index, self._config)
                time.sleep(1)

            if view_index < num_views - 1:
                trade_log(
                    self._device_id,
                    "HQ",
                    "Page %s/%s clear — swiping to page %s",
                    view_index + 1,
                    num_views,
                    view_index + 2,
                )
                self._nav.swipe_trade_depot_next_view(self._config)
                view_index += 1
                continue

            trade_log(
                self._device_id,
                "HQ",
                "Page %s/%s — last page of this pass",
                view_index + 1,
                num_views,
            )
            break

        elapsed = (
            time.monotonic() - hq_pass_started_monotonic
            if hq_pass_started_monotonic is not None
            else 0.0
        )
        trade_log(
            self._device_id,
            "HQ",
            "HQ pass complete — scanned all %s pages in %.1fs",
            num_views,
            elapsed,
        )

        if apply_refresh_timer:
            anchor = hq_pass_started_monotonic or pass_started_monotonic
            if not self._wait_hq_empty_pass_budget(
                anchor,
                stop_check,
                lead_in="HQ pass finished — refresh window",
            ):
                return

    def _wait_hq_empty_pass_budget(
        self,
        pass_started_monotonic: float,
        stop_check: Optional[Callable[[], bool]],
        *,
        lead_in: str,
    ) -> bool:
        """
        Sleep until ``hq_empty_pass_wait_seconds`` budget from ``pass_started_monotonic`` is used.
        Returns False if ``stop_check`` aborts the wait.
        """
        budget = self._config.hq_empty_pass_wait_seconds
        if budget <= 0:
            return True
        elapsed = time.monotonic() - pass_started_monotonic
        remaining = max(0.0, budget - elapsed)
        trade_log(
            self._device_id,
            "TIMER",
            "%s — waiting %.1fs more (%.0fs window, %.1fs elapsed)",
            lead_in,
            remaining,
            budget,
            elapsed,
        )
        if remaining <= 0:
            return True
        return _sleep_interruptible(
            remaining,
            stop_check,
            self._device_id,
            reason="Pausing before next Best Value / HQ refresh cycle",
        )
