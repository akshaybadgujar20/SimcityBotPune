import pytesseract

from simcity.bot.parameters import get_materials, get_material_properties
from simcity.bot.main import set_up, buy_items

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary

device_id = '5665'
set_up(device_id)
buy_items(get_materials(), get_material_properties(), device_id)