import time

import pytesseract
import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe, perform_click, press_esc_key
from simcity.bot.automation.check_adb_devices_and_connect_if_not_connected import check_adb_devices_and_connect_if_not_connected
from simcity.bot.automation.check_for_close_button import check_for_close_button
from simcity.bot.automation.check_for_home_button import check_for_home_button
from simcity.bot.automation.city_utility_actions import click_on_purchase_menu, click_on_own_trade_depot, \
    go_to_next_page_in_city_trade_depot, click_on_city_storage, click_on_own_material_storage, \
    go_to_next_page_in_storage
from simcity.bot.automation.click_on_daniel_face_and_goto_daniel_city import click_on_daniel_face_and_goto_daniel_city, open_global_trade_hq_and_find_material
from simcity.bot.automation.find_empty_trade_boxes_and_sell_material import find_empty_trade_boxes_and_sell_material, \
    stop_sell_materials_task, capture_material_quantity
from simcity.bot.automation.find_material import find_miscellaneous_material, find_material_in_city_storage
from simcity.bot.automation.find_material_count import find_material_count_indefinitely, find_material_count_for_given_iterations
from simcity.bot.automation.find_materials_on_global_trade_hq import find_coins_in_global_trade_hq, stop_buy_items_task
from simcity.bot.automation.open_empty_trade_box import open_empty_trade_box
from simcity.bot.automation.sell_material import sell_material
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
from simcity.bot.automation.trade_depot import find_and_open_trade_depot, check_if_trade_depot_open
from simcity.bot.enums.building import Building
from simcity.bot.enums.material import Material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.logger import setup_logging
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.time_manager import TimerManager

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

import logging
manager = TimerManager()

is_sell_materials_running = True
is_collect_sold_item_money_running = True
is_advertise_all_item_from_trade_depot_running = True
is_collect_raw_materials_running = True
is_add_raw_material_to_production_running = True
is_add_commercial_material_to_production_running = True
is_collect_produced_items_from_commercial_buildings_running = True

material_dict = load_material_info_data()

def set_up(device_id):
    setup_logging()
    check_adb_devices_and_connect_if_not_connected(device_id)

def buy_items(materials, material_priorities, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    manager.create_timer(timer_name, interval=1)
    check_for_close_button(materials, material_priorities, manager, device_id)

def open_next_empty_trade_box(
        device_id,
        current_depot_page,
        used_boxes_on_page,
        max_depot_pages,
        boxes_per_page):

    while True:
        if used_boxes_on_page >= boxes_per_page:
            if current_depot_page >= max_depot_pages:
                return False, current_depot_page, used_boxes_on_page

            go_to_next_page_in_city_trade_depot(device_id)
            time.sleep(1)
            current_depot_page += 1
            used_boxes_on_page = 0
            continue

        empty_trade_boxes, _ = find_miscellaneous_material(
            Miscellaneous.EMPTY_TRADE_BOXES,
            device_id
        )

        if empty_trade_boxes:
            open_empty_trade_box(empty_trade_boxes[0], device_id)
            time.sleep(1)
            return True, current_depot_page, used_boxes_on_page + 1

        used_boxes_on_page = boxes_per_page


def sell_materials(
        materials,
        device_id,
        advertise,
        full_price,
        max_city_storage_scrolls=15,
        max_depot_pages=4,
        boxes_per_page=8):

    click_on_purchase_menu(device_id)
    time.sleep(2)
    click_on_own_trade_depot(device_id)
    time.sleep(2)

    current_depot_page = 1
    used_boxes_on_page = 0

    for material in materials:
        logging.info(f'Selling material: {material.name}')

        # --------------------------------------------------
        # STEP 1: Open ONE trade box to open Sell window
        # --------------------------------------------------
        success, current_depot_page, used_boxes_on_page = \
            open_next_empty_trade_box(
                device_id,
                current_depot_page,
                used_boxes_on_page,
                max_depot_pages,
                boxes_per_page
            )

        if not success:
            logging.info('No empty trade boxes available')
            return

        # --------------------------------------------------
        # STEP 2: Switch storage ONCE for this material
        # --------------------------------------------------
        check_material_type_and_open_trade_depot(device_id, material)
        time.sleep(1)

        # --------------------------------------------------
        # STEP 3: Find material & quantity (vertical scroll)
        # --------------------------------------------------
        founded_material = None
        total_quantity = 0

        for scroll_no in range(max_city_storage_scrolls):
            founded_material_list, _ = find_material_in_city_storage(material, device_id)

            if founded_material_list:
                founded_material = founded_material_list[0]
                total_quantity = capture_material_quantity(founded_material, device_id)
                break

            go_to_next_page_in_storage(device_id)
            time.sleep(1)

        if founded_material is None or total_quantity <= 0:
            logging.info(f'{material.name} not found or zero quantity')
            continue

        remaining_quantity = total_quantity
        logging.info(f'{material.name} quantity: {total_quantity}')

        # --------------------------------------------------
        # STEP 4: Sell using capacity (NO storage switching)
        # --------------------------------------------------
        while remaining_quantity > 0:

            sell_material(
                founded_material,
                device_id,
                advertise,
                full_price,
                material.sell_duration
            )

            remaining_quantity -= min(5, remaining_quantity)
            time.sleep(1)

            if remaining_quantity <= 0:
                break

            success, current_depot_page, used_boxes_on_page = \
                open_next_empty_trade_box(
                    device_id,
                    current_depot_page,
                    used_boxes_on_page,
                    max_depot_pages,
                    boxes_per_page
                )

            if not success:
                logging.info('Depot full while selling')
                return

def check_material_type_and_open_trade_depot(device_id, material):
    if material.building_name != 'FACTORY':
        logging.info('Item is commercial item, opening city storage')
        click_on_city_storage(device_id)
    else:
        logging.info('Item is factory item, opening material storage')
        click_on_own_material_storage(device_id)
    time.sleep(1)


def collect_sold_item_money(iteration, device_id):
    is_trade_depot_open = check_if_trade_depot_open(device_id)
    if not is_trade_depot_open:
        logging.info('trade depot is not open, finding and opening it')
        find_and_open_trade_depot(device_id)
    logging.info('trade depot is open')

    if is_collect_sold_item_money_running:
        logging.info(f'iteration {iteration}')
        if iteration == 4:
            return
        logging.info('finding sold items')
        sold_items, screenshot = find_miscellaneous_material(Miscellaneous.CITY_STORAGE_PURCHASE_COMPLETED, device_id)
        if len(sold_items) > 0:
            for index, sold_item in enumerate(sold_items):
                if is_collect_sold_item_money_running:
                    perform_click_with_rectangle(sold_item, device_id)
            iteration += 1
            collect_sold_item_money(iteration, device_id)
        else:
            perform_swipe(1500, 550, 360, 550, 1000, device_id)
            iteration += 1
            collect_sold_item_money(iteration, device_id)

def collect_produced_items_from_commercial_buildings(no_of_commercial_buildings, device_id):
    for i in range(no_of_commercial_buildings):
        if is_collect_produced_items_from_commercial_buildings_running:
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
        else:
            break

def collect_raw_materials(no_of_factories,device_id):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    for i in range(no_of_factories):
        if is_collect_raw_materials_running:
            logging.info(f'Inside factory no {i+1}')
            perform_click(375, 1025, device_id)
            perform_click(595, 1025, device_id)
            perform_click(810, 1025, device_id)
            perform_click(1030, 1025, device_id)
            perform_click(1240, 1025, device_id)
            time.sleep(0.5)
            perform_click(500, 140, device_id)
        else:
            break

def add_raw_material_to_production(material, no_of_factories, device_id):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    device = u2.connect('127.0.0.1:'+device_id)
    for i in range(no_of_factories):
        if is_add_raw_material_to_production_running:
            device.swipe_points([(material.x_location, material.y_location), (380, 935), (1260, 1000)], duration=0.2)
            time.sleep(0.1)
            perform_click(500, 140, device_id)
            time.sleep(0.5)
        else:
            break

def add_commercial_material_to_production(materials, device_id, no_of_materials= 11):
    for index, material in enumerate(materials):
        if is_add_commercial_material_to_production_running:
            goto_commercial_building(device_id, material.building_name)
            for i in range(no_of_materials):
                if is_add_commercial_material_to_production_running:
                    perform_swipe(material.x_location, material.y_location, 520, 940, 500, device_id)
                else:
                    missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS, device_id)
                    if len(missing_items) > 0:
                        logging.info(f'Missing item window found clicking on it')
                        perform_click(710,795, device_id)
                        time.sleep(1)
                    break

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

# Stopping functions
def stop_sell_materials(is_running):
    global is_sell_materials_running
    is_sell_materials_running = is_running
    stop_sell_materials_task(is_running)

def stop_buy_items(is_running):
    stop_buy_items_task(is_running)

def stop_collect_sold_item_money(is_running):
    global is_collect_sold_item_money_running
    is_collect_sold_item_money_running = is_running

def stop_collect_raw_materials(is_running):
    global is_collect_raw_materials_running
    is_collect_raw_materials_running = is_running

def stop_add_raw_material_to_production(is_running):
    global is_add_raw_material_to_production_running
    is_add_raw_material_to_production_running = is_running

def stop_collect_produced_items_from_commercial_buildings(is_running):
    global is_collect_produced_items_from_commercial_buildings_running
    is_collect_produced_items_from_commercial_buildings_running = is_running

def stop_add_commercial_material_to_production(is_running):
    global is_add_commercial_material_to_production
    is_add_commercial_material_to_production_running = is_running

def set_running_state(is_running):
    stop_buy_items(is_running)
    stop_sell_materials(is_running)
    stop_collect_sold_item_money(is_running)
    stop_collect_raw_materials(is_running)
    stop_add_raw_material_to_production(is_running)
    stop_collect_produced_items_from_commercial_buildings(is_running)
    stop_add_raw_material_to_production(is_running)

def advertise_all_items_on_trade_depot(iteration,device_id):
    is_trade_depot_open = check_if_trade_depot_open(device_id)
    if not is_trade_depot_open:
        logging.info('trade depot is not open, finding and opening it')
        find_and_open_trade_depot(device_id)
    logging.info('trade depot is open')

    if is_advertise_all_item_from_trade_depot_running:
        logging.info(f'iteration {iteration}')
        if iteration == 5:
            return
        logging.info('finding sold items')
        advertised_items, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_DEPOT_COIN, device_id)
        if len(advertised_items) > 0:
            for index, sold_item in enumerate(advertised_items):
                if is_advertise_all_item_from_trade_depot_running:
                    perform_click_with_rectangle(sold_item, device_id)
                    advertised_icon, screenshot = find_miscellaneous_material(Miscellaneous.ADVERTISE_ICON, device_id)
                    if len(advertised_icon) > 0:
                        perform_click_with_rectangle(advertised_icon[0], device_id)
                        perform_click(1280,60, device_id)
                        logging.info(f'waiting for 60s')
                        time.sleep(60)
                    else:
                        perform_click(1280, 60, device_id)
                        continue
            logging.info(f'scrolling horizontaly for next page')
            perform_swipe(1500, 550, 360, 550, 1000, device_id)
            iteration += 1
            advertise_all_items_on_trade_depot(iteration, device_id)
        else:
            perform_swipe(1500, 550, 360, 550, 1000, device_id)
            iteration += 1
            advertise_all_items_on_trade_depot(iteration, device_id)
