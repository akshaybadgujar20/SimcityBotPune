import os
import subprocess
import logging

def check_adb_devices_and_connect_if_not_connected(device_id):
    # Run adb devices command
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Check if command was executed successfully
    if result.returncode == 0:
        # Print the output of the command
        logging.info("ADB Devices Output:")
        logging.info(result.stdout)
        if device_id in result.stdout:
            logging.info(f"'{device_id}' is present in the adb devices output.")
        else:
            logging.info(f"'{device_id}' is NOT present in the adb devices output.")
            os.system(f"adb connect 127.0.0.1:{device_id}")
    else:
        # Print error if there was a problem running the command
        logging.info("Error running adb devices:")
        logging.info(result.stderr)
