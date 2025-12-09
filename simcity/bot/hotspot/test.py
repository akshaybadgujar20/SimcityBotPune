import logging
import uiautomator2 as u2

d = u2.connect("127.0.0.1:5555")

logging.info('Upgrading building')
# perform_swipe(635, 485, 950, 540, 1, device_id)
d.touch.down(635, 485)
d.sleep(1.0)
d.touch.move(950, 540)
d.touch.up(950, 540)