from __future__ import annotations

from types import SimpleNamespace

from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.trade_bot.models.purchase_item import PurchaseItem


def material_facade_for(purchase_item: PurchaseItem):
    """Builds the extra fields needed to buy from a visiting mayor’s depot."""
    info = load_material_info_data()[purchase_item.material.name]
    return SimpleNamespace(
        name=purchase_item.material.name,
        depot_templates=info.depot_templates,
        hq_templates=info.hq_templates,
    )
