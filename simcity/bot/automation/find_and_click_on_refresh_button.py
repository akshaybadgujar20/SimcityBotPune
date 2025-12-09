import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle
from simcity.bot.automation.find_material import find_material_in_global_trade_hq, find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
import logging

is_find_and_click_on_refresh_button_running = True

def find_and_click_on_refresh_button_indefinitely(device_id):
    logging.info('finding refresh button indefinitely')
    refresh_button = []
    while len(refresh_button) == 0:
        if is_find_and_click_on_refresh_button_running:
            refresh_button, screenshot = find_miscellaneous_material(Miscellaneous.REFRESH, device_id)
            time.sleep(1.5)
    perform_click_with_rectangle(refresh_button[0], device_id)

def stop_refresh_task(is_running):
    global is_find_and_click_on_refresh_button_running
    is_find_and_click_on_refresh_button_running = is_running