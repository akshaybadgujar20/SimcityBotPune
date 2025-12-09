from enum import Enum

class CityAction(Enum):
    CONTINUOUS_BUY = "Continuous Buy"
    SELL_WITH_FULL_VALUE = "Sell with full value"
    SELL_WITH_ZERO_VALUE = "Sell with zero value"
    COLLECT_FROM_FACTORY = "Collect from factory"
    COLLECT_FROM_COMMERCIAL = "Collect from commercial"
    COLLECT_SOLD_ITEM_MONEY = "Collect sold item Money"
    ADVERTISE_ITEM_ON_TRADE_DEPOT = "Advertise item on trade depot"
    ADD_COMMERCIAL_MATERIAL_TO_PRODUCTION = "Add commercial to production"
    ADD_RAW_MATERIAL_TO_PRODUCTION = "Add raw material to production"