#Python HSV Editor
import cv2 as cv
import pybot as pb
from WindowCapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

windows = pb.getWindows()
for win in windows:
    if "RuneLite - " in win:  #Edit this to capture whatever window you want
        target = win
        break

wincap = WindowCapture(target)

not_found = 0
DEBUG = False

default_filter = HsvFilter(0, 0, 0, 255, 255, 255, 0, 0, 0, 0)
cow_vision = Vision(None)


vision = cow_vision
DEBUG = True
vision.init_control_gui()

wincap.start()
try:
    while True:
        if wincap.screenshot is None:
            continue

        processed_img = vision.apply_hsv_filter(wincap.screenshot, None)
        
        cv.imshow('HSV Editor', processed_img)
        
        key = cv.waitKey(1)
        if key == ord('q'):
            wincap.stop()
            break
    
except KeyboardInterrupt:
    wincap.stop()

cv.destroyAllWindows()
    