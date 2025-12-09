import re

import cv2
import logging
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.automation.take_screenshot_and_read_text import read_text_from_image


def draw_rectangle(device_id):
    screenshot = take_bw_screenshot(device_id)
    cv2.rectangle(screenshot, [285,435], [285,690], (0, 255, 0), 2)
    # cv2.rectangle(screenshot, [825,300], [930,400], (0, 255, 0), 2)
    output_path = 'output_image_with_rectangles.jpg'
    cv2.imwrite(output_path, screenshot)
    text = read_text_from_image(575, 400, 690, 300, screenshot)
    # text = read_text_from_image(825, 400, 930, 300, screenshot)
    numbers = re.findall(r'\d+\.?\d*', text)
    logging.info(f'numbers {numbers}')