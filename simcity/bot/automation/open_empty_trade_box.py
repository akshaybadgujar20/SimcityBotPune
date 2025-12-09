import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle


def open_empty_trade_box(empty_trade_box, device_id):
    perform_click_with_rectangle(empty_trade_box, device_id)
    time.sleep(0.3)