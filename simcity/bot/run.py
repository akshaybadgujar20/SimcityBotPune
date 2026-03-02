import logging
import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle
from simcity.bot.automation.find_material import find_material_in_global_trade_hq
from simcity.bot.enums.material import Material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up
from simcity.bot.material_data_loader import load_material_info_data

materials = []
# device_id = "5705"
device_id = "5575"
set_up(device_id)
material_dict = load_material_info_data()
materials.append(material_dict[Material.SILK.value])
# sell_materials(materials, device_id, False, True, 1)
# collect_produced_items_from_commercial_buildings(11,device_id)
# add_commercial_material_to_production(materials, device_id)
# collect_raw_materials(12,device_id)
# collect_sold_item_money(0, device_id)

# take_screenshot_and_read_text(device_id, 690,105,1250,165)

material_dict = load_material_info_data()

founded_materials, screenshot = find_material_in_global_trade_hq(materials[0], device_id)
if len(founded_materials) >= 1:
    perform_click_with_rectangle(founded_materials[0], device_id)
    time.sleep(5)