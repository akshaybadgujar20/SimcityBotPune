import logging
import sys
from pathlib import Path

import cv2


def take_template(template_path):
    # Example usage
    image_path = get_image_path(template_path)

    # Check if the file exists
    if image_path.exists():
        template = cv2.imread(str(image_path))
        # Check if the image is loaded correctly
        if template is None:
            logging.info("Error: Template image not loaded.")
            sys.exit()
        template_grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # save template which is made gey
        cv2.imwrite('template_grey.png',template_grey)
        return template_grey
    else:
        print(f"Image not found: {image_path}")

def get_image_path(relative_path):
    # Get the directory where the current script is located
    script_dir = Path(__file__).resolve().parent

    # Construct the full path to the resources directory
    # Assuming 'resources' is located at the same level as the 'simcity' folder
    project_root = script_dir.parent.parent.parent  # Go up two levels to reach the project root
    resources_dir = project_root / 'resources'

    # Create the full image path by joining the resources dir with the relative path
    image_path = resources_dir / relative_path

    # Resolve the absolute path
    return image_path.resolve()