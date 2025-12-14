import os
import time


def perform_click_with_rectangle(match, device_id):
    # Calculate the center of the rectangle for tapping
    center_x = match[0] + ((match[2] - match[0]) // 2)
    center_y = match[1] + ((match[3] - match[1]) // 2)
    print(f"Found image at: {match}")
    # Tap on the location using ADB (optional)
    os.system(f"adb -s 127.0.0.1:{device_id} shell input tap {center_x} {center_y}")

def perform_click(x,y, device_id):
    # Tap on the location using ADB (optional)
    os.system(f"adb -s 127.0.0.1:{device_id} shell input tap {x} {y}")

def perform_swipe(x1, y1, x2, y2, duration, device_id):
    # Tap on the location using ADB (optional)
    os.system(f"adb -s 127.0.0.1:{device_id} shell input swipe {x1} {y1} {x2} {y2} {duration}")

def press_esc_key(device_id):
    os.system(f"adb -s 127.0.0.1:{device_id} shell input keyevent 111")


def adb_long_press_drag(device_id, x1, y1, x2, y2, hold_ms=500, drag_ms=200):
    # long press (touch down + hold)
    os.system(f"adb -s {device_id} shell input touchscreen swipe {x1} {y1} {x1} {y1} {hold_ms}")

    # small delay to ensure hold is registered
    time.sleep(hold_ms / 1000.0)

    # drag from start to end
    os.system(f"adb -s {device_id} shell input touchscreen swipe {x1} {y1} {x2} {y2} {drag_ms}")
