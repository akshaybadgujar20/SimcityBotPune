import os
import time
import logging

from simcity.bot.automation.adb_actions import press_esc_key


def close_trade_depot(device_id):
    logging.info('closing trade depot')
    press_esc_key(device_id)
    time.sleep(1)
