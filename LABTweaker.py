import cv2
import numpy as np

image_path = "20251121112237_1.jpg"  
image = cv2.imread(image_path)

lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

cv2.namedWindow("LAB Filter", cv2.WINDOW_NORMAL)

def nothing(x):
    pass

cv2.createTrackbar("L lower", "LAB Filter", 0, 255, nothing)
cv2.createTrackbar("A lower", "LAB Filter", 0, 255, nothing)
cv2.createTrackbar("B lower", "LAB Filter", 0, 255, nothing)

cv2.createTrackbar("L upper", "LAB Filter", 255, 255, nothing)
cv2.createTrackbar("A upper", "LAB Filter", 255, 255, nothing)
cv2.createTrackbar("B upper", "LAB Filter", 255, 255, nothing)

print("Use the sliders to adjust the LAB color range.")
print("Press ESC to exit.")

while True:
    lLower = cv2.getTrackbarPos("L lower", "LAB Filter")
    aLower = cv2.getTrackbarPos("A lower", "LAB Filter")
    b_lower = cv2.getTrackbarPos("B lower", "LAB Filter")

    lUpper = cv2.getTrackbarPos("L upper", "LAB Filter")
    aUpper = cv2.getTrackbarPos("A upper", "LAB Filter")
    bUpper = cv2.getTrackbarPos("B upper", "LAB Filter")

    lower = np.array([lLower, aLower, b_lower])
    upper = np.array([lUpper, aUpper, bUpper])

    mask = cv2.inRange(lab, lower, upper)
    filtered = cv2.bitwise_and(image, image, mask=mask)

    combined = np.hstack((image, filtered))
    cv2.imshow("LAB Filter", combined)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()