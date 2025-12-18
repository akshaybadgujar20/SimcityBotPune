import time

from simcity.bot.automation.adb_actions import perform_click
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous


def click_on_back_button(device_id):
    perform_click(100, 975, device_id)

def click_on_material_storage(device_id):
    perform_click(65, 250, device_id)

def click_on_home_button(device_id):
    perform_click(95, 85, device_id)

def click_on_regions_button(device_id):
    perform_click(330, 890, device_id)

def add_item_to_factory_production(device, x1,y1,x2,y2,x3,y3):
    device.swipe_points([(x1, y1), (x2, y2), (x3, y3)], duration=0.2)

def click_on_limestone_cliff(device_id):
    perform_click(950, 705, device_id)

def click_on_green_valley(device_id):
    perform_click(665, 540, device_id)

def click_on_purchase_menu(device_id):
    perform_click(1840, 195, device_id)

def click_on_best_value_menu(device_id):
    perform_click(180,195, device_id)

def click_on_global_trade_hq(device_id):
    perform_click(180, 345, device_id)

def click_on_own_trade_depot(device_id):
    perform_click(180, 625, device_id)

def click_on_city_storage(device_id):
    perform_click(625,775,device_id)

def click_on_own_material_storage(device_id):
    perform_click(510,775,device_id)

def check_if_i_reach_home(device_id):
    for i in range(15):
        home_trade_icon, screenshot = find_miscellaneous_material(Miscellaneous.HOME_TRADE_ICON, device_id)
        if len(home_trade_icon) > 0:
            break
        time.sleep(1)
        continue

def collect_all_items_from_factory(device_id):
    perform_click(375, 1025, device_id)
    perform_click(595, 1025, device_id)
    perform_click(810, 1025, device_id)
    perform_click(1030, 1025, device_id)
    perform_click(1240, 1025, device_id)

def check_if_regions_button_visible(device_id):
    regions, screenshot = find_miscellaneous_material(Miscellaneous.GO_TO_REGIONS_BUTTON, device_id)
    if len(regions) > 0:
        return True
    return False