import logging
import math
import time

from simcity.bot.automation.adb_actions import perform_swipe, perform_click_with_rectangle, perform_click, press_esc_key
from simcity.bot.automation.find_material import find_miscellaneous_material, find_material_in_city_storage
from simcity.bot.automation.open_empty_trade_box import open_empty_trade_box
from simcity.bot.automation.sell_material import sell_material
from simcity.bot.automation.take_screenshot_and_read_text import take_screenshot_and_read_text
from simcity.bot.enums.miscellaneous import Miscellaneous

is_find_empty_trade_boxes_and_sell_material_running = True
is_find_material_on_city_storage_and_sell_running = True

def capture_material_quantity(material, device_id):
    quantity: str = take_screenshot_and_read_text(device_id, material[2], material[1], material[2]+80, material[3])
    logging.info(f'found quantity = {quantity}')
    return int(quantity)

def find_empty_trade_boxes_and_sell_material(material, device_id, advertise, full_price, depot_page_no):
    if is_find_empty_trade_boxes_and_sell_material_running:
        found_quantity = 0
        remaining_quantity = 0
        for depot_page_no in range(6):
            logging.info(f'finding {material.name} on trade depot page no  {depot_page_no}')
            empty_trade_boxes, screenshot = find_miscellaneous_material(Miscellaneous.EMPTY_TRADE_BOXES, device_id)
            if len(empty_trade_boxes) > 0:
                logging.info(f'found {len(empty_trade_boxes)} empty trade boxes')
                if found_quantity == 0:
                    logging.info(f'finding {material.name} quantity on city storage for quantity')
                    open_empty_trade_box(empty_trade_boxes[0], device_id)
                    for city_storage_page_no in range(15):
                        founded_material_list, screenshot = find_material_in_city_storage(material, device_id)
                        if len(founded_material_list) > 0:
                            found_quantity = capture_material_quantity(founded_material_list[0], device_id)
                            remaining_quantity = found_quantity
                            sell_material(founded_material_list[0], device_id, advertise, full_price, material.sell_duration)
                            if remaining_quantity > 5:
                                remaining_quantity = remaining_quantity - 5
                            else:
                                remaining_quantity = remaining_quantity - remaining_quantity
                            break
                        else:
                            logging.info(f'material not found city storage page no {city_storage_page_no}, going to scroll vertically for next page')
                            perform_swipe(925, 650, 925, 260, 1000, device_id)
                            time.sleep(1)

                    logging.info(f'found quantity = {found_quantity}')

                if len(empty_trade_boxes)-1 > 0:
                    for index, empty_trade_box in enumerate(empty_trade_boxes[1:], start=1):
                        open_empty_trade_box(empty_trade_box, device_id)
                        logging.info(f'remaining_quantity => {remaining_quantity}')
                        for city_storage_page_no in range(15):
                            logging.info(f'finding {material.name} on city storage page no {city_storage_page_no}')
                            founded_material_list, screenshot = find_material_in_city_storage(material, device_id)
                            if len(founded_material_list) > 0:
                                sell_material(founded_material_list[0], device_id, advertise, full_price, material.sell_duration)
                                if remaining_quantity > 5:
                                    remaining_quantity = remaining_quantity - 5
                                else:
                                    remaining_quantity = remaining_quantity - remaining_quantity
                                break
                            else:
                                logging.info(f'material not found city storage page no {city_storage_page_no}, going to scroll vertically for next page')
                                perform_swipe(925, 650, 925, 260, 1000, device_id)
                                time.sleep(1)

                            if found_quantity > 0 and remaining_quantity == 0:
                                logging.info(f'break 1')
                                return depot_page_no

                        if found_quantity > 0 and remaining_quantity == 0:
                            logging.info(f'break 2')
                            return depot_page_no
                    return depot_page_no
            else:
                logging.info(f'empty trade boxes not found on trade depot page no {depot_page_no}, going to scroll horizontally for next  depot page')
                perform_swipe(1250, 550, 350, 550, 1000, device_id)
                time.sleep(1)
        return depot_page_no

def stop_sell_materials_task(is_running):
    global is_find_empty_trade_boxes_and_sell_material_running
    global is_find_material_on_city_storage_and_sell_running
    is_find_empty_trade_boxes_and_sell_material_running = is_running
    is_find_material_on_city_storage_and_sell_running = is_running