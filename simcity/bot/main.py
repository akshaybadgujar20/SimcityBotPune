import time

import pytesseract
import uiautomator2 as u2

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe, perform_click, press_esc_key
from simcity.bot.automation.check_adb_devices_and_connect_if_not_connected import \
    check_adb_devices_and_connect_if_not_connected
from simcity.bot.automation.check_for_close_button import check_for_close_button
from simcity.bot.automation.city_utility_actions import go_to_next_page_in_city_trade_depot, click_on_return_button
from simcity.bot.automation.find_empty_trade_boxes_and_sell_material import find_empty_trade_boxes_and_sell_material
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.find_materials_on_global_trade_hq import stop_buy_items_task
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
from simcity.bot.automation.trade_depot import find_and_open_trade_depot
from simcity.bot.enums.building import Building
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.logger import setup_logging
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.time_manager import TimerManager

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

import logging
manager = TimerManager()

material_dict = load_material_info_data()

def set_up(device_id):
    setup_logging()
    check_adb_devices_and_connect_if_not_connected(device_id)

def buy_items(materials, material_priorities, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    manager.create_timer(timer_name, interval=1)
    check_for_close_button(materials, material_priorities, manager, device_id)

def sell_materials( materials, device_id, advertise, full_price):
    find_empty_trade_boxes_and_sell_material(materials, device_id, advertise, full_price)

def collect_sold_item_money(device_id, max_pages=5):
    logging.info('opening trade HQ')
    find_and_open_trade_depot(device_id)

    logging.info('trade depot is open')

    for current_page in range(1, max_pages + 1):
        logging.info(f'scanning trade depot page {current_page}')

        sold_items, _ = find_miscellaneous_material(Miscellaneous.CITY_STORAGE_PURCHASE_COMPLETED, device_id)

        if len(sold_items) > 0:
            logging.info(f'found {len(sold_items)} sold items')

            for sold_item in sold_items:
                perform_click_with_rectangle(sold_item, device_id)
                time.sleep(0.3)
        else:
            logging.info('no sold items on this page')

        # Move to next page if not last
        if current_page < max_pages:
            go_to_next_page_in_city_trade_depot(device_id)

    click_on_return_button(device_id)

def collect_produced_items_from_commercial_buildings(no_of_commercial_buildings, device_id):
    for i in range(no_of_commercial_buildings):
        logging.info(f'Inside commercial building window')
        press_esc_key(device_id)
        time.sleep(1)
        for j in range(11):
            perform_click(950, 520, device_id)
        else:
            logging.info(f'11 clicks finished')
            time.sleep(1)
            found_item, screenshot = find_miscellaneous_material(Miscellaneous.COMMERCIAL_INFO_ICON, device_id)
            if len(found_item) > 0:
                logging.info('commercial building window is open, go to next one')
                perform_click(500, 140, device_id)
                time.sleep(1)
            else:
                logging.info(f'opening commercial building window again')
                perform_click(950, 520, device_id)
                logging.info('sleeping 1 sec')
                time.sleep(1)
                logging.info('clicking on left button')
                perform_click(500, 140, device_id)


def collect_raw_materials(no_of_factories,device_id):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    for i in range(no_of_factories):
        logging.info(f'Inside factory no {i+1}')
        perform_click(375, 1025, device_id)
        perform_click(595, 1025, device_id)
        perform_click(810, 1025, device_id)
        perform_click(1030, 1025, device_id)
        perform_click(1240, 1025, device_id)
        time.sleep(0.5)
        perform_click(500, 140, device_id)


def add_raw_material_to_production(material, no_of_factories, device_id):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    device = u2.connect('127.0.0.1:'+device_id)
    for i in range(no_of_factories):
        device.swipe_points([(material.x_location, material.y_location), (380, 935), (1260, 1000)], duration=0.2)
        time.sleep(0.1)
        perform_click(500, 140, device_id)
        time.sleep(0.5)


def add_commercial_material_to_production(materials, device_id, no_of_materials= 11):
    for index, material in enumerate(materials):
        goto_commercial_building(device_id, material.building_name)
        for i in range(no_of_materials):
            perform_swipe(material.x_location, material.y_location, 520, 940, 500, device_id)


        missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS, device_id)
        if len(missing_items) > 0:
            logging.info(f'Missing item window found clicking on it')
            perform_click(710,795, device_id)
            time.sleep(1)
        else:
            missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS, device_id)
            if len(missing_items) > 0:
                logging.info(f'Missing item window found clicking on it')
                perform_click(710,795, device_id)
                time.sleep(1)
            break

def goto_commercial_building(device_id, building_name):
    logging.info(f'building_name => {building_name}')
    keyword_array = []
    keyword_array = fetch_keyword_array(building_name)
    logging.info(f'keyword_array => {keyword_array}')
    for i in range(15):
        commercial_building_name: str = take_screenshot_and_read_text(device_id, 690, 105, 1250, 165)
        logging.info(f'commercial_building_name => {commercial_building_name}')
        if any(item in commercial_building_name.lower() for item in keyword_array):
            break
        else:
            perform_click(500, 140, device_id)
            continue

def fetch_keyword_array(building_name):
    vu_random_generator = ["vu's random gnerator"]
    toy_shop = ["toy shop"]
    building_supplies_store = ["building supplies store"]
    gardening_supplies = ["gardening supplies"]
    farmer_market = ["farmer's market"]
    hardware_store = ["hardware store"]
    fashion_store = ["fashion store"]
    home_appliances = ["home appliances"]
    furniture_store = ["furniture store"]
    donut_shop = ["donut shop"]
    fast_food_restaurant = ["fast food restaurant"]
    dessert_shop = ["dessert shop"]
    country_store = ["country store"]
    sports_shop = ["sports shop"]
    bureau_of_restoration = ["bureau of restoration"]
    if building_name == Building.VU_RANDOM_GENERATOR.value:
        return vu_random_generator
    elif building_name == Building.TOY_SHOP.value:
        return toy_shop
    elif building_name == Building.BUILDING_SUPPLIES_STORE.value:
        return building_supplies_store
    elif building_name == Building.GARDENING_SUPPLIES.value:
        return gardening_supplies
    elif building_name == Building.FARMER_S_MARKET.value:
        return farmer_market
    elif building_name == Building.HARDWARE_STORE.value:
        return hardware_store
    elif building_name == Building.FASHION_STORE.value:
        return fashion_store
    elif building_name == Building.HOME_APPLIANCES.value:
        return home_appliances
    elif building_name == Building.FURNITURE_STORE.value:
        return furniture_store
    elif building_name == Building.DONUT_SHOP.value:
        return donut_shop
    elif building_name == Building.FAST_FOOD_RESTAURANT.value:
        return fast_food_restaurant
    elif building_name == Building.DESERT_SHOP.value:
        return dessert_shop
    elif building_name == Building.COUNTRY_STORE.value:
        return country_store
    elif building_name == Building.SPORT_SHOP.value:
        return sports_shop
    elif building_name == Building.BUREAU_OF_RESTORATION.value:
        return bureau_of_restoration

def buy_from_friends(materials, city_name, device_id):
    logging.info('finding friends icon')
    friends, screenshot = find_miscellaneous_material(Miscellaneous.FRIENDS, device_id)
    if len(friends) > 0:
        logging.info('friends icon found and clicking on it')
        perform_click_with_rectangle(friends[0], device_id)
        city_name, screenshot = find_miscellaneous_material(Miscellaneous['TRADER_RIDGE'], device_id)
        if len(friends) > 0:
            perform_click_with_rectangle(city_name, device_id)
            time.sleep(10)
            remote_trade_depot_icon, screenshot = find_miscellaneous_material(Miscellaneous.REMOTE_TRADE_DEPOT_ICON, device_id)
            if len(remote_trade_depot_icon) > 0:
                perform_click_with_rectangle(remote_trade_depot_icon, device_id)
                time.sleep(1)
                coins, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_DEPOT_COIN, device_id)
                if len(coins) > 0:
                    for i in range(4):
                        for coin in coins:
                            perform_click_with_rectangle(coin, device_id)
                        perform_swipe(1500, 550, 350, 550, 1000, device_id)


    else:
        logging.info('friends icon not found')

