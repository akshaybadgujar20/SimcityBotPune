import logging

from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle
from simcity.bot.automation.click_on_daniel_face_and_goto_daniel_city import open_global_trade_hq_and_find_material, click_on_daniel_face_and_goto_daniel_city
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
from simcity.bot.enums.miscellaneous import Miscellaneous


def check_for_home_button(materials, material_priorities, manager, device_id):
    logging.info('Checking if home button is visible')
    home_icon, screenshot = find_miscellaneous_material(Miscellaneous.HOME, device_id)
    if len(home_icon) > 0:
        logging.info('home button is visible, checking for city name')
        city_name = take_screenshot_and_read_text(device_id, 715, 140, 1215, 245)
        daniel_city = ["daniel", "daniel's", "city", "daniel city", "daniel's city"]
        if any(item in city_name.lower() for item in daniel_city):
            logging.info('we are in daniel city, opening trade HQ')
            open_global_trade_hq_and_find_material(materials, material_priorities, manager, device_id)
        else:
            logging.info('we are in other city, clicking on friends icon')
            perform_click(65, 1015, device_id)
            click_on_daniel_face_and_goto_daniel_city(materials, material_priorities, 225, 865, manager, device_id)
    else:
        logging.info('we are in our own city')
        logging.info('finding friends icon')
        friends, screenshot = find_miscellaneous_material(Miscellaneous.FRIENDS, device_id)
        if len(friends) > 0:
            logging.info('friends icon found and clicking on it')
            perform_click_with_rectangle(friends[0], device_id)
            click_on_daniel_face_and_goto_daniel_city(materials, material_priorities, 545, 870, manager, device_id)
        else:
            logging.info('friends icon not found')