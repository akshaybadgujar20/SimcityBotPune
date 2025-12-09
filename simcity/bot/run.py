import logging

from simcity.bot.automation.take_screenshot_and_read_text import read_text_from_image, take_screenshot_and_read_text
from simcity.bot.enums.material import Material
from simcity.bot.main import sell_materials, collect_sold_item_money, set_up, collect_produced_items_from_commercial_buildings, collect_raw_materials, \
    add_commercial_material_to_production
from simcity.bot.material_data_loader import load_material_info_data

materials = []
# device_id = "5705"
device_id = "5555"
set_up(device_id)
material_dict = load_material_info_data()
materials.append(material_dict[Material.GARDEN_GNOMES.value])
# sell_materials(materials, device_id, False, True, 1)
# collect_produced_items_from_commercial_buildings(11,device_id)
# add_commercial_material_to_production(materials, device_id)
# collect_raw_materials(12,device_id)
# collect_sold_item_money(0, device_id)

# take_screenshot_and_read_text(device_id, 690,105,1250,165)
take_screenshot_and_read_text(device_id, 370,840,1210,1070)

# material_dict = load_material_info_data()

# logging.info(material_dict)