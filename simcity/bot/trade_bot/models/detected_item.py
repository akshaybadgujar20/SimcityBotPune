from __future__ import annotations

from dataclasses import dataclass
from typing import List

from simcity.bot.trade_bot.models.purchase_item import PurchaseItem


@dataclass
class DetectedItem:
    purchase_item: PurchaseItem
    rect: List[int]
