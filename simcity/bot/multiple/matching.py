import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from simcity.bot.automation.apply_nsm import apply_nms
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.automation.take_template import take_template

device_id = '5555'


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
        print(f'no rectangles found for {material_name}')
    matches = []
    if len(rectangles) > 0:
        matches = apply_nms(rectangles, threshold, screenshot)
    return matches

# Preprocessing function (e.g., convert to grayscale, edge detection)
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges


templates_path = [
    'city_storage/raw_materials/glass.png',
    'city_storage/raw_materials/plastic.png',
    'city_storage/raw_materials/minerals.png',
    'city_storage/raw_materials/chemicals.png',
    'city_storage/raw_materials/seeds.png',
    'city_storage/raw_materials/metal.png',
    'city_storage/raw_materials/wood.png'
]



# Function to pass the screenshot and templates for each match in parallel
def process_template(template_path):
    template = take_template(template_path)
    return perform_matching(template_path, screenshot, template, 0.9)

def perform_all_template_matching():
    start_time = time.time()
    # Use ThreadPoolExecutor to parallelize template matching
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_template, templates_path))

    # Aggregate all the results (matches) and draw them on the screenshot
    for match_points in results:
        for rect in match_points:
            top_left = (rect[0], rect[1])
            bottom_right = (rect[2], rect[3])
            cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
    end_time = time.time()
    print(f'total time: {end_time - start_time}')
    output_path = 'output_with_all_matches.jpg'
    cv2.imwrite(output_path, screenshot)

screenshot = take_bw_screenshot(device_id)
perform_all_template_matching()