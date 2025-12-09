import time
import logging
import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click, perform_swipe, perform_click_with_rectangle
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up

device_id = '5575'
d = u2.connect("127.0.0.1:5575")

def perform_automation_0():
    set_up(device_id)
    for i in range(1000):
        # search for item
        perform_click(180,195, device_id)
        time.sleep(1)
        perform_click(170, 335, device_id)
        time.sleep(1)
        for i in range(10):
            coin, screenshot = find_miscellaneous_material(Miscellaneous.COIN, device_id)
            if len(coin) > 0:
                break
            continue

        recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
        if len(recycled_fabric) == 1:
            logging.info('recycled_fabric (1) icon found and clicking on it')
            perform_click_with_rectangle(recycled_fabric[0], device_id)
            time.sleep(10)
            buy_recycled_fabric()
        elif len(recycled_fabric) > 1:
            logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')
            perform_click_with_rectangle(recycled_fabric[0], device_id)
            time.sleep(10)
            buy_recycled_fabric()
            perform_click(170, 335, device_id)
            continue
        else:
            # swipe to right 1st time
            d.swipe(1575, 460, 620, 460, 0.5)
            recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
            if len(recycled_fabric) == 1:
                logging.info('recycled_fabric (1) icon found and clicking on it')
                perform_click_with_rectangle(recycled_fabric[0], device_id)
                time.sleep(10)
                buy_recycled_fabric()
            elif len(recycled_fabric) > 1:
                logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')
                perform_click_with_rectangle(recycled_fabric[0], device_id)
                time.sleep(10)
                buy_recycled_fabric()
                perform_click(170, 335, device_id)
                continue
            else:
                # swipe to right 2nd time
                d.swipe(1575, 460, 620, 460, 0.5)
                recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
                if len(recycled_fabric) == 1:
                    logging.info('recycled_fabric (1) icon found and clicking on it')
                    perform_click_with_rectangle(recycled_fabric[0], device_id)
                    time.sleep(10)
                    buy_recycled_fabric()
                elif len(recycled_fabric) > 1:
                    logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')
                    perform_click_with_rectangle(recycled_fabric[0], device_id)
                    time.sleep(10)
                    buy_recycled_fabric()
                    perform_click(170, 335, device_id)
                    continue
                else:
                    # swipe to right 3rd time
                    d.swipe(1575, 460, 620, 460, 0.5)
                    recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC, device_id)
                    if len(recycled_fabric) == 1:
                        logging.info('recycled_fabric (1) icon found and clicking on it')
                        perform_click_with_rectangle(recycled_fabric[0], device_id)
                        time.sleep(10)
                        buy_recycled_fabric()
                    elif len(recycled_fabric) > 1:
                        logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')
                        perform_click_with_rectangle(recycled_fabric[0], device_id)
                        time.sleep(10)
                        buy_recycled_fabric()
                        perform_click(170, 335, device_id)
                        continue
                    else:
                        logging.info("nothing found waiting for 25 second")
                        time.sleep(25)

def buy_recycled_fabric():
    recycled_fabric, screenshot = find_miscellaneous_material(Miscellaneous.RECYCLED_FABRIC_2, device_id)
    if len(recycled_fabric) == 1:
        logging.info('recycled_fabric (1) icon found and clicking on it')
        perform_click_with_rectangle(recycled_fabric[0], device_id)
    elif len(recycled_fabric) > 1:
        logging.info('recycled_fabric (More than 1) icon found and clicking on all one by one')
        for recycled_fabric_data in recycled_fabric:
            perform_click_with_rectangle(recycled_fabric_data[0], device_id)
    else:
        logging.info('recycled_fabric (More than 1) icon found and clicking on 1st it')


set_up(device_id)
perform_automation_0()