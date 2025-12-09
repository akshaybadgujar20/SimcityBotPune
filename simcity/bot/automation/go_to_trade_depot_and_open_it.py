import time

from simcity.bot.automation.adb_actions import perform_swipe, perform_click


def go_to_trade_depot_and_open_it(device_id):
    for i in range(5):
        perform_swipe(600, 830, 1715, 150, 1000, device_id)
    perform_swipe(1715, 150, 0, 1080, 1000, device_id)
    time.sleep(0.2)
    perform_swipe(1250, 175, 1250, 975, 1000, device_id)
    time.sleep(0.2)
    perform_click(860,500, device_id)
    time.sleep(0.2)