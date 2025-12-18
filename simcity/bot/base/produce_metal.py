import logging
import time
from types import SimpleNamespace

import uiautomator2 as u2

from simcity.bot.main import add_raw_material_to_production, collect_raw_materials, set_up

device_id = '5555'
device = u2.connect("127.0.0.1:5555")

def produce_metal():
    material = SimpleNamespace(
        x_location=665,
        y_location=375
    )
    # add metal to production
    for i in range(8):
        logging.info('collecting metal')
        collect_raw_materials(12, device_id)
        logging.info('add metal to production')
        add_raw_material_to_production(material, 12, device_id)
        logging.info('waiting for 62 seconds')
        time.sleep(62)

set_up(device_id)
produce_metal()