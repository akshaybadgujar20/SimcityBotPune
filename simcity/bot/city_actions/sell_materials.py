from simcity.bot.automation.city_utility_actions import click_on_own_trade_depot, click_on_city_storage, \
    click_on_own_material_storage, go_to_next_page_in_city_trade_depot, go_to_next_page_in_storage, \
    click_on_purchase_menu
import logging
import time

from simcity.bot.automation.find_empty_trade_boxes_and_sell_material import capture_material_quantity
from simcity.bot.automation.find_material import find_miscellaneous_material, find_material_in_city_storage
from simcity.bot.automation.open_empty_trade_box import open_empty_trade_box
from simcity.bot.automation.sell_material import sell_material
from simcity.bot.enums.miscellaneous import Miscellaneous


def sell_materials(
        materials,
        device_id,
        advertise,
        full_price,
        max_city_storage_scrolls=15,
        max_depot_pages=4):

    click_on_purchase_menu(device_id)
    time.sleep(2)
    click_on_own_trade_depot(device_id)
    time.sleep(2)

    current_depot_page = 1
    empty_trade_boxes, _ = find_miscellaneous_material(
        Miscellaneous.EMPTY_TRADE_BOXES,
        device_id
    )
    empty_trade_box_index = 0

    for material in materials:
        logging.info(f'Selling material: {material.name}')

        # --------------------------------------------------
        # STEP 1: Open ONE trade box (page-aware, sequential)
        # --------------------------------------------------
        box, empty_trade_boxes, empty_trade_box_index, current_depot_page = \
            get_next_empty_trade_box(
                device_id,
                empty_trade_boxes,
                empty_trade_box_index,
                current_depot_page,
                max_depot_pages
            )

        if box is None:
            logging.info('No empty trade boxes available')
            return

        open_empty_trade_box(box, device_id)
        time.sleep(1)

        # --------------------------------------------------
        # STEP 2: Switch storage ONCE for material
        # --------------------------------------------------
        check_material_type_and_open_trade_depot(device_id, material)
        time.sleep(1)

        # --------------------------------------------------
        # STEP 3: Find quantity (vertical scroll)
        # --------------------------------------------------
        total_quantity = 0

        for _ in range(max_city_storage_scrolls):
            founded_material_list, _ = find_material_in_city_storage(material, device_id)

            if founded_material_list:
                total_quantity = capture_material_quantity(founded_material_list[0], device_id)
                break

            go_to_next_page_in_storage(device_id)
            time.sleep(1)

        if total_quantity <= 0:
            logging.info(f'{material.name} not found or zero quantity')
            continue

        remaining_quantity = total_quantity
        logging.info(f'{material.name} quantity: {total_quantity}')

        # --------------------------------------------------
        # STEP 4: Sell loop (re-scan storage EVERY time)
        # --------------------------------------------------
        while remaining_quantity > 0:

            founded_material = None

            for _ in range(max_city_storage_scrolls):
                founded_material_list, _ = find_material_in_city_storage(material, device_id)

                if founded_material_list:
                    founded_material = founded_material_list[0]
                    break

                go_to_next_page_in_storage(device_id)
                time.sleep(1)

            if founded_material is None:
                logging.info(f'{material.name} not found during selling')
                break

            sell_material(
                founded_material,
                device_id,
                advertise,
                full_price,
                material.sell_duration
            )

            remaining_quantity -= min(5, remaining_quantity)
            time.sleep(1)

            if remaining_quantity <= 0:
                break

            box, empty_trade_boxes, empty_trade_box_index, current_depot_page = \
                get_next_empty_trade_box(
                    device_id,
                    empty_trade_boxes,
                    empty_trade_box_index,
                    current_depot_page,
                    max_depot_pages
                )

            if box is None:
                logging.info('Depot full while selling')
                return

            open_empty_trade_box(box, device_id)
            time.sleep(1)


def check_material_type_and_open_trade_depot(device_id, material):
    if material.building_name != 'FACTORY':
        logging.info('Item is commercial item, opening city storage')
        click_on_city_storage(device_id)
    else:
        logging.info('Item is factory item, opening material storage')
        click_on_own_material_storage(device_id)
    time.sleep(1)

def get_next_empty_trade_box(
        device_id,
        empty_trade_boxes,
        empty_trade_box_index,
        current_depot_page,
        max_depot_pages):

    # If we still have unused boxes on current page
    if empty_trade_box_index < len(empty_trade_boxes):
        return (
            empty_trade_boxes[empty_trade_box_index],
            empty_trade_boxes,
            empty_trade_box_index + 1,
            current_depot_page
        )

    # Otherwise, move to next page and scan again
    if current_depot_page >= max_depot_pages:
        return None, empty_trade_boxes, empty_trade_box_index, current_depot_page

    go_to_next_page_in_city_trade_depot(device_id)
    time.sleep(1)
    current_depot_page += 1

    empty_trade_boxes, _ = find_miscellaneous_material(
        Miscellaneous.EMPTY_TRADE_BOXES,
        device_id
    )

    empty_trade_box_index = 0

    if not empty_trade_boxes:
        return None, empty_trade_boxes, empty_trade_box_index, current_depot_page

    return (
        empty_trade_boxes[0],
        empty_trade_boxes,
        1,
        current_depot_page
    )