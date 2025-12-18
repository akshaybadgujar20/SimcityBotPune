from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.enums.miscellaneous import Miscellaneous
from simcity.bot.main import set_up

device_id = '5555'
set_up(device_id)
find_miscellaneous_material(Miscellaneous.EMPTY_TRADE_BOXES,device_id)