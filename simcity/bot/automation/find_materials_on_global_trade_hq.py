import logging
import time

from simcity.bot.automation.adb_actions import perform_click_with_rectangle, perform_swipe, perform_click
from simcity.bot.automation.close_trade_depot import close_trade_depot
from simcity.bot.automation.find_and_click_on_refresh_button import find_and_click_on_refresh_button_indefinitely, stop_refresh_task
from simcity.bot.automation.find_city_name_and_click_on_trade_hq import find_city_name_and_click_on_trade_hq
from simcity.bot.automation.find_material import find_miscellaneous_material
from simcity.bot.automation.find_material_count import find_material_count_for_given_iterations, find_material_count_indefinitely, find_material_count_once
from simcity.bot.automation.find_materials_with_priorities import find_materials_with_priorities_in_global_trade_hq, \
    find_materials_with_priorities_in_trade_depot
from simcity.bot.automation.get_page_one_and_two_waiting_time import get_page_one_and_two_waiting_time
from simcity.bot.automation.stop_reset_start_timer import stop_reset_start_timer
from simcity.bot.enums.miscellaneous import Miscellaneous

is_find_materials_on_global_trade_hq_running = True
is_find_materials_on_trade_depot_running = True
is_find_material_boxes_in_global_trade_hq_running = True

def find_coins_in_global_trade_hq(materials, material_priorities, manager, device_id):
    while(True):
        logging.info('while loop ran')
        logging.info('finding coins on global trade hq')
        coins_count_in_global_trade_hq = find_material_count_for_given_iterations(Miscellaneous.GLOBAL_TRADE_HQ_COIN, device_id, 3.0)
        if coins_count_in_global_trade_hq > 0:
            logging.info('coins found')
            find_materials_on_global_trade_hq(materials, 1, coins_count_in_global_trade_hq, material_priorities, manager, device_id)
        else:
            coins_not_found_wait_30_and_refresh_global_trade_hq(materials, material_priorities, manager, device_id)

def find_materials_on_global_trade_hq(materials, global_trade_hq_page_no, coins_count_in_global_trade_hq, material_priorities, manager, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    if is_find_materials_on_global_trade_hq_running:
        logging.info(f'finding material on page no {global_trade_hq_page_no}')
        founded_items, screenshot = find_materials_with_priorities_in_global_trade_hq(materials, device_id, material_priorities)
        logging.info(f'materials found {len(founded_items)}, materials - {materials}')
        if len(founded_items) > 0:
            if len(founded_items) > 1:
                if is_find_materials_on_global_trade_hq_running:
                    logging.info('more than one matches found, using for loop for buying')
                    for index, founded_item in enumerate(founded_items):
                        perform_click_with_rectangle(founded_item, device_id)
                        time.sleep(1)
                        return find_trade_boxes_and_buy_material_on_trade_depot(materials, material_priorities, 1, manager, device_id, True)
                    logging.info(f'going for next flow')
                    return handle_next_page_or_waiting_scenario_for_global_trade_hq(materials, material_priorities, global_trade_hq_page_no, coins_count_in_global_trade_hq, manager, device_id)
            else:
                logging.info('single match found, buying default found material')
                logging.info(f'clicking on trade HQ at location {founded_items[0]}')
                perform_click_with_rectangle(founded_items[0], device_id)
                time.sleep(1)
                return find_trade_boxes_and_buy_material_on_trade_depot(materials, material_priorities, 1, manager, device_id, True)
                logging.info(f'going for next flow')
                return handle_next_page_or_waiting_scenario_for_global_trade_hq(materials, material_priorities, global_trade_hq_page_no, coins_count_in_global_trade_hq, manager, device_id)
        else:
            logging.info('no materials found')
            return handle_next_page_or_waiting_scenario_for_global_trade_hq(materials, material_priorities, global_trade_hq_page_no, coins_count_in_global_trade_hq, manager, device_id)

def handle_next_page_or_waiting_scenario_for_global_trade_hq(materials, material_priorities, global_trade_hq_page_no, coins_count_in_global_trade_hq, manager, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    page_one_wait_time, page_two_wait_time = get_page_one_and_two_waiting_time(timer_name, manager)
    if coins_count_in_global_trade_hq == 8 and global_trade_hq_page_no == 1:
        logging.info('going for page 2')
        perform_swipe(1500, 550, 350, 550, 1000, device_id)
        time.sleep(1)
        find_materials_on_global_trade_hq(materials, global_trade_hq_page_no + 1, coins_count_in_global_trade_hq, material_priorities, manager, device_id)
    else:
        if global_trade_hq_page_no == 1:
            wait_for_given_seconds(page_one_wait_time)
        elif global_trade_hq_page_no == 2:
            wait_for_given_seconds(page_two_wait_time)
        else:
            logging.info(f'handle this page no {global_trade_hq_page_no} scenario')

        logging.info(f'finding refresh button')
        refresh_button_count = find_material_count_indefinitely(Miscellaneous.REFRESH,device_id)
        if refresh_button_count > 0:
            logging.info(f'refresh button found, clicking on it')
            perform_click(965, 955, device_id)
            time.sleep(1)
            stop_reset_start_timer(manager, timer_name)
            coins_count_in_global_trade_hq = find_material_count_for_given_iterations(Miscellaneous.GLOBAL_TRADE_HQ_COIN, device_id, 3)
            if coins_count_in_global_trade_hq > 0:
                logging.info(f'coins found on global trade hq')
                return
            else:
                logging.info(f'coins not found on global trade hq')
                page_one_wait_time, page_two_wait_time = get_page_one_and_two_waiting_time(timer_name, manager)
                if global_trade_hq_page_no == 1:
                    wait_for_given_seconds(page_one_wait_time)
                elif global_trade_hq_page_no == 2:
                    wait_for_given_seconds(page_two_wait_time)

                find_and_click_on_refresh_button_indefinitely(device_id)
                time.sleep(1)
                stop_reset_start_timer(manager, timer_name)
                return find_coins_and_then_call_find_materials_in_global_trade_hq(materials, material_priorities, manager, device_id)
        else:
            logging.info('refresh button not found')
            logging.info('handle this scenario')

def find_trade_boxes_and_buy_material_on_trade_depot(materials, material_priorities, trade_depot_page_no, manager, device_id, is_indefinitely=True):
    if is_indefinitely:
        trade_box_count_in_trade_depot = find_material_count_indefinitely(Miscellaneous.TRADE_BOX, device_id)
    else:
        trade_box_count_in_trade_depot = find_material_count_once(Miscellaneous.TRADE_BOX, device_id)
    if trade_box_count_in_trade_depot > 0:
        logging.info(f'coins found')
        return find_materials_on_trade_depot(materials, trade_depot_page_no, trade_box_count_in_trade_depot, material_priorities, manager, device_id)
    else:
        logging.info(f'no coins found, probably item is aready sold or not present in trade depot')
        timer = close_trade_depot_and_open_global_trade_hq(timer_name, manager, device_id)
        if timer < 25:
            logging.info(f'timer {timer}, returning to global trade hq')
            return
        elif timer > 25 and timer < 30:
            logging.info(f'timer {timer}, waiting for refresh button to appear')
            return check_for_refresh_button_and_refresh_global_trade_hq(materials, material_priorities, timer, timer_name, manager, device_id)
        elif timer > 30:
            return handle_timer_greater_than_30_scenario_in_trade_depot(materials, material_priorities, timer, timer_name, manager, device_id)
        else:
            logging.info(f'handle this scenarios')

def wait_for_given_seconds(seconds):
    logging.info(f'waiting for {seconds} sec')
    time.sleep(seconds)
    logging.info(f'waiting for {seconds} sec completed, opening trade hq again, finding refresh button')

def find_materials_on_trade_depot(materials, trade_depot_page_no, trade_box_count_in_trade_depot, material_priorities, manager, device_id):
    if is_find_materials_on_trade_depot_running:
        timer_name = 'TRADE_HQ_TIMER_' + device_id
        logging.info(f'finding items in another city trade depot on page no {trade_depot_page_no}')
        found_items, screenshot = find_materials_with_priorities_in_trade_depot(materials, device_id, material_priorities)
        logging.info(f'found {len(found_items)}')
        if len(found_items) > 0:
            for index, found_item in enumerate(found_items):
                if is_find_materials_on_trade_depot_running:
                    logging.info(f'clicking on item no {index + 1} on trade depot')
                    perform_click_with_rectangle(found_item, device_id)
                    time.sleep(1)

            ok_icon, screenshot = find_miscellaneous_material(Miscellaneous.OK, device_id)
            if len(ok_icon) > 0:
                logging.info('ok icon window found, closing it')
                perform_click(945, 720, device_id)

            if trade_depot_page_no == 1 and trade_box_count_in_trade_depot == 8:
                return goto_next_trade_depot_page(materials, material_priorities, trade_depot_page_no, device_id, manager)
            else:
                timer = close_trade_depot_and_open_global_trade_hq(timer_name, manager, device_id)
                if timer < 25:
                    logging.info(f'timer {timer}, returning to global trade hq')
                    return
                elif timer > 25 and timer < 30:
                    logging.info(f'timer {timer}, waiting for refresh button to appear')
                    return check_for_refresh_button_and_refresh_global_trade_hq(materials, material_priorities, timer, timer_name, manager, device_id)
                elif timer > 30:
                    return handle_timer_greater_than_30_scenario_in_trade_depot(materials, material_priorities, timer, timer_name, manager, device_id)
                else:
                    logging.info(f'handle this scenarios')
        else:
            logging.info(f'item not found on page no {trade_depot_page_no}')
            if trade_depot_page_no == 1 and trade_box_count_in_trade_depot == 8:
                return goto_next_trade_depot_page(materials, material_priorities, trade_depot_page_no, device_id, manager)
            else:
                timer = close_trade_depot_and_open_global_trade_hq(timer_name, manager, device_id)
                if timer < 25:
                    logging.info(f'timer {timer}, returning to global trade hq')
                    return
                elif timer > 25 and timer < 30:
                    logging.info(f'timer {timer}, waiting for refresh button to appear')
                    return check_for_refresh_button_and_refresh_global_trade_hq(materials, material_priorities, timer, timer_name, manager, device_id)
                elif timer > 30:
                    return handle_timer_greater_than_30_scenario_in_trade_depot(materials, material_priorities, timer, timer_name, manager, device_id)
                else:
                    logging.info(f'handle this scenarios')

def handle_timer_greater_than_30_scenario_in_trade_depot(materials, material_priorities, timer, timer_name, manager, device_id):
    refresh_button_count = find_material_count_once(Miscellaneous.REFRESH, device_id)
    if refresh_button_count > 0:
        logging.info(f'timer {timer}, refresh button is already visible, clicking on refresh button')
        return check_for_refresh_button_and_refresh_global_trade_hq(materials, material_priorities, timer, timer_name, manager, device_id)
    else:
        logging.info(f'global trade depot is already refreshed, scaning for coins')
        find_coins_in_global_trade_hq(materials, material_priorities, manager, device_id)

def goto_next_trade_depot_page(materials, material_priorities, trade_depot_page_no, device_id, manager):
    logging.info('going for page 2')
    perform_swipe(1500, 550, 350, 550, 1000, device_id)
    time.sleep(1)
    return find_trade_boxes_and_buy_material_on_trade_depot(materials, material_priorities, trade_depot_page_no + 1, manager, device_id, False)

def check_for_refresh_button_and_refresh_global_trade_hq(materials, material_priorities, timer, timer_name, manager, device_id):
    logging.info(f'timer {timer}, waiting to refresh the page from another city itself')
    find_and_click_on_refresh_button_indefinitely(device_id)
    time.sleep(1)
    stop_reset_start_timer(manager, timer_name)
    return find_coins_and_then_call_find_materials_in_global_trade_hq(materials, material_priorities, manager, device_id)

def find_coins_and_then_call_find_materials_in_global_trade_hq(materials, material_priorities, manager, device_id):
    timer_name = 'TRADE_HQ_TIMER_' + device_id
    coins_count_in_global_trade_hq = find_material_count_for_given_iterations(Miscellaneous.GLOBAL_TRADE_HQ_COIN, device_id, 3)
    if coins_count_in_global_trade_hq > 0:
        logging.info(f'coins found on global trade hq')
        return
    else:
        logging.info(f'Nothing for sale right now')
        page_one_wait_time, page_two_wait_time = get_page_one_and_two_waiting_time(timer_name, manager)
        wait_for_given_seconds(27)
        find_and_click_on_refresh_button_indefinitely(device_id)
        time.sleep(1)
        stop_reset_start_timer(manager, timer_name)
        find_coins_and_then_call_find_materials_in_global_trade_hq(materials, material_priorities, manager, device_id)

def close_trade_depot_and_open_global_trade_hq(timer_name, manager, device_id):
    time.sleep(1)
    close_trade_depot(device_id)
    time.sleep(1)
    find_city_name_and_click_on_trade_hq(device_id)
    timer = manager.get_timer_time(timer_name)
    time.sleep(1)
    return timer

def coins_not_found_wait_30_and_refresh_global_trade_hq(materials, material_priorities, manager, device_id):
    logging.info('no coins found, waiting for 30 seconds')
    time.sleep(30)
    logging.info('waiting is completed, clicking on refresh')
    perform_click(965, 955, device_id)
    time.sleep(1)
    stop_reset_start_timer(manager,'TRADE_HQ_TIMER_' + device_id)
    return

def stop_buy_items_task(is_running):
    global is_find_materials_on_global_trade_hq_running
    global is_find_material_boxes_in_global_trade_hq_running
    global is_find_materials_on_trade_depot_running
    is_find_materials_on_global_trade_hq_running = is_running
    is_find_material_boxes_in_global_trade_hq_running = is_running
    is_find_materials_on_trade_depot_running = is_running
    stop_refresh_task(is_running)