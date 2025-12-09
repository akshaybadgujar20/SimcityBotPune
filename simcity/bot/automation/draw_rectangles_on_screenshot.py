import cv2


def draw_rectangles_on_screenshot(rectangles, screenshot, output_path):
    for index, rect in enumerate(rectangles):
        x, y, x2, y2 = rect
        cv2.rectangle(screenshot, (x, y), (x2, y2), (0, 255, 0), 2)  # Green border

        # Put the index number inside the rectangle
        position_text = str(index + 1)  # Using 1-based indexing
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0  # Increase font scale for visibility
        color = (0, 255, 0)  # Same color as rectangle border (Green)
        thickness = 2  # Thicker text for visibility

        # Calculate the text size and position
        text_size = cv2.getTextSize(position_text, font, font_scale, thickness)[0]
        text_x = x + (x2 - x - text_size[0]) // 2
        text_y = y + (y2 - y + text_size[1]) // 2

        # Draw the text on the screenshot
        cv2.putText(screenshot, position_text, (text_x, text_y), font, font_scale, color, thickness)

        # Save the modified screenshot
    cv2.imwrite(output_path, screenshot)
