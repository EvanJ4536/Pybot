import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter

class Vision:
    
    TRACKBAR_WINDOW = 'HSV Filter Tool'
    
    img = None
    img_w = 0
    img_h = 0
    method = None

    def __init__(self, locate_img, method=cv.TM_CCOEFF_NORMED):
        if locate_img != None:
            self.img = cv.imread(locate_img)
            

            self.img_w = self.img.shape[1]
            self.img_h = self.img.shape[0]
            
            #Methods to choose from: TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
            self.method = method
        
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 100)
        
        def nothing(position):
            pass
        
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW , 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW , 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW , 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW , 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW , 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW , 0, 255, nothing)
        
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW , 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW , 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW , 255)
        
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW , 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW , 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW , 0, 255, nothing)        
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW , 0, 255, nothing)
        
    def get_hsv_filter_from_controls(self):
        #get current slider positions
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        
        return hsv_filter
        
    def apply_hsv_filter(self, original_img, hsv_filter=None):
        hsv = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)
        
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()
        
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])
       
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)
        
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        
        return img
        
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c