# logger.py

import logging

class CustomLogger(logging.Logger):
    def info(self, msg, device_id=None, *args, **kwargs):
        if device_id:
            from simcity.bot.cities import get_city_name_by_port  # Import here to avoid circular dependency
            msg = f"[Device ID: {get_city_name_by_port(device_id)}] {msg}"
        super().info(msg, *args, **kwargs)

def setup_logging():
    logging.setLoggerClass(CustomLogger)
    logger = logging.getLogger()
    # Check if handlers are already added to prevent duplicates
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # File handler
        filename = 'simcity_buildit.log'
        file_handler = logging.FileHandler(filename, mode='w')
        file_handler.setLevel(logging.INFO)

        # Formatter for both handlers
        formatter = logging.Formatter(
            '%(asctime)s  - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y - %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.info('\n===== New Automation Started =====\n')
        print('Logging setup completed')