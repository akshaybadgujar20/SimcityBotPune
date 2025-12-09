import logging
import time
import threading

class CustomTimer:
    def __init__(self, key, interval=1):
        self.key = key               # Identifier for the timer
        self.interval = interval     # Interval in seconds
        self.time_elapsed = 0        # Time elapsed
        self.running = False         # Timer status
        self._lock = threading.Lock() # To handle multi-threading safely

    def start(self):
        """Starts the timer"""
        if not self.running:
            self.running = True
            self._run_timer_thread = threading.Thread(target=self._run)
            self._run_timer_thread.start()

    def stop(self):
        """Stops the timer"""
        with self._lock:
            self.running = False

    def reset(self):
        """Resets the timer to 0"""
        with self._lock:
            self.time_elapsed = 0

    def _run(self):
        """Internal method to run the timer in a separate thread"""
        while self.running:
            with self._lock:
                self.time_elapsed += self.interval
            time.sleep(self.interval)

    def get_time(self):
        """Returns the current time elapsed"""
        with self._lock:
            return self.time_elapsed

    def set_interval(self, new_interval):
        """Set a new interval for the timer"""
        with self._lock:
            self.interval = new_interval