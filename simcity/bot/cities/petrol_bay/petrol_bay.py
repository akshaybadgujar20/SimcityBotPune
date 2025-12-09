import pytesseract

from simcity.bot.main import buy_items, set_up
from simcity.bot.parameters import get_materials, get_material_properties

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

device_id = '6055'
set_up(device_id)
buy_items(get_materials(), get_material_properties(), device_id)