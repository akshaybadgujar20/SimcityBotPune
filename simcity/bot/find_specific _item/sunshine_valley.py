import logging
import time

import uiautomator2 as u2
from sympy import false

from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle, press_esc_key
from simcity.bot.automation.city_utility_actions import click_on_back_button, check_if_regions_button_visible, \
    click_on_home_button, collect_all_items_from_factory, add_item_to_factory_production, check_if_i_reach_home, \
    click_on_regions_button, click_on_limestone_cliff, click_on_green_valley, click_on_material_storage
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up
from simcity.bot.time_manager import TimerManager

device_id = '5565'
device = u2.connect("127.0.0.1:5565")
manager = TimerManager()
global_trade_hq_timer = "global_trade_hq_timer"
production_timer = "production_timer"

def perform_automation():
    manager.create_timer(global_trade_hq_timer, interval=1)
    for i in range(1000):
        # search for item
        perform_click(180,195, device_id)
        time.sleep(1)
        perform_click(170, 335, device_id)
        time.sleep(1)

        manager.reset_timer(global_trade_hq_timer)
        for i in range(15):
            coin, screenshot = find_miscellaneous_material(Miscellaneous.COIN, device_id)
            if len(coin) > 0:
                manager.start_timer(global_trade_hq_timer)
                break
            time.sleep(1)
            continue

        recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
        if len(recycled_fabric) == 1:
            buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
            check_for_production_of_recycled_fabric()
            set_timer()
            continue
        elif len(recycled_fabric) > 1:
            buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
            check_for_production_of_recycled_fabric()
            continue
            # goto next global trade hq for buy
        else:
            # swipe to right 1st time
            device.swipe(1575, 460, 620, 460, 0.5)
            time.sleep(1)
            recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
            if len(recycled_fabric) == 1:
                buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
                check_for_production_of_recycled_fabric()
                set_timer()
                continue
            elif len(recycled_fabric) > 1:
                buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
                check_for_production_of_recycled_fabric()
                continue
                # goto next global trade hq for buy
            else:
                # swipe to right 2nd time
                device.swipe(1575, 460, 620, 460, 0.5)
                time.sleep(1)
                recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
                if len(recycled_fabric) == 1:
                    buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
                    check_for_production_of_recycled_fabric()
                    set_timer()
                    continue
                elif len(recycled_fabric) > 1:
                    buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric)
                    check_for_production_of_recycled_fabric()
                    continue
                    # goto next global trade hq for buy
                else:
                    check_for_production_of_recycled_fabric()
                    set_timer()

def check_for_production_of_recycled_fabric():
    timer = manager.get_timer_time(production_timer)
    logging.info(f"timer: {timer}")
    if timer is not None and timer > 360:
        click_on_back_button(device_id)
        logging.info("finding REGIONS")
        regions_icon, screenshot = find_miscellaneous_material(Miscellaneous.REGIONS, device_id)
        if len(regions_icon) > 0:
            logging.info("REGIONS found")
            logging.info("clicking on regions button")
            handle_scenario_where_i_am_in_same_region()
            handle_adding_recycle_fabric_to_production_when_previous_production_is_ready()
        else:
            time.sleep(1)
            click_on_home_button(device_id)
            check_if_i_reach_home(device_id)
            handle_adding_recycle_fabric_to_production_when_previous_production_is_ready()
    elif timer is None:
        click_on_back_button(device_id)
        regions_icon, screenshot = find_miscellaneous_material(Miscellaneous.REGIONS, device_id)
        if len(regions_icon) > 0:
            handle_scenario_where_i_am_in_same_region()
            add_items_to_production_when_no_timer_present()
        else:
            click_on_home_button(device_id)
            check_if_i_reach_home(device_id)
            add_items_to_production_when_no_timer_present()
    else:
        # click_on_back_button(device_id)
        # home_trade_icon, screenshot = find_miscellaneous_material(Miscellaneous.HOME_TRADE_ICON, device_id)
        # if len(home_trade_icon) > 0:
        #     perform_click_with_rectangle(home_trade_icon[0], device_id)
        # time.sleep(1)
        return

    logging.info("process complete")
    click_on_material_storage(device_id)
    time.sleep(1)
    press_esc_key(device_id)
    time.sleep(1)
    home_trade_icon, screenshot = find_miscellaneous_material(Miscellaneous.HOME_TRADE_ICON, device_id)
    if len(home_trade_icon) > 0:
        perform_click_with_rectangle(home_trade_icon[0], device_id)
    time.sleep(1)
    return

def add_items_to_production_when_no_timer_present():
    perform_click(490, 510, device_id)
    time.sleep(1)
    add_item_to_factory_production(device, 670, 370, 380, 935, 1260, 935)
    manager.create_timer(production_timer, interval=1)
    manager.start_timer(production_timer)

def handle_scenario_where_i_am_in_same_region():
    click_on_regions_button(device_id)
    time.sleep(1)
    click_on_limestone_cliff(device_id)
    check_if_i_reach_home(device_id)
    click_on_regions_button(device_id)
    time.sleep(1)
    click_on_green_valley(device_id)
    check_if_i_reach_home(device_id)

def handle_adding_recycle_fabric_to_production_when_previous_production_is_ready():
    timer = manager.get_timer_time(production_timer)
    logging.info("handle_adding_recycle_fabric_to_production_when_previous_production_is_ready")
    logging.info(f"timer {timer}")
    logging.info("Timer present and it is > 300")
    perform_click(530, 520, device_id)
    time.sleep(0.2)
    perform_click(530, 520, device_id)
    time.sleep(0.2)
    perform_click(530, 520, device_id)
    time.sleep(0.2)
    perform_click(530, 520, device_id)
    time.sleep(0.2)
    perform_click(530, 520, device_id)
    time.sleep(1)
    perform_click(530, 520, device_id)
    time.sleep(1)
    add_item_to_factory_production(device, 670, 370, 380, 935, 1260, 935)
    manager.reset_timer(production_timer)
    manager.start_timer(production_timer)


def set_timer():
    timer = manager.get_timer_time(global_trade_hq_timer)
    if timer < 27:
        time.sleep(30-timer)
    return

def produce_and_collect_recycle_fabric():
    for i in range(100):
        perform_click(375, 1025, device_id)
        perform_click(595, 1025, device_id)
        perform_click(810, 1025, device_id)
        perform_click(1030, 1025, device_id)
        perform_click(1240, 1025, device_id)
        device.swipe_points([(670, 370), (380, 935), (1260, 935)], duration=0.3)
        time.sleep(301)

def buy_recycle_fabric_from_visiting_city_trade_depot(recycled_fabric):
    logging.info('recycle fabric found')
    global home
    home= False
    perform_click_with_rectangle(recycled_fabric[0], device_id)
    time.sleep(5)
    check_if_visiting_city_trade_depo_opened_or_not()
    buy_recycled_fabric()

def check_if_visiting_city_trade_depo_opened_or_not():
    for i in range(15):
        my_trade_depot, screenshot = find_miscellaneous_material(Miscellaneous.VISITNG_TRADE_DEPOT, device_id)
        if len(my_trade_depot) > 0:
            perform_click_with_rectangle(my_trade_depot[0], device_id)
            break
        time.sleep(1)
        continue
    time.sleep(1)
    for i in range(15):
        trade_boxes, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_BOX, device_id)
        if len(trade_boxes) > 0:
            break
        time.sleep(1)
        continue

def buy_recycled_fabric():
    recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC_2, device_id)
    if len(recycled_fabric) >= 1:
        logging.info('recycled_fabric (More than 1) icon found and clicking on all one by one')
        for recycled_fabric_data in recycled_fabric:
            perform_click_with_rectangle(recycled_fabric_data, device_id)
            time.sleep(1)
    else:
        logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')
    return

set_up(device_id)
# produce_and_collect_recycle_fabric()
perform_automation()