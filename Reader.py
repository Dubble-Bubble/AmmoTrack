import cv2
import numpy as np
import mss

def preprocessMap(img: np.ndarray):
    h, w = img.shape[:2]
    K = np.array([[h/9*16,0,w/2],[0,h,h/2],[0,0,1]]) 
    # mock intrinsics
    h_,w_ = img.shape[:2]
    Kinv = np.linalg.inv(K)
    # pixel coordinates
    y_i, x_i = np.indices((h_,w_))
    # to homog
    X = np.stack([x_i,y_i,np.ones_like(x_i)],axis=-1).reshape(h_*w_,3) 
    # normalized coords
    X = Kinv.dot(X.T).T 
    # calculate cylindrical coords (sin\theta, h, cos\theta)
    A = np.stack([np.sin(X[:,0]),X[:,1],np.cos(X[:,0])],axis=-1).reshape(w_*h_,3)
    B = K.dot(A.T).T # project back to image-pixels plane
    # back from homog coords
    B = B[:,:-1] / B[:,[-1]]
    B = B.reshape(h_,w_,-1)
    return cv2.convertMaps(x_i.astype(np.float32), B[:, :, 1].astype(np.float32), cv2.CV_16SC2) 

#must supply a BGRA numpy array of same shape used in preprocessMap
#x_i and B supplied by preprocessMap
def preprocessedWarp(img: np.ndarray, x_i, B) -> np.ndarray:
    return cv2.remap(img, x_i, B, cv2.INTER_AREA)

class Mossynator:
    def __init__(self, img: np.ndarray ):
        x_i, B = preprocessMap(img)
        self.x_i = x_i
        self.B = B
    
    def map(self, img: np.ndarray ) -> np.ndarray:
        return preprocessedWarp(img, self.x_i, self.B)


class Reader():

    def readSpecialMeter(self):
        lowerGreen = np.array([100, 55, 125])
        upperGreen = np.array([193, 118, 156])
        floor = 80  
        cieling = 255
        with mss.mss() as sct:
            sctimg = sct.grab({"top": 0, "left": 0, "width": 1920, "height":1080})
            # sctimg = cv2.imread('spiderfullbounds.png')
            redef = np.array(sctimg)

            bgra = cv2.cvtColor(redef, cv2.COLOR_BGR2BGRA)
        
            mossynator = Mossynator(bgra)
            rotated = mossynator.map(bgra)

            cv2.imwrite("rot.jpg", rotated)

            trueRotated = rotated[1016:1017, 450:546]

            lab = cv2.cvtColor(trueRotated, cv2.COLOR_BGR2LAB)

            mask = cv2.inRange(lab, lowerGreen, upperGreen)
            result = cv2.bitwise_and(trueRotated, trueRotated, mask=mask)
            rGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            cv2.imwrite('filter.jpg', rGray)

            uselessSlop, thresh = cv2.threshold(rGray, floor, cieling, cv2.THRESH_BINARY)
        
            pxin = np.count_nonzero(thresh)
            pxtot = 96

            percentage = (pxin / pxtot) * 100
            print(f"Percentage of pixels within threshold: {percentage:.2f}%")
            
            return percentage, pxin


    def readHeavylMeter(self):
        lowerPurple = np.array([110, 129, 94])
        upperPurple = np.array([157, 150, 113])
        floor = 80  
        cieling = 255
        with mss.mss() as sct:
            sctimg = sct.grab({"top": 0, "left": 0, "width": 1920, "height":1080})
            # sctimg = cv2.imread('spiderfullbounds.png')
            redef = np.array(sctimg)

            bgra = cv2.cvtColor(redef, cv2.COLOR_BGR2BGRA)
        
            mossynator = Mossynator(bgra)
            rotated = mossynator.map(bgra)

            trueRotated = rotated[1016:1017, 576:672]

            lab = cv2.cvtColor(trueRotated, cv2.COLOR_BGR2LAB)

            mask = cv2.inRange(lab, lowerPurple, upperPurple)
            result = cv2.bitwise_and(trueRotated, trueRotated, mask=mask)
            rGray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            cv2.imwrite('filter.jpg', rGray)

            uselessSlop, thresh = cv2.threshold(rGray, floor, cieling, cv2.THRESH_BINARY)
        
            pxin = np.count_nonzero(thresh)
            pxtot = 96

            percentage = (pxin / pxtot) * 100
            print(f"Percentage of pixels within threshold: {percentage:.2f}%")
            
            return percentage, pxin    



