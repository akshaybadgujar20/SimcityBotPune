import logging
import time
from concurrent.futures import ThreadPoolExecutor

import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle, press_esc_key
from simcity.bot.automation.city_utility_actions import click_on_back_button, click_on_home_button, \
    check_if_i_reach_home, click_on_material_storage, add_item_to_factory_production, click_on_regions_button, \
    click_on_limestone_cliff, click_on_green_valley, click_on_purchase_menu, click_on_global_trade_hq, \
    click_on_best_value_menu
from simcity.bot.automation.find_material import find_miscellaneous_material, find_material_in_global_trade_hq, \
    find_material_in_trade_depot
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.enums.material import Material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.time_manager import TimerManager

manager = TimerManager()
global_trade_hq_timer = "global_trade_hq_timer"
materials_priority_list = []
material_dict = load_material_info_data()
materials_priority_list.append(material_dict[Material.STORAGE_BARS.value])
materials_priority_list.append(material_dict[Material.STORAGE_LOCK.value])
materials_priority_list.append(material_dict[Material.STORAGE_CAMERA.value])

founded_materials_list = []

def buy_items(materials_priority_list, device_id):
    logging.info(f'buy_items')
    manager.create_timer(global_trade_hq_timer, interval=1)
    device = u2.connect(f"127.0.0.1:{device_id}")

    click_on_purchase_menu(device_id)
    time.sleep(1)
    click_on_global_trade_hq(device_id)

    for _ in range(1000):

        click_on_best_value_menu(device_id)
        time.sleep(1)
        click_on_global_trade_hq(device_id)
        time.sleep(1)

        manager.reset_timer(global_trade_hq_timer)

        for _ in range(15):
            coin, screenshot = find_miscellaneous_material(Miscellaneous.COIN, device_id)
            if len(coin) > 0:
                manager.start_timer(global_trade_hq_timer)
                break
            time.sleep(1)

        founded_materials = []

        # Take ONE screenshot
        screenshot = take_bw_screenshot(device_id)

        # Parallel template matching for 3 materials
        with ThreadPoolExecutor(max_workers=len(materials_priority_list)) as executor:
            results = executor.map(match_material, materials_priority_list)

        for material, matches in results:
            if len(matches) > 0:
                founded_materials.append({
                    "material": material,
                    "rectangles": matches
                })

        if len(founded_materials) >= 1:
            logging.info(f'founded_materials {founded_materials}')
            buy_item_from_visiting_city_trade_depot(founded_materials, device_id)
            set_timer()
            continue
        else:
            # swipe to right 1st time
            device.swipe(1575, 460, 620, 460, 0.5)
            time.sleep(2)
            # Take ONE screenshot
            screenshot = take_bw_screenshot(device_id)

            # Parallel template matching for 3 materials
            with ThreadPoolExecutor(max_workers=len(materials_priority_list)) as executor:
                results = executor.map(match_material, materials_priority_list)

            for material, matches in results:
                if len(matches) > 0:
                    founded_materials.append({
                        "material": material,
                        "rectangles": matches
                    })

            if len(founded_materials) >= 1:
                logging.info(f'founded_materials {founded_materials}')
                buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
                set_timer()
                continue
            else:
                set_timer()


def match_material(material):
    matches, _ = find_material_in_global_trade_hq(
        material,
        device_id,
        screenshot = screenshot
    )
    return material, matches

def buy_item_from_visiting_city_trade_depot(found_item_list, device_id):
    perform_click_with_rectangle(found_item_list[0], device_id)
    time.sleep(5)
    check_if_visiting_city_trade_depo_opened_or_not(device_id)
    buy_item(device_id)


def check_if_visiting_city_trade_depo_opened_or_not(device_id):
    for _ in range(15):
        trade_boxes, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_BOX, device_id)
        if len(trade_boxes) > 0:
            break
        time.sleep(1)


def buy_item(material, device_id):
    device = u2.connect(f"127.0.0.1:{device_id}")

    materials, screenshot = find_material_in_trade_depot(material, device_id)

    if len(materials) >= 1:
        for mat in materials:
            perform_click_with_rectangle(mat, device_id)
            time.sleep(1)
        return

    device.swipe(1575, 460, 620, 460, 0.5)
    time.sleep(2)

    materials, screenshot = find_material_in_trade_depot(material, device_id)

    if len(materials) >= 1:
        for mat in materials:
            perform_click_with_rectangle(mat, device_id)
            time.sleep(1)


def set_timer():
    timer = manager.get_timer_time(global_trade_hq_timer)
    if timer < 27:
        time.sleep(30 - timer)


def buy_for_all_cities(materials_priority_list, device_id, stop_event):

    cities = [
        click_on_home_button,
        click_on_limestone_cliff,
        click_on_green_valley,
        click_on_regions_button
    ]

    for city in cities:
        city(device_id)
        time.sleep(3)
        buy_items(materials_priority_list, device_id, stop_event)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    device_id = "5555"

    materials_priority_list = [
        Miscellaneous.NAIL,
        Miscellaneous.WOOD,
        Miscellaneous.PLASTIC
    ]

    buy_for_all_cities(materials_priority_list, device_id, None)