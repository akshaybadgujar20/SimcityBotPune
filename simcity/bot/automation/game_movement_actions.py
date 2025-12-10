from simcity.bot.automation.adb_actions import perform_swipe


def swipe_top_right(device_id):
    # bottom left to top right
    perform_swipe(1700, 165, 630, 815, 500, device_id)

def swipe_top_right_halfway(device_id):
    # bottom left to top right
    perform_swipe(1700, 165, 960, 540, 500, device_id)

def swipe_bottom_left(device_id):
    # top right to bottom left
    perform_swipe(630, 815, 1700, 165, 500, device_id)

def swipe_right(device_id):
    # left to right
    perform_swipe(1700, 540, 300, 540, 500, device_id)

def swipe_left(device_id):
    # left to right
    perform_swipe(300, 540, 1700, 540, 500, device_id)

def swipe_up(device_id):
    # top to bottom
    perform_swipe(960, 120, 960, 880, 500, device_id)

def swipe_down(device_id):
    # bottom to top
    perform_swipe(960, 880, 960, 120, 500, device_id)