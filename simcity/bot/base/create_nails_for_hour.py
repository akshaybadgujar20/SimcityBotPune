import logging
import time
from types import SimpleNamespace

import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click, press_esc_key, perform_swipe
from simcity.bot.automation.city_utility_actions import click_on_material_storage
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import add_raw_material_to_production, collect_raw_materials, set_up, \
    collect_produced_items_from_commercial_buildings

device_id = '5555'
device = u2.connect("127.0.0.1:5555")

def produce_metal():
    material = SimpleNamespace(
        x_location=665,
        y_location=375
    )
    # add metal to production
    for i in range(6):
        collect_raw_materials(12, device_id)
        add_raw_material_to_production(material, 12, device_id)
        time.sleep(62)
    # logging.info('going to random factory')
    # perform_click(500, 140, device_id)
    # time.sleep(1)
    # logging.info('going to building supply store')
    # perform_click(500, 140, device_id)
    # time.sleep(1)
    # logging.info('clicking on material storage')
    # perform_click(500, 140, device_id)
    # time.sleep(1)
    # logging.info('clicking esc')
    # press_esc_key(device_id)

def manufacture_nails():
    material = SimpleNamespace(
        x_location=665,
        y_location=375
    )

    for i in range(12):
        logging.info('waiting for 150 sec')
        time.sleep(150)
        click_on_material_storage(device_id)
        time.sleep(1)
        press_esc_key(device_id)
        time.sleep(1)
        logging.info("collecting nails")
        for j in range(11):
            perform_click(950, 520, device_id)
            time.sleep(1)
        logging.info("checking for building opening")
        found_item, screenshot = find_miscellaneous_material(Miscellaneous.BUILDING_SUPPLY_STORE, device_id)
        logging.info(f"len(found_item) => {len(found_item)}")
        if len(found_item) < 1:
            perform_click(950, 520, device_id)
            time.sleep(1)
        # add metal to production
        logging.info("adding nails to production")
        for j in range(11):
            perform_swipe(material.x_location, material.y_location, 520, 940, 500, device_id)
            time.sleep(1)


set_up(device_id)
# produce_metal()
# goto building supply store
manufacture_nails()