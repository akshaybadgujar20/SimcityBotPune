import time

import uiautomator2 as u2

from simcity.bot.automation.adb_actions import perform_click_with_rectangle
from simcity.bot.automation.find_material import (
    find_material_in_trade_depot,
    find_miscellaneous_material,
)
from simcity.bot.enums.material import Material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import manager
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem
from simcity.bot.trade_bot.utils.trade_log import trade_log

global_trade_hq_timer = "global_trade_hq_timer"
production_timer = "production_timer"


def _to_purchase_items(material_or_list) -> list[PurchaseItem]:
    if isinstance(material_or_list, list):
        return [
            PurchaseItem(name=m.name, priority=index + 1, material=Material[m.name])
            for index, m in enumerate(material_or_list)
        ]
    material = material_or_list
    return [
        PurchaseItem(name=material.name, priority=1, material=Material[material.name])
    ]


def buy_items(material_or_list, device_id, stop_event):
    """Backward-compatible entry point; delegates to ``run_trade_session``."""
    from simcity.bot.trade_bot.orchestrator.trade_session import run_trade_session

    purchase_items = _to_purchase_items(material_or_list)
    trade_log(
        device_id,
        "SESSION",
        "buy_items wrapper — delegating %s item(s) to run_trade_session",
        len(purchase_items),
    )
    run_trade_session(device_id, purchase_items, stop_event)


def buy_item_from_visiting_city_trade_depot(material, found_item_list, device_id):
    trade_log(
        device_id,
        "DEPOT",
        'HQ listing matched "%s" — clicking ad',
        material.name,
    )
    perform_click_with_rectangle(found_item_list[0], device_id)
    time.sleep(5)
    check_if_visiting_city_trade_depo_opened_or_not(device_id)
    buy_item(material, device_id)


def check_if_visiting_city_trade_depo_opened_or_not(device_id):
    for _ in range(15):
        trade_boxes, _ = find_miscellaneous_material(Miscellaneous.TRADE_BOX, device_id)
        if len(trade_boxes) > 0:
            trade_log(
                device_id,
                "DEPOT",
                "Visiting mayor depot open — %s trade slot marker(s)",
                len(trade_boxes),
            )
            break
        time.sleep(1)


def buy_item(material, device_id):
    material_name = material.name
    materials, _ = find_material_in_trade_depot(material, device_id)
    if len(materials) >= 1:
        trade_log(
            device_id,
            "DEPOT",
            'Found %s "%s" listing(s) — clicking each',
            len(materials),
            material_name,
        )
        for rect in materials:
            perform_click_with_rectangle(rect, device_id)
            time.sleep(3)
    else:
        device = u2.connect(f"127.0.0.1:{device_id}")
        trade_log(
            device_id,
            "DEPOT",
            '"%s" not on first depot page — swiping to page 2',
            material_name,
        )
        device.swipe(1575, 460, 620, 460, 0.5)
        time.sleep(2)
        materials, _ = find_material_in_trade_depot(material, device_id)
        if len(materials) >= 1:
            trade_log(
                device_id,
                "DEPOT",
                'Found %s "%s" listing(s) on page 2 — clicking',
                len(materials),
                material_name,
            )
            for rect in materials:
                perform_click_with_rectangle(rect, device_id)
                time.sleep(1)
        else:
            trade_log(
                device_id,
                "DEPOT",
                '"%s" not found in visiting depot after swipe',
                material_name,
            )


def set_timer():
    timer = manager.get_timer_time(global_trade_hq_timer)
    if timer < 27:
        time.sleep(30 - timer)
