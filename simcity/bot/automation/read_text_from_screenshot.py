import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import logging
cropped_image_path = 'cropped_image.png'

def read_text_from_screenshot(upper, lower, left, right, screenshot):
    cropped_image = screenshot[upper:lower, left:right]
    cv2.imwrite(cropped_image_path, cropped_image)

    height, width = cropped_image.shape
    new_size = (width * 2, height * 2)
    resized = cv2.resize(cropped_image, new_size, interpolation=cv2.INTER_CUBIC)

    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)
    contrasted = cv2.convertScaleAbs(resized, alpha=alpha, beta=beta)

    blurred = cv2.GaussianBlur(contrasted, (5, 5), 0)

    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    config = '--oem 3 --psm 6'
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(thresh, config=config)
    logging.info(f"Extracted Text: {text}")
    return text