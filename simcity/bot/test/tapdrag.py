import time

import uiautomator2 as u2

# Step 1: Connect to the device
device = u2.connect('127.0.0.1:5725')  # Replace with your device's IP or USB connection
print('started')
points = [(675, 680), (500, 935), (1450, 935)]
# device.swipe_points(points, duration=0.2)