from __future__ import annotations

import logging
import time
from typing import Callable, MutableMapping, Optional, Sequence

from simcity.bot.automation.city_utility_actions import (
    click_on_best_value_menu,
    click_on_global_trade_hq,
)
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

logger = logging.getLogger("trade_bot")


def _sleep_interruptible(
    seconds: float,
    stop_check: Optional[Callable[[], bool]],
    *,
    reason: str,
) -> bool:
    """Sleep up to ``seconds``, checking ``stop_check`` every second. Returns False if stopped."""
    if seconds <= 0:
        return True
    logger.info("Waiting %.0f seconds — %s", seconds, reason)
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if stop_check and stop_check():
            logger.info("Stop requested — ending the wait early.")
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
        logger.info(
            "Checking this trade depot view — waiting until coin offers show (so the view has rendered)…"
        )
        for attempt in range(1, max_attempts + 1):
            if stop_check and stop_check():
                logger.info("You asked to stop — canceling while waiting for the trade depot.")
                return False
            coin, _ = find_miscellaneous_material(
                Miscellaneous.COIN,
                self._device_id,
                log_empty_match=False,
            )
            if len(coin) > 0:
                manager.start_timer(self._hq_timer_key)
                logger.info("Coin offers visible — this trade depot view is ready to search.")
                return True
            if attempt in (1, max_attempts) or (
                max_attempts > 5 and attempt in (5, 10)
            ):
                logger.info(
                    "View still drawing… checking again in %.2fs (try %s of %s).",
                    interval,
                    attempt,
                    max_attempts,
                )
            if attempt < max_attempts:
                time.sleep(interval)
        logger.info(
            "No coin offers detected after %s checks — trade depot may be empty or still loading.",
            max_attempts,
        )
        return False

    def scan_trade_depot_views_and_visit(
        self,
        purchase_items: Sequence[PurchaseItem],
        purchase_by_name: dict[str, PurchaseItem],
        stop_check: Optional[Callable[[], bool]] = None,
        apply_refresh_timer: bool = True,
    ) -> None:
        if not purchase_items:
            logger.info("Nothing on your shopping list — skipping the trade depot.")
            return

        items_list = list(purchase_items)
        num_views = self._config.hq_trade_views
        need_wait_after_empty_depot_pass = False
        hq_pass_started_monotonic: Optional[float] = None
        view_index = 0
        pass_started_monotonic = time.monotonic()
        # Wall-clock start of the current trade-refresh window (1st HQ view coin-ready).
        hq_refresh_anchor_monotonic: Optional[float] = None

        while view_index < num_views:
            if stop_check and stop_check():
                logger.info("You asked to stop — leaving the trade depot.")
                return

            if not self.wait_until_hq_ready(stop_check):
                logger.info(
                    "Applying the usual %.0f s pause, then the next cycle will tap Best Value and open Global Trade HQ again.",
                    self._config.hq_empty_pass_wait_seconds,
                )
                if not self._wait_hq_empty_pass_budget(
                    pass_started_monotonic,
                    stop_check,
                    lead_in=(
                        "Couldn’t confirm coin offers on this trade depot view — treating it like an empty pass."
                    ),
                ):
                    return
                return

            if hq_pass_started_monotonic is None:
                hq_pass_started_monotonic = time.monotonic()

            if view_index == 0:
                hq_refresh_anchor_monotonic = time.monotonic()
                logger.info(
                    "Trade depot — 1st view (opens as soon as HQ loads). Searching for your items…"
                )
            elif view_index == 1:
                logger.info(
                    "Trade depot — 2nd view (after one swipe right from the 1st). Searching…"
                )
            else:
                logger.info(
                    "Trade depot — %s view (after swiping right again). Searching…",
                    _ordinal(view_index + 1),
                )

            screenshot = take_bw_screenshot(self._device_id)
            detected = self._detection.detect_parallel_hq(
                items_list,
                screenshot,
                stop_check,
                view_index=view_index,
            )
            flat = self._detection.flatten_sorted_by_priority(detected)
            deduped = self._detection.dedupe_cross_items(
                flat, self._config.dedup_iou_threshold
            )
            choice = self._detection.pick_highest_priority_hit(deduped)

            if choice is None:
                if view_index < num_views - 1:
                    logger.info(
                        "Nothing you need on the %s view — swiping right to the %s view.",
                        _ordinal(view_index + 1),
                        _ordinal(view_index + 2),
                    )
                    self._nav.swipe_trade_depot_next_view(self._config)
                    view_index += 1
                    continue
                need_wait_after_empty_depot_pass = True
                logger.info(
                    "Nothing on the %s view — that was the last trade depot view for this pass.",
                    _ordinal(view_index + 1),
                )
                break

            best_item, best_rect = choice
            need_wait_after_empty_depot_pass = False
            hq_pass_started_monotonic = None
            facade = material_facade_for(best_item)
            logger.info(
                'Found "%s" in the trade depot (one of your higher-priority wants). Visiting that mayor’s city…',
                best_item.name,
            )
            buy_item_from_visiting_city_trade_depot(
                facade, [best_rect], self._device_id
            )
            self._record_buy(best_item.name)

            others = {p.name for p in items_list} - {best_item.name}
            if others:
                logger.info(
                    "While we’re here, also checking their trade depot for: %s",
                    ", ".join(sorted(others)),
                )
                self._city_depot.sweep_depot_for_targets(
                    others, purchase_by_name, stop_check
                )
            else:
                logger.info("No other items from your list to look for in this city.")

            logger.info("Leaving this city — closing their depot and returning to Global Trade HQ…")
            self._city_depot.return_to_global_trade_hq(stop_check)

            if apply_refresh_timer:
                period = self._config.hq_trade_refresh_period_seconds
                if hq_refresh_anchor_monotonic is not None and period > 0:
                    now = time.monotonic()
                    elapsed = now - hq_refresh_anchor_monotonic
                    remaining = max(0.0, period - elapsed)
                    logger.info(
                        "Trade refresh window (%.0fs): %.1fs elapsed since this pass was ready on the 1st HQ view; %s",
                        period,
                        elapsed,
                        (
                            f"{remaining:.1f}s remaining — waiting before searching HQ again."
                            if remaining > 0
                            else "window already used — continuing to search as a new iteration."
                        ),
                    )
                    if remaining > 0 and not _sleep_interruptible(
                        remaining,
                        stop_check,
                        reason="Waiting for the remainder of the trade refresh window before browsing HQ again.",
                    ):
                        return
                elif hq_refresh_anchor_monotonic is None:
                    logger.warning(
                        "Trade refresh anchor missing — skipping post-visit wait (unexpected)."
                    )

            if stop_check and stop_check():
                logger.info("Stop requested — skipping Best Value / reopen Global Trade HQ.")
                return
            logger.info("Tapping Best Value so new offers can load…")
            click_on_best_value_menu(self._device_id)
            logger.info("Short pause while the game updates…")
            time.sleep(1)
            if stop_check and stop_check():
                return
            logger.info("Opening Global Trade HQ again…")
            click_on_global_trade_hq(self._device_id)
            logger.info("Waiting a moment for the trade screen to finish loading…")
            time.sleep(1)
            view_index = 0

        if need_wait_after_empty_depot_pass:
            elapsed = (
                time.monotonic() - hq_pass_started_monotonic
                if hq_pass_started_monotonic is not None
                else 0.0
            )
            lead = (
                f"Finished searching all trade depot views with no match — this pass took about {elapsed:.1f} seconds."
            )
            if not self._wait_hq_empty_pass_budget(
                hq_pass_started_monotonic or pass_started_monotonic,
                stop_check,
                lead_in=lead,
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
        logger.info(
            "%s Waiting %.1f seconds more (%.0f s window minus %.1f s already spent) before the next refresh.",
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
            reason="Pausing before Best Value / opening the trade depot again.",
        )


def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
