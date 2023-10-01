import cv2
import numpy as np

def remove_bg(image_path):
    image = cv2.imread(image_path)

    lower_white = np.array([200, 200, 200])
    upper_white = np.array([255, 255, 255])

    mask = cv2.inRange(image, lower_white, upper_white)
    mask = cv2.bitwise_not(mask)

    result = cv2.bitwise_and(image, image, mask=mask)
    output_file = "face_only.png"

    cv2.imwrite(output_file, result)

    return output_file

def detect_gender(image_path_bg, image_path_no_bg):
    face_img_no_bg = cv2.imread(image_path_no_bg)
    gray_face = cv2.cvtColor(face_img_no_bg, cv2.COLOR_BGR2GRAY)

    contours, _ = cv2.findContours(gray_face, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    
    y_coordinates = [point[0][1] for point in largest_contour]
    face_length_y = max(y_coordinates) - min(y_coordinates)

    face_img_bg = cv2.imread(image_path_bg)
    hsv_image = cv2.cvtColor(face_img_bg, cv2.COLOR_BGR2HSV)

    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([180, 255, 30], dtype=np.uint8)

    black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
    contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_y_cord_hair = 0


    for contour in contours:
        max_cont_y = max(point[0][1] for point in contour)

        if max_cont_y > max_y_cord_hair:
            max_y_cord_hair = max_cont_y

    if max_y_cord_hair >= face_length_y:
        return "Female"
    else:
        return "Male"


# Detects gender based on hair length in an input image pair, one with a background and the other without. 
# It calculates the vertical extent of the face in the no-background image and compares it to the maximum 
# Y-coordinate of hair contours in the background image. If the hair length exceeds the face height, 
# it suggests "Female"; otherwise, it suggests "Male."


image_path_no_bg = remove_bg("fig4.jpg")
image_path_bg = "fig4.jpg"
gender = detect_gender(image_path_bg, image_path_no_bg)
print("Gender detected:", gender)
