import logging
import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_click
from simcity.bot.automation.find_material import find_material_in_global_trade_hq
from simcity.bot.enums.material import Material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up
from simcity.bot.material_data_loader import load_material_info_data
import uiautomator2 as u2
materials = []
# device_id = "5705"
device_id = "5555"
set_up(device_id)
# material_dict = load_material_info_data()
# materials.append(material_dict[Material.SILK.value])
# sell_materials(materials, device_id, False, True, 1)
# collect_produced_items_from_commercial_buildings(11,device_id)
# add_commercial_material_to_production(materials, device_id)
# collect_raw_materials(12,device_id)
# collect_sold_item_money(0, device_id)

# take_screenshot_and_read_text(device_id, 690,105,1250,165)

# material_dict = load_material_info_data()

device = u2.connect(f"127.0.0.1:{device_id}")
device.swipe(190, 500, 1600, 500, 0.5)
time.sleep(1)
device.swipe(360, 380, 1200, 815, 0.5)

# add new home
device.swipe(500, 870, 960, 540, 0.5)

# click on green confirm button
perform_click(1260,665,device_id)
# close home menu
perform_click(1835,900,device_id)