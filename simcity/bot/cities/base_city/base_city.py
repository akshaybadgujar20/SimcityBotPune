import pytesseract

from simcity.bot.enums.material import Material
from simcity.bot.main import buy_items, set_up

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path if necessary



def get_materials():
    return ['BURGERS']

def get_material_properties():
    return {
        Material.BURGERS: 1,
    }

# device_id = '6065'
device_id = '5555'
set_up(device_id)
buy_items(get_materials(), get_material_properties(), device_id)