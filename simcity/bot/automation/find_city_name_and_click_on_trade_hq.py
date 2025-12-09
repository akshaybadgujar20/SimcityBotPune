from simcity.bot.automation.adb_actions import perform_click
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
import logging

def find_city_name_and_click_on_trade_hq(device_id, left=630, upper=245, right=960, lower=340):
    logging.info('finding city name to click on trade HQ')
    city_name: str = take_screenshot_and_read_text(device_id, left,upper, right, lower)
    capital_city = ["capital", "city", "capital city"]
    green_valley = ["green", "valley", "green valley"]
    sunny_isles = ["sunny", "isles", "sunny isles"]
    limestone_cliff = ["limestone", "cliffs", "limestone cliffs"]
    cactus_canyon = ["cactus", "canyon", "cactus_canyon"]
    if any(item in city_name.lower() for item in capital_city):
        # perform_click(1400, 650, device_id)
        perform_click(1550, 850, device_id)
    elif any(item in city_name.lower() for item in green_valley):
        # perform_click(480, 900, device_id)
        perform_click(410, 990, device_id)
    elif any(item in city_name.lower() for item in sunny_isles):
        perform_click(620, 385, device_id)
    elif any(item in city_name.lower() for item in limestone_cliff):
        perform_click(465, 625, device_id)
    elif any(item in city_name.lower() for item in cactus_canyon):
        # perform_click(370, 240, device_id)
        perform_click(290, 150, device_id)
    else:
        perform_click(750, 450, device_id)

