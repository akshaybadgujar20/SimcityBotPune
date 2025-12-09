import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe, perform_click


def sell_material(material, device_id, advertise, full_price, duration=1000):
    perform_click_with_rectangle(material, device_id)
    if not advertise:
        perform_click(1680, 840, device_id)
    if full_price:
        # increase price
        perform_swipe(1680, 650, 1680, 650, 1200, device_id)
    else:
        # decrease price
        perform_swipe(1360, 650, 1360, 650, duration, device_id)
    # increase quantity
    perform_swipe(1680, 430, 1680, 430, 1200, device_id)
    # click on sell button
    perform_click(1515, 995, device_id)
    time.sleep(1)