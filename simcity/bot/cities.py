from simcity.bot.enums.city_actions import CityAction
from simcity.bot.enums.city_names import CityNames
from simcity.bot.main import add_commercial_material_to_production, add_raw_material_to_production

from simcity.bot.material_data_loader import load_material_info_data


def get_cities():
    materials_data = load_material_info_data()
    material_list = []
    for material in materials_data:
        material_list.append(material)
    from simcity.bot.main import buy_items, collect_raw_materials, sell_materials, collect_produced_items_from_commercial_buildings, \
        collect_sold_item_money
    actions_values = [
        {"name": CityAction.CONTINUOUS_BUY, "function_call": buy_items},
        {"name": CityAction.SELL_WITH_FULL_VALUE, "function_call": sell_materials},
        {"name": CityAction.SELL_WITH_ZERO_VALUE, "function_call": sell_materials},
        {"name": CityAction.COLLECT_FROM_FACTORY, "function_call": collect_raw_materials},
        {"name": CityAction.COLLECT_FROM_COMMERCIAL, "function_call": collect_produced_items_from_commercial_buildings},
        {"name": CityAction.COLLECT_SOLD_ITEM_MONEY, "function_call": collect_sold_item_money},
        {"name": CityAction.ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION, "function_call": add_commercial_material_to_production},
        {"name": CityAction.ADD_RAW_MATERIAL_TO_PRODUCTION, "function_call": add_raw_material_to_production},
        {"name": CityAction.ADVERTISE_ITEM_ON_TRADE_DEPOT, "function_call": ""}
    ];

    # City buttons (replace with your city names)
    cities = [
        {"name": CityNames.BASE_CITY.value, "port": "5555", "actions": actions_values, "materials":material_list, "no_of_factories":12,
         "no_of_commercial_buildings":15},
        {"name": CityNames.BARLEYCORN_POINT.value, "port": "5895", "actions": actions_values, "materials":material_list, "no_of_factories":9, "no_of_commercial_buildings":7},
        {"name": CityNames.SUNSHINE_VALLEY.value, "port": "6135", "actions": actions_values, "materials":material_list, "no_of_factories":9, "no_of_commercial_buildings":7},
        {"name": CityNames.TRADERS_RIDGE.value, "port": "5915", "actions": actions_values, "materials":material_list, "no_of_factories":7,
         "no_of_commercial_buildings":7},
        {"name": CityNames.MAGNOLIA_WETLANDS.value, "port": "5925", "actions": actions_values, "materials":material_list, "no_of_factories":12, "no_of_commercial_buildings":15},
        {"name": CityNames.HOKUSAI_CLIFFS.value, "port": "6025", "actions": actions_values, "materials":material_list, "no_of_factories":12, "no_of_commercial_buildings":15},
        {"name": CityNames.NAUTILUS_PLATEAU.value, "port": "5945", "actions": actions_values, "materials":material_list, "no_of_factories":12, "no_of_commercial_buildings":15},
        {"name": CityNames.PETROL_BAY.value, "port": "5955", "actions": actions_values, "materials":material_list, "no_of_factories":12,
         "no_of_commercial_buildings":15},
        {"name": CityNames.GRAND_HAVEN.value, "port": "5965", "actions": actions_values, "materials":material_list, "no_of_factories":12,
         "no_of_commercial_buildings":15},
        {"name": CityNames.JUGBAND_HILLS.value, "port": "5985", "actions": actions_values, "materials":material_list, "no_of_factories":12, "no_of_commercial_buildings":15},
        {"name": CityNames.COTTONWOOD_FOREST.value, "port": "6005", "actions": actions_values, "materials":material_list, "no_of_factories":12, "no_of_commercial_buildings":15},
    ]

    # # City buttons (replace with your city names)
    # cities = [
    #     {"name": "Base City", "port": 5555, "actions": actions_values},
    #     {"name": "Barleycorn Point", "port": 5895, "actions": actions_values},
    #     {"name": "Sunshine Valley", "port": 5905, "actions": actions_values},
    #     {"name": "Traders Ridge", "port": 5915, "actions": actions_values},
    #     {"name": "Magnolia Wetlands", "port": 5925, "actions": actions_values},
    #     {"name": "Hokusai Cliffs", "port": 6025, "actions": actions_values},
    #     {"name": "Nautilus Plateau", "port": 5945, "actions": actions_values},
    #     {"name": "Petrol Bay", "port": 5955, "actions": actions_values},
    #     {"name": "Grand Haven", "port": 5965, "actions": actions_values},
    #     {"name": "Jugband Hills", "port": 5985, "actions": actions_values},
    #     {"name": "Cottonwood Forest", "port": 6005, "actions": actions_values},
    # ]

    return cities

def get_city_name_by_port(port):
    """Find the city name based on the port."""
    for city in get_cities():
        if city['port'] == port:
            return city['name']
    return None  # Return None if no city is found for the given port