import cv2
import numpy as np
import os

def removeBackground(imagePath):
    image = cv2.imread(imagePath)

    if image is None:
        print("Error: Failed to read the input image.")
        return

    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])

    mask = cv2.inRange(image, lower_white, upper_white)
    mask = cv2.bitwise_not(mask)
    bones = cv2.bitwise_and(image, image, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        bone_segment = bones[y:y + h, x:x + w]
        output_file = f"bone_{i + 1}.png"
        cv2.imwrite(output_file, bone_segment)
        print(f"Bone {i + 1}: Height: {h}, Width: {w}")

# This function loads an input image and removes its background by extracting white regions.
# It identifies bone segments by finding contours in the remaining mask and saves each segment as an individual image file.
# The dimensions (height and width) of each bone segment are printed during processing.


def get_color_bones(image_path, output_folder):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Failed to read the image with removed background.")
        return

    color_ranges = {
        "yellow": [(20, 100, 100), (30, 255, 255)],
        "blue_color_range" : [(100, 50, 50), (120, 255, 255)],
        "green": [(45, 100, 100), (85, 255, 255)],
        "peach_pink": [(5, 100, 100), (15, 255, 255)],
        "purple": [(110, 50, 50), (130, 255, 255)]
    }

    os.makedirs(output_folder, exist_ok=True)
    bone_segments = {}

    purple_width = 0
    purple_height = 0

    for color, (lower_range, upper_range) in color_ranges.items():
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, np.array(lower_range), np.array(upper_range))
        bone_segment = cv2.bitwise_and(image, image, mask=mask)
        bone_segments[color] = bone_segment

    gray_segment = cv2.cvtColor(bone_segment, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_segment, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if color == "purple" and contours:
        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        purple_width = w
        purple_height = h

    for color, (lower_range, upper_range) in color_ranges.items():
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, np.array(lower_range), np.array(upper_range))
        bone_segment = cv2.bitwise_and(image, image, mask=mask)
        bone_segments[color] = bone_segment

    for i, (color, segment) in enumerate(bone_segments.items(), 1):
        gray_segment = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_segment, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            if color == "blue_color_range":
                w = w - purple_width
                h = h - purple_height
            print(f"Bone {i} ({color}): Height: {h}, Width: {w}")
            output_file = os.path.join(output_folder, f"bone_{i}_{color}.png")
            cv2.imwrite(output_file, segment)

# This function processes an input image to extract bone segments of different colors based on predefined HSV color ranges.
# It then adjusts the dimensions of these segments and saves them as separate image files in an output folder.
# Load the input image and check if it was loaded successfully.
# Define color ranges for various bone colors in the HSV color space.
# Create an output folder if it doesn't exist and initialize an empty dictionary to store segmented bone images.
# For each color range, apply a mask to the input image to extract the bone segment of that color.
# Calculate and store the dimensions (width and height) of the purple bone segment if it's purple.
# Process each segmented bone, adjusting its dimensions if necessary, and print the dimensions.
# Save each bone as a separate image file in the output folder.

if __name__ == "__main__":
    input_image_path = "finger-bones.jpg"
    output_directory = "bone_segments"

    removeBackground(input_image_path)
    get_color_bones("bone_1.png", output_directory)
