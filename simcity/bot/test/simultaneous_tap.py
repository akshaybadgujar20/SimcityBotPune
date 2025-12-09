import subprocess
import threading
import time

import cv2

from simcity.bot.automation.take_screenshot_and_read_text import read_text_from_image


def tap_and_hold(x,y):
    # Simulate a tap and hold (2 seconds)
    subprocess.run(["adb", "-s", "127.0.0.1:5555", "shell", "input", "swipe", str(x), str(y), str(x), str(y), "2000"])

def take_bw_screenshot():
    time.sleep(0.5)  # Wait for the hold action to start
    # Capture a screenshot
    with open("requirement.png", "wb") as f:
        subprocess.run(["adb", "-s", "127.0.0.1:5555", "exec-out", "screencap", "-p"], stdout=f)

def perform_tap_and_screenshot():
    """
    Performs a tap and hold action and takes a screenshot in parallel.

    Parameters:
        x (int): The x-coordinate of the tap.
        y (int): The y-coordinate of the tap.
        duration_ms (int): The duration of the tap in milliseconds.
        screenshot_filename (str): The name of the file to save the screenshot to.
    """

    tap_thread = threading.Thread(target=tap_and_hold, args=(670, 375))
    screenshot_thread = threading.Thread(target=take_bw_screenshot)

    tap_thread.start()
    screenshot_thread.start()

    tap_thread.join()
    screenshot_thread.join()

# Execute the function
if __name__ == "__main__":
    try:
        perform_tap_and_screenshot()
        print("Screenshot captured and processed successfully.")

    except Exception as e:
        print(f"Error: {e}")
    # Load the screenshot image
    screenshot = cv2.imread("requirement.png")

    # Ensure the image was loaded successfully
    if screenshot is None:
        raise FileNotFoundError(f"Failed to load screenshot from requirement.png Check the device and ADB connection.")

    # Convert the screenshot to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Save the grayscale screenshot
    cv2.imwrite("requirement_gray.png", screenshot_gray)
    read_text_from_image(820, 400, 1340, 450, screenshot_gray)
