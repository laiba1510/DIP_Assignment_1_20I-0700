import cv2
import numpy as np

def get_color_area(image, lower_color_range, upper_color_range):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_color_range, upper_color_range)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    return total_area, contours

# Converts the input image to the HSV color space for color-based analysis.
# Applies color range masking, morphological operations, and contour detection to identify color regions.



def calculate_percentage_area_covered(image_path, arrow_lower_range, arrow_upper_range):
    image = cv2.imread(image_path)
    color_ranges = [
        (np.array([20, 100, 100]), np.array([30, 255, 255]), (0, 255, 255), "Yellow"),
        (np.array([0, 0, 180]), np.array([180, 25, 255]), (192, 192, 192), "Light Gray"),
        (np.array([0, 0, 100]), np.array([180, 25, 179]), (128, 128, 128), "Gray"),
        (np.array([0, 0, 50]), np.array([180, 25, 99]), (64, 64, 64), "Dark Gray")
    ]
    arrow_coverage = {}

    for lower, upper, color, color_name in color_ranges:
        total_area, contours = get_color_area(image, lower, upper)
        arrow_area, _ = get_color_area(image, arrow_lower_range, arrow_upper_range)
        percentage_covered = (arrow_area / total_area) * 100 if total_area > 0 else 0
        arrow_coverage[color_name] = percentage_covered

# Loads the input image and defines color ranges for different colors.
# Calculates the area covered by a specified arrow color within each color range.
# Computes the percentage area covered by the arrow and stores it in a dictionary.


    print("Bar Area Covered(%)")
    for color_name, coverage in arrow_coverage.items():
        print(f"{color_name}: {coverage * 100:.2f}%")

arrow_lower_range = np.array([0, 100, 100])
arrow_upper_range = np.array([10, 255, 255])
calculate_percentage_area_covered('fig2.jpg', arrow_lower_range, arrow_upper_range)
