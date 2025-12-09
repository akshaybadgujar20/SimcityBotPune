import cv2
import numpy as np
import logging

def apply_nms_and_draw_rectangle(rectangles, threshold, screenshot):
    # Convert rectangles to numpy array
    rectangles = np.array(rectangles)
    # Apply Non-Maximum Suppression (NMS)
    if len(rectangles) > 0:
        # The list of indices of the remaining rectangles after NMS
        indices = cv2.dnn.NMSBoxes(rectangles.tolist(), np.ones(len(rectangles)), score_threshold=threshold, nms_threshold=0.6)
        if len(indices) > 0:
            indices = indices.flatten()
            matches = []
            # Iterate through the filtered rectangles and draw them
            for i in indices:
                # draw rectangle on screenshot
                rect = rectangles[i]
                top_left = (rect[0], rect[1])
                bottom_right = (rect[2], rect[3])
                cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                matches.append(rectangles[i])
            logging.info(f'total matches {len(indices)}')
            # save drawn rectangles as image
            output_path = 'output_image_with_rectangles.jpg'
            cv2.imwrite(output_path, screenshot)
            return matches

def apply_nms(rectangles, threshold, screenshot):
    # Convert rectangles to numpy array
    rectangles = np.array(rectangles)
    # Apply Non-Maximum Suppression (NMS)
    if len(rectangles) > 0:
        # The list of indices of the remaining rectangles after NMS
        indices = cv2.dnn.NMSBoxes(rectangles.tolist(), np.ones(len(rectangles)), score_threshold=threshold, nms_threshold=0.6)
        if len(indices) > 0:
            indices = indices.flatten()
            matches = []
            # Iterate through the filtered rectangles and draw them
            for i in indices:
                matches.append(rectangles[i])
            logging.info(f'total matches {len(indices)}')
            # save drawn rectangles as image
            output_path = 'output_image_with_rectangles.jpg'
            cv2.imwrite(output_path, screenshot)
            return matches