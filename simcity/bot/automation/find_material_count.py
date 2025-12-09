import time

from simcity.bot.automation.find_material import find_miscellaneous_material
import logging

def find_material_count_for_given_iterations(material, device_id, duration=1.5):
    logging.info(f'finding material {material} count for given iterations')
    trade_boxes = []
    timer = 0.0
    while len(trade_boxes) == 0:
        trade_boxes, screenshot = find_miscellaneous_material(material, device_id)
        if len(trade_boxes) > 0:
            return len(trade_boxes)
        # reducing to 1
        time.sleep(1)
        timer += 1
        if timer > duration:
            return 0

def find_material_count_after_each_delay(material, device_id, delay=1):
    logging.info(f'finding material {material} count after each delay {delay}')
    trade_boxes = []
    timer = 0.0
    while len(trade_boxes) == 0:
        trade_boxes, screenshot = find_miscellaneous_material(material, device_id)
        if len(trade_boxes) > 0:
            return len(trade_boxes)
        time.sleep(delay)
        # reducing to 1
        timer += 1
        if timer > 30.0:
            return 0

def find_material_count_once(material, device_id):
    logging.info(f'finding material {material} count once')
    trade_boxes = []
    while len(trade_boxes) == 0:
        trade_boxes, screenshot = find_miscellaneous_material(material, device_id)
        if len(trade_boxes) > 0:
            return len(trade_boxes)
        return 0

def find_material_count_indefinitely(material, device_id):
    logging.info(f'finding material {material} count indefinite')
    trade_boxes = []
    timer = 0.0
    while len(trade_boxes) == 0:
        trade_boxes, screenshot = find_miscellaneous_material(material, device_id)
        if len(trade_boxes) > 0:
            return len(trade_boxes)
        # reducing to 1
        timer = timer + 1