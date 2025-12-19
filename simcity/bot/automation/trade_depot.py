import logging

from simcity.bot.automation.city_utility_actions import click_on_purchase_menu, click_on_own_trade_depot
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous


def find_and_open_trade_depot(device_id):
    logging.info('checking if trade hq already open or not')
    my_trade_depot, screenshot = find_miscellaneous_material(Miscellaneous.GLOBAL_TRADE_HQ_CHECK, device_id)
    if len(my_trade_depot) < 1:
        logging.info('checking if trade hq menu visible or not')
        my_trade_depot, screenshot = find_miscellaneous_material(Miscellaneous.GLOBAL_PURCHASE_MENU, device_id)
        if len(my_trade_depot) > 0:
            logging.info('trade hq menu visible')
            click_on_purchase_menu(device_id)
            click_on_own_trade_depot(device_id)

    else:
        logging.info('checking if trade hq already open')
