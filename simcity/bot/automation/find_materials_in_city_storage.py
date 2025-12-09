from simcity.bot.automation.find_material import find_material_in_city_storage


def find_materials_in_city_storage(materials, device_id):
    founded_item_list = []
    for material in materials:
        found_item, screenshot = find_material_in_city_storage(material, device_id)
        if len(found_item) > 0:
            founded_item_list.append(found_item[0])
    return founded_item_list