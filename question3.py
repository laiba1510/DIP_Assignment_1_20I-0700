import cv2

def determine_blur(images):
    if len(images[0].shape) == 3:
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]

    laplacian_sharpness = [cv2.Laplacian(img, cv2.CV_64F).var() for img in images]

    blurred_index = laplacian_sharpness.index(min(laplacian_sharpness))
    original_index = 1 - blurred_index

    # Determines which of the input images is more blurred by calculating Laplacian sharpness.
    # Converts images to grayscale if they are in color.
    # Displays the blurred and original images, allowing visual comparison.

    cv2.imshow("Blurred Image", images[blurred_index])
    cv2.imshow("Original Image", images[original_index])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image1 = cv2.imread("fig5.jpg")
image2 = cv2.imread("fig5_blur.jpg")

determine_blur([image1, image2])
