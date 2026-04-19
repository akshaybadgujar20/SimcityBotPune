import logging
import os
import time

import cv2

# screenshot_path = '..\\..\\..\\resources\\screenshots_3\\screenshot (32).png'  # Path to save the screenshot
# screenshot_path = 'C:\\Users\\Akshay\\Pictures\\BlueStacks\\Screenshot_2024.10.25_00.33.50.277.png'  # Path to save the screenshot

BASE_DIR = "screenshots"


def take_bw_screenshot(device_id):
    city_dir = os.path.join(BASE_DIR, f"city_{device_id}")
    os.makedirs(city_dir, exist_ok=True)

    screenshot_path = os.path.join(city_dir, "screenshot.png")
    screenshot_gray_path = os.path.join(city_dir, "screenshot_gray.jpg")

    # Take a screenshot from the Android device using ADB
    os.system(f"adb -s 127.0.0.1:{device_id} exec-out screencap -p > \"{screenshot_path}\"")
    # Load the screenshot and template images
    screenshot = cv2.imread(screenshot_path)
    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(screenshot_gray_path, screenshot_gray)
    return screenshot_gray

def take_color_screenshot(device_id):
    city_dir = os.path.join(BASE_DIR, f"city_{device_id}")
    os.makedirs(city_dir, exist_ok=True)

    screenshot_path = os.path.join(city_dir, "screenshot.png")
    screenshot_color_path = os.path.join(city_dir, "screenshot.jpg")

    # Take a screenshot from the Android device using ADB
    os.system(f"adb -s 127.0.0.1:{device_id} exec-out screencap -p > \"{screenshot_path}\"")
    # Load the screenshot and template images
    screenshot = cv2.imread(screenshot_path)
    cv2.imwrite(screenshot_color_path, screenshot)
    return screenshot