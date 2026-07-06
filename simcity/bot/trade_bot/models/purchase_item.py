from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

from simcity.bot.enums.material import Material
from simcity.bot.material_data_loader import load_material_info_data


def purchase_items_from_specs(
    specs: Sequence[Mapping[str, Any]],
) -> list[PurchaseItem]:
    """Turn API/JSON rows into shopping-list entries.

    Each row needs ``material`` (name as text) and ``priority`` (number);
    optional ``name`` and ``template_path``.
    """
    out: list[PurchaseItem] = []
    for row in specs:
        material_key = str(row["material"]).strip().upper()
        material = Material[material_key]
        name = str(row.get("name") or material_key)
        priority = int(row["priority"])
        template_path = row.get("template_path")
        if template_path is not None:
            template_path = str(template_path).strip() or None
        out.append(
            PurchaseItem(
                name=name,
                priority=priority,
                material=material,
                template_path=template_path,
            )
        )
    return out


@dataclass
class PurchaseItem:
    name: str
    priority: int
    material: Material
    template_path: Optional[str] = None

    def resolved_hq_template_path(self) -> str:
        if self.template_path:
            return self.template_path
        info = load_material_info_data()[self.material.name]
        return info.hq_templates.base
