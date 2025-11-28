import time
import cv2
import numpy as np
import mss

lowerWhite = np.array([220])
upperWhite = np.array([240])

lowTol = 50
highTol = 20
areaTol = 100
color = np.array([209, 189, 85])

hudtop = 1080-360

lower = np.array([color[0]-lowTol, color[1]-lowTol, color[2]-lowTol])
upper = np.array([color[0]+highTol, color[1]+highTol, color[2]+highTol])

with mss.mss() as sct:

    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    while "Screen capturing":
        lastTime = time.time()

        raw =  np.array(sct.grab(monitor))

        mod = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)

        hud = mod[hudtop:1080, 0:640]

        mask = cv2.inRange(mod, lower, upper)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        resultant = cv2.bitwise_and(raw, raw, mask= mask)
        grayed = cv2.cvtColor(resultant, cv2.COLOR_RGB2GRAY)
        
        ret, thresh = cv2.threshold(grayed, 0, 255, 0)
        contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # rect = cv2.minAreaRect(contours)
        # box = np.int0(cv2.boxPoints(rect))


        for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = w / float(h)

                    if aspect_ratio > 4 and w > 50:
                        cv2.drawContours(mod, [approx], -1, (255, 0, 0), 2)
            

        cv2.imshow("Mask", mask)
        cv2.imshow("Grayed", mod)
        # cv2.imshow("Edited", morphed)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
