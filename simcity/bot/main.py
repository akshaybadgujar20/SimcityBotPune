import pytesseract

from simcity.bot.automation.check_adb_devices_and_connect_if_not_connected import \
    check_adb_devices_and_connect_if_not_connected
from simcity.bot.logger import setup_logging
from simcity.bot.material_data_loader import load_material_info_data
from simcity.bot.time_manager import TimerManager

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

manager = TimerManager()

is_sell_materials_running = True
is_collect_sold_item_money_running = True
is_advertise_all_item_from_trade_depot_running = True
is_collect_raw_materials_running = True
is_add_raw_material_to_production_running = True
is_add_commercial_material_to_production_running = True
is_collect_produced_items_from_commercial_buildings_running = True

material_dict = load_material_info_data()

def set_up(device_id):
    setup_logging()
    check_adb_devices_and_connect_if_not_connected(device_id)
