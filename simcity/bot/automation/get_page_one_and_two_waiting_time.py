import logging


def get_page_one_and_two_waiting_time(timer_name, manager):
    timer = manager.get_timer_time(timer_name)
    logging.info(f'remaining timer value {timer}')
    if timer < 25:
        page_one_wait_time = 30 - timer - 1
        page_two_wait_time = 30 - timer - 4
    else:
        page_one_wait_time = 0
        page_two_wait_time = 0
    logging.info(f'page_one_wait_time {page_one_wait_time}')
    logging.info(f'page_two_wait_time {page_two_wait_time}')
    return page_one_wait_time, page_two_wait_time