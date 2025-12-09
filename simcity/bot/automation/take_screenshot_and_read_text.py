import cv2

from simcity.bot.automation.take_screenshot import take_bw_screenshot
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cropped_image_path = 'cropped_image.png'


def take_screenshot_and_read_text(device_id, left, upper, right, lower):
    screenshot = take_bw_screenshot(device_id)
    return read_text_from_image(left, upper, right, lower, screenshot)

def read_text_from_image(left, upper, right, lower, screenshot):
    # upper:lower left:right
    cropped_image = screenshot[upper:lower, left:right]
    # cv2.imwrite(cropped_image_path, cropped_image)
    cv2.imwrite(cropped_image_path + '_' + str(left) + '_' + str(upper) + '_' + str(right) + '_' + str(lower)+'.png', cropped_image)
    # Custom configuration for Tesseract
    custom_config = r'--oem 3 --psm 6 tessedit_char_whitelist=0123456789'
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(cropped_image, config=custom_config)
    # text = pytesseract.image_to_string(cropped_image)
    print(f"Extracted Text: {text}")
    return text