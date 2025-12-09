from dataclasses import dataclass, field
from typing import Dict, Any

from simcity.bot.enums.material import Material


@dataclass
class HqTemplates:
    base: str
    x1: str
    x2: str
    x3: str
    x4: str
    x5: str

@dataclass
class DepotTemplates:
    base: str
    x1: str
    x2: str
    x3: str
    x4: str
    x5: str

@dataclass
class MaterialInfo:
    name: Material
    x_location: int
    y_location: int
    hq_templates: HqTemplates
    depot_templates: DepotTemplates
    base_price: int
    actual_price: int
    storage_template: str
    sell_duration: int
    building_name: str
    manufacturing_recipes: Dict[str, Dict[str, int]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert MaterialInfo to a dictionary."""
        return {
            "name": self.name.name,
            "x_location": self.x_location,
            "y_location": self.y_location,
            "hq_templates": self.hq_templates.__dict__,
            "depot_templates": self.depot_templates.__dict__,
            "base_price": self.base_price,
            "actual_price": self.actual_price,
            "storage_template": self.storage_template,
            "sell_duration": self.sell_duration,
            "building_name": self.building_name,
            "manufacturing_recipes": self.manufacturing_recipes
        }