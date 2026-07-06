from __future__ import annotations

import logging
import time

import uiautomator2 as u2

from simcity.bot.automation.city_utility_actions import go_to_next_page_in_city_trade_depot
from simcity.bot.trade_bot.config.defaults import TradeBotConfig
from simcity.bot.trade_bot.utils.trade_log import trade_log

logger = logging.getLogger("trade_bot")


class NavigationWrapper:
    def __init__(self, device_id: str) -> None:
        self._device_id = device_id

    def swipe_trade_depot_next_view(self, config: TradeBotConfig) -> None:
        trade_log(self._device_id, "NAV", "Swiping right to the next Global Trade HQ page")
        device = u2.connect(f"127.0.0.1:{self._device_id}")
        device.swipe(
            config.hq_swipe_x1,
            config.hq_swipe_y1,
            config.hq_swipe_x2,
            config.hq_swipe_y2,
            config.hq_swipe_duration_s,
        )

    def navigate_to_hq_view(self, view_index: int, config: TradeBotConfig) -> None:
        """Swipe right from HQ page 1 until ``view_index`` (0-based) is reached."""
        if view_index <= 0:
            return
        trade_log(
            self._device_id,
            "NAV",
            "Navigating back to HQ page %s — %s swipe(s) right",
            view_index + 1,
            view_index,
        )
        for swipe_num in range(1, view_index + 1):
            trade_log(
                self._device_id,
                "NAV",
                "HQ restore swipe %s of %s",
                swipe_num,
                view_index,
            )
            self.swipe_trade_depot_next_view(config)
            time.sleep(config.swipe_after_seconds)

    def swipe_mayor_depot_next_page(self) -> None:
        trade_log(self._device_id, "NAV", "Swiping to the next page in this mayor's trade depot")
        go_to_next_page_in_city_trade_depot(self._device_id)
