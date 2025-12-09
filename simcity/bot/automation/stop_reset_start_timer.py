

def stop_reset_start_timer(manager, timer_name):
    manager.stop_timer(timer_name)
    manager.reset_timer(timer_name)
    manager.start_timer(timer_name)