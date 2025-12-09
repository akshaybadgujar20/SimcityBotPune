from simcity.bot.automation.adb_actions import perform_click, perform_click_with_rectangle
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous


def check_if_close_button_visible(device_id):
    founded_items, screenshot = find_miscellaneous_material(Miscellaneous.CLOSE, device_id)
    if len(founded_items) > 0:
        perform_click_with_rectangle(founded_items,device_id)