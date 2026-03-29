import logging
import threading

from simcity.bot.custom_timer import CustomTimer


class TimerManager:
    """Multiple timers by key; safe for concurrent trade sessions (different keys per device)."""

    def __init__(self) -> None:
        self.timers: dict = {}
        self._lock = threading.Lock()

    def create_timer(self, key, interval=1):
        """Creates a new timer identified by a unique key"""
        with self._lock:
            if key not in self.timers:
                self.timers[key] = CustomTimer(key, interval)

    def start_timer(self, key):
        """Start a specific timer"""
        with self._lock:
            t = self.timers.get(key)
        if t is not None:
            t.start()

    def stop_timer(self, key):
        """Stop a specific timer"""
        with self._lock:
            t = self.timers.get(key)
        if t is not None:
            t.stop()

    def reset_timer(self, key):
        """Reset a specific timer"""
        with self._lock:
            t = self.timers.get(key)
        if t is not None:
            t.reset()

    def get_timer_time(self, key):
        """Get the time elapsed for a specific timer (0 if the key was never created)."""
        with self._lock:
            t = self.timers.get(key)
        if t is not None:
            return t.get_time()
        return 0

    def set_timer_interval(self, key, interval):
        """Set a new interval for a specific timer"""
        with self._lock:
            t = self.timers.get(key)
        if t is not None:
            t.set_interval(interval)
