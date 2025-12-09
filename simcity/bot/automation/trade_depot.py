import logging
import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous


def find_and_open_trade_depot(device_id):
    is_depot_close = True
    for i in range(9):
        my_trade_depot, screenshot = find_miscellaneous_material(Miscellaneous.MY_TRADE_DEPOT, device_id)
        if len(my_trade_depot) > 0:
            logging.info(f'Trade Depot found {len(my_trade_depot)}, opening it')
            perform_click_with_rectangle(my_trade_depot[0], device_id)
            is_depot_close = False
            time.sleep(1)
            break
        perform_swipe( 630, 815, 1700, 165, 1000, device_id)

    if is_depot_close:
        perform_swipe( 1700, 165, 630, 815, 1000, device_id)
        perform_swipe( 960, 120, 960, 700, 1000, device_id)
        my_trade_depot, screenshot = find_miscellaneous_material(Miscellaneous.MY_TRADE_DEPOT, device_id)
        if len(my_trade_depot) > 0:
            logging.info(f'Trade Depot found {len(my_trade_depot)}, opening it')
            perform_click_with_rectangle(my_trade_depot[0], device_id)
            time.sleep(1)

def check_if_trade_depot_open(device_id):
    logging.info(f'checking is trade depot is open or not')
    trade_depot_name, screenshot = find_miscellaneous_material(Miscellaneous.TRADE_DEPOT_NAME, device_id)
    if len(trade_depot_name) > 0:
        logging.info(f'Trade Depot open')
        return True
    return False