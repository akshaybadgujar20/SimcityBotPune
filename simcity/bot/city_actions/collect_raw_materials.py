import logging
import time

from simcity.bot.automation.adb_actions import perform_click


def collect_raw_materials(no_of_factories, device_id, stop_event):
    perform_click(500, 140, device_id)
    time.sleep(0.5)
    for i in range(no_of_factories):
        if stop_event.is_set():
            break
        logging.info(f'Inside factory no {i + 1}')
        perform_click(375, 1025, device_id)
        perform_click(595, 1025, device_id)
        perform_click(810, 1025, device_id)
        perform_click(1030, 1025, device_id)
        perform_click(1240, 1025, device_id)
        time.sleep(0.5)
        perform_click(500, 140, device_id)
