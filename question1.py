import cv2
import numpy as np

def process_image(image):
    screen_width, screen_height = 1040, 720
    image = cv2.resize(image, (screen_width, screen_height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            perimeter = cv2.arcLength(approx, True)
            M = cv2.moments(approx)
            centroid_x = int(M['m10'] / M['m00'])
            centroid_y = int(M['m01'] / M['m00'])
            cv2.putText(image, f"Parameter: {perimeter}", (centroid_x, centroid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, f"Centroid: ({centroid_x}, {centroid_y})", (centroid_x, centroid_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return image
# This function processes an input image to identify and annotate rectangles.
# It resizes the image, converts it to grayscale, applies thresholding, and finds contours.
# For each contour that represents a rectangle, it calculates perimeter and centroid, adding annotations to the image.


image = cv2.imread('rect1.jpg')
result = process_image(image)
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
