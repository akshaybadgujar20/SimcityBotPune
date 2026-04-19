import logging
import time

from simcity.bot.automation.adb_actions import perform_click, perform_swipe
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
from simcity.bot.enums.building import Building
from simcity.bot.enums.miscellaneous import Miscellaneous


def add_commercial_material_to_production(materials, device_id, stop_event, no_of_materials=11):
    for index, material in enumerate(materials):
        if stop_event and stop_event.is_set():
            break
        missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS,device_id)
        if len(missing_items) > 0:
            logging.info('Missing item window found clicking on it')
            perform_click(710, 795, device_id)
            time.sleep(1)

        goto_commercial_building(device_id, material.building_name)

        for i in range(no_of_materials):
            if stop_event and stop_event.is_set():
                break
            missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS,device_id)
            if len(missing_items) > 0:
                logging.info('Missing item window found clicking on it')
                perform_click(710, 795, device_id)
                time.sleep(1)
            perform_swipe(material.x_location, material.y_location, 520, 940, 500, device_id)

        missing_items, screenshot = find_miscellaneous_material(Miscellaneous.MISSING_ITEMS,device_id)
        if len(missing_items) > 0:
            logging.info('Missing item window found clicking on it')
            perform_click(710, 795, device_id)
            time.sleep(1)


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