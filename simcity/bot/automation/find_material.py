import logging

import cv2
import numpy as np

from simcity.bot.automation.apply_nsm import apply_nms_and_draw_rectangle
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.automation.take_template import take_template


def find_miscellaneous_material(material, device_id, threshold=0.8):
    template = take_template(material.value)
    return take_screenshot_and_perform_template_matching(material, template, device_id, threshold)

def find_material_in_city_storage(material, device_id, threshold=0.9):
    template = take_template(material.storage_template)
    return take_screenshot_and_perform_template_matching(material.name, template, device_id, threshold)

def find_material_in_global_trade_hq(material, device_id, threshold=0.9):
    template = take_template(material.hq_templates.base)
    return take_screenshot_and_perform_template_matching(material.name, template, device_id, threshold)

def find_material_in_trade_depot(material, device_id, threshold=0.9):
    template = take_template(material.depot_templates.base)
    return take_screenshot_and_perform_template_matching(material.name, template, device_id, threshold)

def take_screenshot_and_perform_template_matching(material_name, template, device_id, threshold):
    screenshot = take_bw_screenshot(device_id)
    return perform_matching(material_name, screenshot, template, threshold)

def perform_template_matching(screenshot, material_name, template, device_id, threshold):
    return perform_matching(material_name, screenshot, template, threshold)

def perform_matching(material_name, screenshot, template, threshold):
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    # Set a threshold for matching
    locations = np.where(result >= threshold)
    # Prepare data for Non-Maximum Suppression (NMS)
    rectangles = []
    for point in zip(*locations[::-1]):
        h, w = template.shape[:2]
        rect = [int(point[0]), int(point[1]), int(point[0] + w), int(point[1] + h)]
        rectangles.append(rect)
    if len(rectangles) == 0:
        logging.info(f'no rectangles found for {material_name}')
    matches = []
    if len(rectangles) > 0:
        matches = apply_nms_and_draw_rectangle(rectangles, threshold, screenshot)
    return matches, screenshot
