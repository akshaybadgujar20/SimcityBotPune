import logging
import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe, perform_click


def sell_material(material, device_id, advertise, full_price, duration=1000):
    perform_click_with_rectangle(material, device_id)
    if not advertise:
        perform_click(1610, 675, device_id)
    if full_price:
        # increase price
        perform_swipe(1610, 540, 1610, 540, 1200, device_id)
    else:
        # decrease price
        perform_swipe(1370, 540, 1370, 540, duration, device_id)
    # increase quantity
    perform_swipe(1610, 375, 1610, 375, 1200, device_id)
    # click on sell button
    perform_click(1485, 770, device_id)
    time.sleep(1)