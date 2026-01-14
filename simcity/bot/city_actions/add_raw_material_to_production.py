import time

import uiautomator2 as u2

from simcity.bot.automation.adb_actions import perform_click

def add_raw_material_to_production(material, no_of_factories, device_id, stop_event):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    device = u2.connect('127.0.0.1:' + device_id)
    for i in range(no_of_factories):
        if stop_event.is_set():
            break
        device.swipe_points([(material.x_location, material.y_location),(380, 935),(1260, 1000)],duration=0.2)
        time.sleep(0.1)
        perform_click(500, 140, device_id)
        time.sleep(0.5)
