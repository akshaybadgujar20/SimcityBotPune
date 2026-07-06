import logging
import os
import time
from pathlib import Path

import cv2

# Repo root / ``screenshots`` so concurrent API workers (different cwd) still isolate by device.
_REPO_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = str(_REPO_ROOT / "screenshots")


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