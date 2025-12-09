from simcity.bot.custom_timer import CustomTimer
import logging

# Managing multiple timers with unique keys
class TimerManager:
    def __init__(self):
        self.timers = {}

    def create_timer(self, key, interval=1):
        """Creates a new timer identified by a unique key"""
        if key not in self.timers:
            self.timers[key] = CustomTimer(key, interval)

    def start_timer(self, key):
        """Start a specific timer"""
        if key in self.timers:
            self.timers[key].start()

    def stop_timer(self, key):
        """Stop a specific timer"""
        if key in self.timers:
            self.timers[key].stop()

    def reset_timer(self, key):
        """Reset a specific timer"""
        if key in self.timers:
            self.timers[key].reset()

    def get_timer_time(self, key):
        """Get the time elapsed for a specific timer"""
        if key in self.timers:
            return self.timers[key].get_time()

    def set_timer_interval(self, key, interval):
        """Set a new interval for a specific timer"""
        if key in self.timers:
            self.timers[key].set_interval(interval)
