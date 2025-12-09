# Function to read JSON files and populate trade_data_dict
import json
import os
from typing import Dict
from pathlib import Path

from simcity.bot.enums.material import Material
from simcity.bot.material_info import MaterialInfo, HqTemplates, DepotTemplates

material_info_dict = {}

def load_material_info_data() -> Dict[str, MaterialInfo]:
    directory = get_json_path()
    if len(material_info_dict)==0:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    items = json.load(file)

                    for item in items:
                        # Convert item name to Material type
                        material_name = Material[item['name'].upper()]  # Adjust as necessary
                        hq_templates = HqTemplates(**item['hq_templates'])
                        depot_templates = DepotTemplates(**item['depot_templates'])

                        material_info = MaterialInfo(
                            name=material_name,
                            x_location=item['x_location'],
                            y_location=item['y_location'],
                            hq_templates=hq_templates,
                            depot_templates=depot_templates,
                            base_price=item['base_price'],
                            actual_price=item['actual_price'],
                            storage_template=item['storage_template'],
                            sell_duration=item['sell_duration'],
                            building_name=item['building_name']
                        )
                        material_info_dict[material_info.name.name] = material_info  # Store by material name
    # Save material_info_dict to JSON, converting MaterialInfo to a dictionary
    with open('data.json', 'w') as json_file:
        json.dump({key: material.to_dict() for key, material in material_info_dict.items()}, json_file, indent=2)
    return material_info_dict

def get_json_path():
    # Get the directory where the current script is located
    script_dir = Path(__file__).resolve().parent

    # Construct the full path to the resources directory
    # Assuming 'resources' is located at the same level as the 'simcity' folder
    project_root = script_dir.parent.parent  # Go up two levels to reach the project root
    resources_dir = project_root / 'resources'

    # Create the full image path by joining the resources dir with the relative path
    image_path = resources_dir / 'material_data'

    # Resolve the absolute path
    return image_path.resolve()

