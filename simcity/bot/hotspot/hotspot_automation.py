import logging
import time
import uiautomator2 as u2
from simcity.bot.automation.adb_actions import perform_click, perform_swipe, perform_click_with_rectangle
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up

device_id = '5555'
d = u2.connect("127.0.0.1:5555")

def perform_automation():
    set_up(device_id)
    for i in range(500):
        logging.info('Clicking on home icon')
        perform_click(1720, 1010, device_id)
        # wait for sometime
        logging.info('Waiting for 0.5 seconds')
        time.sleep(1)
        # click on home and drag it to point 2
        logging.info('Creating new building')
        # perform_swipe(490, 900, 950, 540, 1, device_id)
        d.drag(490, 900, 950, 540, duration=0.2)
        #build home
        confirm_icon, screenshot = find_miscellaneous_material(Miscellaneous.CONFIRM_ICON, device_id)
        if len(confirm_icon) > 0:
            logging.info('confirm_icon icon found and clicking on it')
            perform_click_with_rectangle(confirm_icon[0], device_id)
        else:
            logging.info('confirm_icon icon not found stopping automation')
            break
        time.sleep(1)
        # close home menu
        logging.info('Clicking on close home menu icon')
        perform_click(1835, 995, device_id)
        # wait for some time
        logging.info('Waiting for 7 seconds')
        time.sleep(7)
        # search for contruction hat and click on it
        logging.info('Finding contruction hat icon')
        contruction_hat, screenshot = find_miscellaneous_material(Miscellaneous.CONTRUCTION_HAT, device_id)
        if len(contruction_hat) > 0:
            logging.info('contruction_hat icon found and clicking on it')
            perform_click_with_rectangle(contruction_hat[0], device_id)
        else:
            logging.info('contruction_hat icon not found stopping automation')
            break
        time.sleep(1)
        # click and hold b
        # upgrade building
        logging.info('Upgrading building')
        # perform_swipe(635, 485, 950, 540, 1, device_id)
        d.drag(635, 485, 950, 540, duration=0.3)
        # wait for some time
        logging.info('Waiting for 11 seconds')
        time.sleep(11)
        # click and hold building
        logging.info('Opening building menu')
        # perform_swipe(950, 540, 950, 540, 1, device_id)
        d.touch.down(950, 540)
        d.sleep(2)
        # click on delete
        time.sleep(2)
        logging.info('Clicking on delete')
        perform_click(1835, 430, device_id)
        # confirm on yes
        time.sleep(1)
        logging.info('Clicking on confirm delete button')
        perform_click(1140, 730, device_id)
        time.sleep(5)

perform_automation()