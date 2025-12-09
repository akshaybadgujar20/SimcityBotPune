import pytesseract

from simcity.bot.parameters import get_materials, get_material_properties
from simcity.bot.main import buy_items, set_up

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

device_id = '5655'
set_up(device_id)
buy_items(get_materials(), get_material_properties(), device_id)