"""
Deprecated standalone script — use ``run_trade_session`` from ``simcity.bot.trade_bot``.

This module previously contained an experimental multi-material buy loop. It now
delegates to the same trade_bot session used by ``CONTINUOUS_BUY`` on the API.
"""

import logging
import time

from simcity.bot.automation.city_utility_actions import (
    click_on_green_valley,
    click_on_home_button,
    click_on_limestone_cliff,
    click_on_regions_button,
)
from simcity.bot.enums.material import Material
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.trade_bot import PurchaseItem, run_trade_session

material_dict = load_material_info_data()

DEFAULT_PURCHASE_ITEMS = [
    PurchaseItem(name=Material.STORAGE_BARS.name, priority=1, material=Material.STORAGE_BARS),
    PurchaseItem(name=Material.STORAGE_LOCK.name, priority=2, material=Material.STORAGE_LOCK),
    PurchaseItem(name=Material.STORAGE_CAMERA.name, priority=3, material=Material.STORAGE_CAMERA),
]


def buy_items(materials_priority_list, device_id, stop_event=None):
    """Run continuous multi-item buy for one city (delegates to trade_bot)."""
    purchase_items = [
        PurchaseItem(name=m.name, priority=index + 1, material=Material[m.name])
        for index, m in enumerate(materials_priority_list)
    ]
    run_trade_session(device_id, purchase_items, stop_event)


def buy_for_all_cities(materials_priority_list, device_id, stop_event):
    cities = [
        click_on_home_button,
        click_on_limestone_cliff,
        click_on_green_valley,
        click_on_regions_button,
    ]
    for city in cities:
        city(device_id)
        time.sleep(3)
        buy_items(materials_priority_list, device_id, stop_event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    device_id = "5555"
    materials_priority_list = [
        material_dict[Material.STORAGE_BARS.value],
        material_dict[Material.STORAGE_LOCK.value],
        material_dict[Material.STORAGE_CAMERA.value],
    ]
    buy_for_all_cities(materials_priority_list, device_id, None)
