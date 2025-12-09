import time

from simcity.bot.automation.find_material import find_material_in_global_trade_hq, find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
import logging

def find_trade_icon_in_daniel_city(device_id):
    logging.info('finding trade icon in daniel city')
    daniel_trade_icon = []
    while len(daniel_trade_icon) == 0:
        daniel_trade_icon, screenshot = find_miscellaneous_material(Miscellaneous.DANIEL_TRADE_ICON, device_id)
        if len(daniel_trade_icon) > 0:
            break
        time.sleep(1.5)
