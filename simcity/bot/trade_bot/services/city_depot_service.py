from __future__ import annotations

import logging
import time
from typing import Callable, Dict, MutableMapping, Optional, Set

from simcity.bot.automation.city_utility_actions import (
    click_on_global_trade_hq,
    click_on_purchase_menu,
)
from simcity.bot.automation.find_material import (
    find_material_in_trade_depot,
    find_miscellaneous_material,
)
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.automation.close_trade_depot import close_trade_depot
from simcity.bot.city_actions.buy_items import buy_item
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.models.material_facade import material_facade_for
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.services.detection_service import DetectionService
from simcity.bot.trade_bot.services.navigation_wrapper import NavigationWrapper

logger = logging.getLogger("trade_bot")


class CityDepotService:
    def __init__(
        self,
        device_id: str,
        config: TradeBotConfig,
        detection: DetectionService,
        navigation: NavigationWrapper,
        *,
        buy_counts_by_item: Optional[MutableMapping[str, int]] = None,
    ) -> None:
        self._device_id = device_id
        self._config = config
        self._detection = detection
        self._nav = navigation
        self._buy_counts = buy_counts_by_item

    def _record_buy(self, item_name: str) -> None:
        if self._buy_counts is None:
            return
        self._buy_counts[item_name] = self._buy_counts.get(item_name, 0) + 1

    def _trade_box_marker_count(self) -> int:
        rects, _ = find_miscellaneous_material(
            Miscellaneous.TRADE_BOX,
            self._device_id,
            log_empty_match=False,
        )
        return len(rects)

    def _wait_until_visiting_depot_ready(
        self,
        stop_check: Optional[Callable[[], bool]],
    ) -> bool:
        """
        After travel from Global Trade HQ, the game auto-opens the mayor’s depot.
        We treat ``Miscellaneous.TRADE_BOX`` markers as “depot is up” (same signal as legacy code).
        """
        logger.info(
            "Waiting for travel (~5–7s typical) and their trade depot — looking for trade slot markers "
            "(up to %.0fs)…",
            self._config.visiting_depot_trade_box_wait_seconds,
        )
        deadline = time.monotonic() + self._config.visiting_depot_trade_box_wait_seconds
        interval = 1.0
        while time.monotonic() < deadline:
            if stop_check and stop_check():
                logger.info("Stop requested while waiting for their depot.")
                return False
            n = self._trade_box_marker_count()
            if n > 0:
                logger.info(
                    "Reached their city — trade depot is open (counted %s trade slot marker(s) on screen).",
                    n,
                )
                return True
            time.sleep(interval)
        logger.warning(
            "Did not see any trade slot markers — depot may not have opened. Skipping extra shopping here."
        )
        return False

    def sweep_depot_for_targets(
        self,
        target_names: Set[str],
        purchase_by_name: Dict[str, PurchaseItem],
        stop_check: Optional[Callable[[], bool]] = None,
    ) -> None:
        remaining = set(target_names)
        if not remaining:
            logger.info("No extra items to shop for in this city — moving on.")
            return

        if not self._wait_until_visiting_depot_ready(stop_check):
            return

        threshold = self._config.depot_full_page_trade_box_threshold
        max_pages = self._config.max_depot_pages
        logger.info(
            "We’ll scan up to %s mayor depot page(s). If we still need items and see at least %s "
            "trade slot markers on a page, we’ll try the next page; otherwise we stop early.",
            max_pages,
            threshold,
        )

        page = 0
        while page < max_pages:
            if stop_check and stop_check():
                logger.info("You asked to stop — leaving this depot.")
                return
            if not remaining:
                logger.info("Got everything we still needed from this depot.")
                return

            items = [purchase_by_name[n] for n in remaining if n in purchase_by_name]
            if not items:
                logger.warning(
                    "Couldn’t match those item names to your shopping list — stopping depot shopping here."
                )
                return

            box_count = self._trade_box_marker_count()
            logger.info(
                "Mayor depot page %s of %s — %s trade slot marker(s); looking for: %s",
                page + 1,
                max_pages,
                box_count,
                ", ".join(sorted(remaining)),
            )

            screenshot = take_bw_screenshot(self._device_id)
            candidates = self._detection.detect_parallel_depot(
                items, screenshot, stop_check, page_index=page
            )
            flat = self._detection.flatten_sorted_by_priority(candidates)
            deduped = self._detection.dedupe_cross_items(
                flat, self._config.dedup_iou_threshold
            )

            for purchase_item, _rect in deduped:
                if purchase_item.name not in remaining:
                    continue
                facade = material_facade_for(purchase_item)
                logger.info('Trying to buy "%s" from their depot…', purchase_item.name)
                buy_item(facade, self._device_id)
                still, _ = find_material_in_trade_depot(
                    facade,
                    self._device_id,
                    self._config.match_threshold,
                    log_empty_match=False,
                )
                if not still:
                    remaining.discard(purchase_item.name)
                    self._record_buy(purchase_item.name)
                    logger.info(
                        'Looks good — "%s" is no longer showing here (bought or gone).',
                        purchase_item.name,
                    )
                else:
                    logger.info(
                        'Still seeing "%s" on screen after the buy tap — we may try again or move on.',
                        purchase_item.name,
                    )

            if not remaining:
                logger.info("All requested items from your list are handled in this depot.")
                return

            box_after = self._trade_box_marker_count()
            if box_after >= threshold:
                if page + 1 >= max_pages:
                    logger.info(
                        "Saw %s slot markers (full-looking page) but already at max mayor depot pages (%s).",
                        box_after,
                        max_pages,
                    )
                    break
                logger.info(
                    "%s slot markers (≥ %s) — there may be another depot page; swiping. "
                    "Pausing %.1fs…",
                    box_after,
                    threshold,
                    self._config.swipe_after_seconds,
                )
                self._nav.swipe_mayor_depot_next_page()
                time.sleep(self._config.swipe_after_seconds)
                page += 1
                continue

            logger.info(
                "Only %s slot markers on this page (below %s) — treating this as the last depot page. "
                "Still didn’t get: %s",
                box_after,
                threshold,
                ", ".join(sorted(remaining)),
            )
            break

        if remaining:
            logger.info(
                "Mayor depot sweep finished. Still didn’t get: %s",
                ", ".join(sorted(remaining)),
            )

    def return_to_global_trade_hq(
        self,
        stop_check: Optional[Callable[[], bool]] = None,
    ) -> None:
        if stop_check and stop_check():
            logger.info("Stop requested — skipping the trip back to Global Trade HQ.")
            return
        logger.info("Closing their trade depot (ESC)…")
        close_trade_depot(self._device_id)
        logger.info("Opening the purchase menu…")
        click_on_purchase_menu(self._device_id)
        time.sleep(1)
        if stop_check and stop_check():
            return
        logger.info("Opening Global Trade HQ from the purchase menu…")
        click_on_global_trade_hq(self._device_id)
        time.sleep(1)
