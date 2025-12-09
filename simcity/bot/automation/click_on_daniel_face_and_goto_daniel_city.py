import logging
import time

from simcity.bot.automation.adb_actions import perform_click
from simcity.bot.automation.find_materials_on_global_trade_hq import find_coins_in_global_trade_hq
from simcity.bot.automation.find_trade_icon_in_daniel_city import find_trade_icon_in_daniel_city


def click_on_daniel_face_and_goto_daniel_city(materials, material_priorities, x_location, y_location, manager, device_id):
    time.sleep(1)
    logging.info(f'clicking on daniel face, x location: {x_location}, y location: {y_location}')
    perform_click(x_location, y_location, device_id)
    time.sleep(5)
    perform_click(960, 540, device_id)
    open_global_trade_hq_and_find_material(materials, material_priorities, manager, device_id)

def open_global_trade_hq_and_find_material(materials, material_priorities, manager, device_id):
    find_trade_icon_in_daniel_city(device_id)
    time.sleep(1)
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    manager.start_timer(timer_name)
    logging.info('opening global trade hq')
    perform_click(1610, 200, device_id)
    time.sleep(1)
    find_coins_in_global_trade_hq(materials, material_priorities, manager, device_id)


