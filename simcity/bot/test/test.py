import time

from simcity.bot.automation.adb_actions import perform_swipe, perform_click_with_rectangle, perform_click
from simcity.bot.automation.game_movement_actions import swipe_up, swipe_down, swipe_right, swipe_right, swipe_left, swipe_top_right, swipe_bottom_left, swipe_top_right_halfway
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.take_screenshot import take_color_screenshot
from simcity.bot.automation.take_screenshot_and_read_text import read_text_from_image
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up, farm_nails
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.time_manager import TimerManager

device_id = '5555'
set_up(device_id)
manager = TimerManager()
# find_miscellaneous_material(Miscellaneous['IMG'],device_id)
materials =[]
material_priorities = {}

# import os
# print(f'{os.cpu_count()}')
# open_global_trade_hq_and_find_material(materials, material_priorities, manager, device_id)
# material_dict = load_material_info_data()
# buy_from_friends(material_dict.get(Material.STORAGE_CAMERA.value),'TRADER_RIDGE', device_id)

# Images

# Right
# take_screenshot_and_read_text(device_id,530,275,630, 385)
# take_screenshot_and_read_text(device_id,530,425,630, 535)
# take_screenshot_and_read_text(device_id,530,570,630, 680)

#  Left
# take_screenshot_and_read_text(device_id,270,345,370, 455)
# take_screenshot_and_read_text(device_id,270,490,370, 600)
# take_screenshot_and_read_text(device_id,275,650,375, 760)

# Quantity

# Right
# read_text_from_image(630,275,750, 385, screenshot)
# read_text_from_image(630,425,750, 535, screenshot)
# read_text_from_image(630,570,750, 680, screenshot)

# Left
# read_text_from_image(370,345,490, 455, screenshot)
# read_text_from_image(370,490,490, 600, screenshot)
# read_text_from_image(370,650,490, 760, screenshot)

# 2x
# perform_swipe(925, 850, 925, 330, 1000, device_id)
# 2x
# perform_swipe(925, 850, 925, 340, 1000, device_id)
# perform_swipe(925, 850, 925, 340, 1000, device_id)

# Images
# screenshot = take_color_screenshot(device_id)

# Row 1
# read_text_from_image(430,280,580, 430, screenshot)
# read_text_from_image(700,280,850, 430, screenshot)
# read_text_from_image(970,280,1120, 430, screenshot)
# read_text_from_image(1240,280,1390, 430, screenshot)
#
# Row 2
# read_text_from_image(430,450,580, 600, screenshot)
# read_text_from_image(700,450,850, 600, screenshot)
# read_text_from_image(970,450,1120, 600, screenshot)
# read_text_from_image(1240,450,1390, 600, screenshot)
#
# Row 3
# read_text_from_image(430,630,580, 780, screenshot)
# read_text_from_image(700,630,850, 780, screenshot)
# read_text_from_image(970,630,1120, 780, screenshot)
# read_text_from_image(1240,630,1390, 780, screenshot)

#  Quantity

# Row 1
# read_text_from_image(580,280,680, 430, screenshot)
# read_text_from_image(850,280,950, 430, screenshot)
# read_text_from_image(1120,280,1220, 430, screenshot)
# read_text_from_image(1390,280,1490, 430, screenshot)

# Row 2
# read_text_from_image(430,450,580, 600, screenshot)
# read_text_from_image(700,450,850, 600, screenshot)
# read_text_from_image(970,450,1120, 600, screenshot)
# read_text_from_image(1240,450,1390, 600, screenshot)

# Row 3
# read_text_from_image(430,630,580, 780, screenshot)
# read_text_from_image(700,630,850, 780, screenshot)
# read_text_from_image(970,630,1120, 780, screenshot)
# read_text_from_image(1240,630,1390, 780, screenshot)

# matches, screenshot = find_miscellaneous_material(Miscellaneous['EMPTY2'],device_id)
# print(f'matches {len(matches)}')
select_material_list = []
material_dict = load_material_info_data()
select_material_list.append(material_dict['NAILS'])
farm_nails(select_material_list,12,device_id)

# perform_swipe(center_x,center_y,960,350,1000,device_id)

# perform_swipe(center_x,center_y,960,700,1000,device_id)
# swipe_top_right(device_id)
# swipe_right(device_id)

# def bring_depot_factory_commercial_in_position():
#     matches = []
#     for i in range(7):
#         swipe_bottom_left(device_id)
#         time.sleep(0.5)
#         matches, screenshot = find_miscellaneous_material(Miscellaneous['CARGO_SHIP_ICON'], device_id)
#         if len(matches) > 0:
#             break
#     if len(matches) > 0:
#         return bring_trade_depot_in_position(matches[0], device_id)
#     else:
#         swipe_top_right(device_id)
#         swipe_top_right_halfway(device_id)
#         matches, screenshot = find_miscellaneous_material(Miscellaneous['CARGO_SHIP_ICON'], device_id)
#         return bring_trade_depot_in_position(matches[0], device_id)
#
# def bring_trade_depot_in_position(match, device_id):
#     center_x = match[0] + ((match[2] - match[0]) // 2)
#     center_y = match[1] + ((match[3] - match[1]) // 2)
#     perform_swipe(center_x, center_y, 800, 600, 500, device_id)
#
# def open_ad_factory():
#     match = bring_depot_factory_commercial_in_position()
#     time.sleep(0.5)
#     # perform_click(1400,880,device_id)
#     perform_click(1660,880,device_id)
#
# open_ad_factory()