import logging
from simcity.bot.enums.material import Material
from simcity.bot.main import set_up
from simcity.bot.trade_bot import PurchaseItem, run_trade_session

logging.basicConfig(level=logging.INFO)

items = [
    PurchaseItem(name="STORAGE_BARS", priority=1, material=Material.STORAGE_BARS),
    PurchaseItem(name="STORAGE_LOCK", priority=2, material=Material.STORAGE_LOCK),
    PurchaseItem(name="STORAGE_CAMERA", priority=3, material=Material.STORAGE_CAMERA),
]
set_up('5605')
run_trade_session("5605", items)