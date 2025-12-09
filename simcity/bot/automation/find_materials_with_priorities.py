from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

from simcity.bot.automation.apply_nsm import apply_nms_and_draw_rectangle
from simcity.bot.automation.draw_rectangles_on_screenshot import draw_rectangles_on_screenshot
from simcity.bot.automation.take_screenshot import take_bw_screenshot
from simcity.bot.automation.take_template import take_template
from simcity.bot.material_data_loader import load_material_info_data

material_dict = load_material_info_data()

def find_material_using_thread(material_template_path, material_name, screenshot, threshold, nms_threshold, material_priorities, limit):
    template = take_template(material_template_path)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Find locations where matching exceeds the threshold
    locations = np.where(result >= threshold)

    # Collect rectangles for the current item
    rectangles = []
    h, w = template.shape[:2]
    for point in zip(*locations[::-1]):
        rect = [int(point[0]), int(point[1]), int(point[0] + w), int(point[1] + h)]
        rectangles.append(rect)
    if len(rectangles) > 0:
        # Apply NMS to the rectangles found for this item
        filtered_rectangles = apply_nms_and_draw_rectangle(rectangles, nms_threshold, screenshot)
    else:
        filtered_rectangles = []
    # Return rectangles with their priority
    priority = material_priorities[material_name]
    return [(rect, priority) for rect in filtered_rectangles][:limit]

def find_materials_with_priorities_in_global_trade_hq(materials, device_id, material_priorities, threshold=0.9, nms_threshold=0.6):
    # Take screenshot from the device
    screenshot = take_bw_screenshot(device_id)

    # Thread pool for running tasks concurrently
    all_rectangles = []
    with ThreadPoolExecutor() as executor:
        # Create a list of futures for each item being processed in a separate thread
        futures = [
            executor.submit(find_material_using_thread, material_dict.get(material).hq_templates.base, material_dict.get(material).name, screenshot, threshold, nms_threshold, material_priorities, 9)
            for material in materials
        ]
        # Collect the results (rectangles and their priorities) once they are done
        for future in futures:
            rectangles_with_priority = future.result()
            all_rectangles.extend(rectangles_with_priority)

    return sort_and_return_rectangles(all_rectangles, screenshot)

def find_materials_with_priorities_in_trade_depot(materials, device_id, material_priorities, threshold=0.9, nms_threshold=0.6):
    # Take screenshot from the device
    screenshot = take_bw_screenshot(device_id)

    # Thread pool for running tasks concurrently
    all_rectangles = []
    with ThreadPoolExecutor() as executor:
        # Create a list of futures for each item being processed in a separate thread
        futures = [
            executor.submit(find_material_using_thread, material_dict.get(material).depot_templates.base, material_dict.get(material).name, screenshot, threshold, nms_threshold, material_priorities, 3)
            for material in materials
        ]
        # Collect the results (rectangles and their priorities) once they are done
        for future in futures:
            rectangles_with_priority = future.result()
            all_rectangles.extend(rectangles_with_priority)

    return sort_and_return_rectangles(all_rectangles, screenshot)



def sort_and_return_rectangles(all_rectangles, screenshot):
    # Sort all rectangles based on priority
    all_rectangles.sort(key=lambda x: x[1])  # Sort by priority (second element in tuple)
    # Extract sorted rectangles
    sorted_rectangles = [rect for rect, priority in all_rectangles]
    draw_rectangles_on_screenshot(sorted_rectangles, screenshot, 'output_image.png')
    return sorted_rectangles, screenshot