from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_click, perform_swipe
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.trade_depot import check_if_trade_depot_open, find_and_open_trade_depot
import logging
import time

from simcity.bot.enums.miscellaneous import Miscellaneous


def advertise_all_items_on_trade_depot(iteration, device_id, stop_event):
    if stop_event.is_set():
        return

    is_trade_depot_open = check_if_trade_depot_open(device_id)
    if not is_trade_depot_open:
        logging.info('trade depot is not open, finding and opening it')
        find_and_open_trade_depot(device_id)

    logging.info('trade depot is open')
    logging.info(f'iteration {iteration}')

    if iteration == 5:
        return

    logging.info('finding sold items')
    advertised_items, screenshot = find_miscellaneous_material(
        Miscellaneous.TRADE_DEPOT_COIN,
        device_id
    )

    if len(advertised_items) > 0:
        for index, sold_item in enumerate(advertised_items):

            if stop_event.is_set():
                return

            perform_click_with_rectangle(sold_item, device_id)

            advertised_icon, screenshot = find_miscellaneous_material(
                Miscellaneous.ADVERTISE_ICON,
                device_id
            )

            if len(advertised_icon) > 0:
                perform_click_with_rectangle(advertised_icon[0], device_id)
                perform_click(1280, 60, device_id)

                logging.info('waiting for 60s')

                for _ in range(60):
                    if stop_event.is_set():
                        return
                    time.sleep(1)
            else:
                perform_click(1280, 60, device_id)
                continue

        logging.info('scrolling horizontally for next page')
        perform_swipe(1500, 550, 360, 550, 1000, device_id)

    else:
        perform_swipe(1500, 550, 360, 550, 1000, device_id)

    advertise_all_items_on_trade_depot(iteration + 1, device_id, stop_event)