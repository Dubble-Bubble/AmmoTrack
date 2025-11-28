import cv2
import numpy as np
# hey guys, harm from d2foundry here
# if you look at this function and ask me whats going on
# i will block you on discord
# thx mossy

# must supply a BGRA numpy array 
# returns x_i and B to be used for preprocessedWarp
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

class MossynatorFunc:
    def __init__(self, img: np.ndarray ):
        x_i, B = preprocessMap(img)
        self.x_i = x_i
        self.B = B
    
    def map(self, img: np.ndarray ) -> np.ndarray:
        return preprocessedWarp(img, self.x_i, self.B)