import cv2
import numpy as np

# Load the image
image = cv2.imread('fig2.jpg')

# Load the image with the red arrow
image_with_arrow = cv2.imread('fig2.jpg')

# Convert the image to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color ranges for each color
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])

light_gray_lower = np.array([0, 0, 200])
light_gray_upper = np.array([180, 30, 255])

gray_lower = np.array([0, 0, 100])
gray_upper = np.array([180, 30, 200])

# Adjusted dark gray values
dark_gray_lower = np.array([0, 0, 20])
dark_gray_upper = np.array([180, 30, 100])

# Create masks for each color
yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)
light_gray_mask = cv2.inRange(hsv_image, light_gray_lower, light_gray_upper)
gray_mask = cv2.inRange(hsv_image, gray_lower, gray_upper)

# Convert the image to grayscale for dark gray detection
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to isolate dark gray regions
_, dark_gray_mask = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)

# Create a mask for the red arrow
red_arrow_mask = cv2.inRange(image_with_arrow, (0, 0, 200), (50, 50, 255))  # Assuming red arrow is in this color range

# Find contours and calculate areas for each color
colored_areas = {
    "Yellow": cv2.countNonZero(cv2.bitwise_and(yellow_mask, red_arrow_mask)),
    "Light Gray": cv2.countNonZero(cv2.bitwise_and(light_gray_mask, red_arrow_mask)),
    "Gray": cv2.countNonZero(cv2.bitwise_and(gray_mask, red_arrow_mask)),
    "Dark Gray": cv2.countNonZero(cv2.bitwise_and(dark_gray_mask, red_arrow_mask))
}

# Calculate the total area of the red arrow
total_red_arrow_area = cv2.countNonZero(red_arrow_mask)

# Calculate and print the percentage area of each color covered by the red arrow
for color, area in colored_areas.items():
    percentage_area = (area / total_red_arrow_area) * 100
    print(f"{color}: {percentage_area:.2f}%")