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

def display_areas_and_centroids(image_path):
    image = cv2.imread(image_path)
    color_ranges = [
        (np.array([20, 100, 100]), np.array([30, 255, 255]), (0, 255, 255), "Yellow"),
        (np.array([0, 0, 180]), np.array([180, 25, 255]), (192, 192, 192), "Light Gray"),
        (np.array([0, 0, 100]), np.array([180, 25, 179]), (128, 128, 128), "Gray"),
        (np.array([80, 10, 40]), np.array([100, 30, 60]), (64, 64, 64), "Dark Gray")
    ]

    for lower, upper, color, color_name in color_ranges:
        total_area, contours = get_color_area(image, lower, upper)
        centroid_x = 0
        centroid_y = 0
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centroid_x += cX
                centroid_y += cY
                cv2.drawContours(image, [contour], -1, color, 2)
                cv2.circle(image, (cX, cY), 7, color, -1)
                cv2.putText(image, f"{color_name} Area: {total_area} pixels", (cX - 100, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        if len(contours) > 0:
            centroid_x /= len(contours)
            centroid_y /= len(contours)
        print(f"{color_name} - Centroid: ({centroid_x}, {centroid_y}), Area: {total_area} pixels")

        # Load the image from the provided file path.
        # Iterate through predefined color ranges to detect and analyze specific colors in the image.
        # Calculate the centroid and total area for each color region within the image.
        # Draw contours, centroids, and display area information for each color region.
        # Print centroid coordinates and area for each color region in the image.


    cv2.imshow('Image with Centroids, Contours, and Areas', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

display_areas_and_centroids('fig1.jpg')
