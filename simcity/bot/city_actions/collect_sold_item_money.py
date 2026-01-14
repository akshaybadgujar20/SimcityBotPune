from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.trade_depot import check_if_trade_depot_open, find_and_open_trade_depot
import logging

from simcity.bot.enums.miscellaneous import Miscellaneous


def collect_sold_item_money(iteration, device_id, stop_event):
    if stop_event.is_set():
        return

    is_trade_depot_open = check_if_trade_depot_open(device_id)
    if not is_trade_depot_open:
        logging.info('trade depot is not open, finding and opening it')
        find_and_open_trade_depot(device_id)

    logging.info('trade depot is open')
    logging.info(f'iteration {iteration}')

    if iteration == 4:
        return

    logging.info('finding sold items')
    sold_items, screenshot = find_miscellaneous_material(
        Miscellaneous.CITY_STORAGE_PURCHASE_COMPLETED,
        device_id
    )

    if len(sold_items) > 0:
        for index, sold_item in enumerate(sold_items):

            if stop_event.is_set():
                return

            perform_click_with_rectangle(sold_item, device_id)

        collect_sold_item_money(iteration + 1, device_id, stop_event)

    else:
        perform_swipe(1500, 550, 360, 550, 1000, device_id)
        collect_sold_item_money(iteration + 1, device_id, stop_event)
