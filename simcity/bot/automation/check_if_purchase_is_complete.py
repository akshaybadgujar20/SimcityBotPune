import time

from simcity.bot.automation.find_material import find_material_in_global_trade_hq
from simcity.bot.enums.miscellaneous import Miscellaneous
import logging

def check_if_purchase_is_complete(device_id):
    logging.info('checking if purchase is complete or not')
    purchase_boxes = []
    while len(purchase_boxes) == 0:
        purchase_boxes = find_material_in_global_trade_hq(Miscellaneous.PURCHASE_COMPLETED.value, device_id)
        if len(purchase_boxes) > 0:
            break
        time.sleep(1.5)
