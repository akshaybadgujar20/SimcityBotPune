import logging
import time

from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle
from simcity.bot.automation.check_for_home_button import check_for_home_button
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.find_material_count import find_material_count_for_given_iterations, find_material_count_after_each_delay
from simcity.bot.automation.find_materials_on_global_trade_hq import find_coins_in_global_trade_hq
from simcity.bot.enums.miscellaneous import Miscellaneous


def check_for_close_button(materials, material_priorities, manager, device_id):
    logging.info('Checking if close button is visible')
    close_icon, screenshot = find_miscellaneous_material(Miscellaneous.CLOSE, device_id)
    if len(close_icon) > 0:
        logging.info(f'close button found {len(close_icon)}, finding refresh button now')
        refresh_button = find_material_count_for_given_iterations(Miscellaneous.REFRESH, device_id)
        if refresh_button > 0:
            start_timer_and_click_on_refresh_button(materials, material_priorities, manager, device_id)
        else:
            refresh_button_count = find_material_count_after_each_delay(Miscellaneous.REFRESH, device_id, 5)
            if refresh_button_count > 0:
                start_timer_and_click_on_refresh_button(materials, material_priorities, manager, device_id)
            else:
                logging.info(f'refresh, button not found for duration of 30 seconds, therefore closing trade depot')
                perform_click_with_rectangle(close_icon[0], device_id)
                time.sleep(1)
    else:
        logging.info(f'close button not found')
        check_for_home_button(materials, material_priorities, manager, device_id)


def start_timer_and_click_on_refresh_button(materials, material_priorities, manager, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    manager.start_timer(timer_name)
    logging.info(f'refresh button found, clicking on it')
    perform_click(965, 955, device_id)
    time.sleep(1)
    find_coins_in_global_trade_hq(materials, material_priorities, manager, device_id)