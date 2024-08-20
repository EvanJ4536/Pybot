import win32api, win32con, win32ui, win32gui
import numpy as np
from threading import Thread, Lock

class WindowCapture:
    
    #Size of screen
    w = 0
    h = 0
    
    hwnd = None
    
    stopped = True
    lock = None
    screenshot = None
    
    cropped_x = 0
    cropped_y = 0
    
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name):
        self.lock = Lock()
    
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found {}'.format(window_name))
        
        window_rect = win32gui.GetWindowRect(self.hwnd)

        self.w = window_rect[2] - window_rect[0] -5
        self.h = window_rect[3] - window_rect[1] -5
        
        border_pixels = 8
        titlebar_pixels = 40
        
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        
        self.offset_x = window_rect[0] + border_pixels
        self.offset_y = window_rect[1] - border_pixels
    
    def get_screenshot(self):

        #get image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        #convert to opencv image
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img
        
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        
    def stop(self):
        self.stopped = True
        
    def run(self):
        while not self.stopped:
            screenshot = self.get_screenshot()
            
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()