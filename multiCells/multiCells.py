import numpy as np
import matplotlib.pyplot as plt
import cv2

# Read tiff image
#image = cv2.imread('09_06_22_14h08m_08s_ms024__E02U2OS_53KO_5979GFP.tif', cv2.IMREAD_UNCHANGED)
image = cv2.imread('09_18_21_12h40m_33s_ms021__E03U2OS_SETX_KO_1A4.tif', cv2.IMREAD_UNCHANGED)
#image = cv2.imread('09_18_21_12h39m_32s_ms022__E02U2OS_SETX_KO_1A4.tif', cv2.IMREAD_UNCHANGED)

#img = cv2.imread('09_06_22_14h09m_10s_ms024__E03U2OS_53KO_5979GFP.tif', cv2.IMREAD_UNCHANGED)
# Normalize pixel values to 0-255 range
normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
cv2.imshow('Cells Detected 1', normalized)
cv2.waitKey(0)

blur = cv2.GaussianBlur(normalized,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Apply thresholding to get binary image
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imshow('thresh', thresh)
cv2.waitKey(0)
# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.
RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on original image
cv2.drawContours(blur, contours, -1, (0, 0, 255), 2)

# Display image with detected cells
cv2.imshow('Cells Detected', blur)
cv2.waitKey(0)

for contour in contours:
    # Obtain the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Crop the rectangle from the original image
    cropped = normalized[y:y+h, x:x+w]

    # Display the cropped image
    cv2.imshow('Cropped Image', cropped)
    cv2.waitKey(0)

cv2.destroyAllWindows()
