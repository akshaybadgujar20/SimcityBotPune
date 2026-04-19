import logging
import time
import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle, press_esc_key
from simcity.bot.automation.city_utility_actions import click_on_back_button, click_on_home_button, \
    check_if_i_reach_home, click_on_material_storage, add_item_to_factory_production, click_on_regions_button, \
    click_on_limestone_cliff, click_on_green_valley, click_on_purchase_menu, click_on_global_trade_hq, \
    click_on_best_value_menu
from simcity.bot.automation.find_material import find_miscellaneous_material, find_material_in_global_trade_hq, \
    find_material_in_trade_depot
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import manager
from simcity.bot.time_manager import TimerManager

manager = TimerManager()
global_trade_hq_timer = "global_trade_hq_timer"
production_timer = "production_timer"

def buy_items(
        material_to_be_found,
        device_id,
        stop_event):
    logging.info(f'buy_items')
    manager.create_timer(global_trade_hq_timer, interval=1)
    device = u2.connect(f"127.0.0.1:{device_id}")
    logging.info(f'Opening purchase menu item')
    click_on_purchase_menu(device_id)
    time.sleep(1)
    click_on_global_trade_hq(device_id)
    for i in range(1000):
        click_on_best_value_menu(device_id)
        time.sleep(1)
        click_on_global_trade_hq(device_id)
        time.sleep(1)
        manager.reset_timer(global_trade_hq_timer)
        for i in range(15):
            coin, screenshot = find_miscellaneous_material(Miscellaneous.COIN, device_id)
            if len(coin) > 0:
                manager.start_timer(global_trade_hq_timer)
                break
            time.sleep(1)
            continue

        founded_materials, screenshot = find_material_in_global_trade_hq(material_to_be_found, device_id)
        if len(founded_materials) == 1:
            buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
            set_timer()
            continue
        elif len(founded_materials) > 1:
            buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
            continue
            # goto next global trade hq for buy
        else:
            # swipe to right 1st time
            device.swipe(1575, 460, 620, 460, 0.5)
            time.sleep(2)
            founded_materials, screenshot = find_material_in_global_trade_hq(material_to_be_found, device_id)
            if len(founded_materials) == 1:
                buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
                set_timer()
                continue
            elif len(founded_materials) > 1:
                buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
                continue
                # goto next global trade hq for buy
            else:
                # swipe to right 2nd time
                device.swipe(1575, 460, 620, 460, 0.5)
                time.sleep(2)
                founded_materials, screenshot = find_material_in_global_trade_hq(material_to_be_found, device_id)
                if len(founded_materials) == 1:
                    buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
                    set_timer()
                    continue
                elif len(founded_materials) > 1:
                    buy_item_from_visiting_city_trade_depot(material_to_be_found, founded_materials, device_id)
                    continue
                    # goto next global trade hq for buy
                else:
                    set_timer()

def buy_item_from_visiting_city_trade_depot(material, found_item_list, device_id):
    logging.info(f'{material.name} found')
    global home
    home = False
    perform_click_with_rectangle(found_item_list[0], device_id)
    time.sleep(5)
    check_if_visiting_city_trade_depo_opened_or_not(device_id)
    buy_item(material, device_id)

def check_if_visiting_city_trade_depo_opened_or_not(device_id):
    for i in range(15):
        trade_boxes, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_BOX, device_id)
        if len(trade_boxes) > 0:
            break
        time.sleep(1)
        continue

def buy_item(material, device_id):
    materials, screenshot = find_material_in_trade_depot(material, device_id)
    if len(materials) >= 1:
        logging.info(f'{material.name} (More than 1) icon found and clicking on all one by one')
        for material in materials:
            perform_click_with_rectangle(material, device_id)
            time.sleep(3)
    elif len(materials) == 1:
        logging.info(f'{material.name} (More than 1) icon found and clicking on 1st it')
        perform_click_with_rectangle(materials[0], device_id)
    else:
        # swipe to right 1nd time
        device.swipe(1575, 460, 620, 460, 0.5)
        time.sleep(2)
        materials, screenshot = find_material_in_trade_depot(material, device_id)
        if len(materials) >= 1:
            logging.info(f'{material.name} (More than 1) icon found and clicking on all one by one')
            for material in materials:
                perform_click_with_rectangle(material, device_id)
                time.sleep(1)
        elif len(materials) == 1:
            logging.info(f'{material.name} (More than 1) icon found and clicking on 1st it')
            perform_click_with_rectangle(materials[0], device_id)
        else:
            return
    return

def set_timer():
    timer = manager.get_timer_time(global_trade_hq_timer)
    if timer < 27:
        time.sleep(30-timer)
    return