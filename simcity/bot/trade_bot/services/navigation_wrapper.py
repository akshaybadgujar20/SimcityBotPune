from __future__ import annotations

import logging

import uiautomator2 as u2

from simcity.bot.automation.city_utility_actions import go_to_next_page_in_city_trade_depot
from simcity.bot.trade_bot.config.defaults import TradeBotConfig

logger = logging.getLogger("trade_bot")


class NavigationWrapper:
    def __init__(self, device_id: str) -> None:
        self._device_id = device_id

    def swipe_trade_depot_next_view(self, config: TradeBotConfig) -> None:
        logger.info("Swiping right to the next trade depot view…")
        device = u2.connect(f"127.0.0.1:{self._device_id}")
        device.swipe(
            config.hq_swipe_x1,
            config.hq_swipe_y1,
            config.hq_swipe_x2,
            config.hq_swipe_y2,
            config.hq_swipe_duration_s,
        )

    def swipe_mayor_depot_next_page(self) -> None:
        logger.info("Swiping to the next page in this mayor’s trade depot…")
        go_to_next_page_in_city_trade_depot(self._device_id)
