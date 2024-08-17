import win32api, win32con, win32gui, win32ui
import random
import numpy as np
import cv2 as cv
import sys
import pytweening as pyt
from datetime import datetime
import time
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

#Prints all open window names, helpful when looking for true window name
def winEnumHandler(window_name, extra):
    if win32gui.IsWindowVisible(window_name):
        print(win32gui.GetWindowText(window_name))

#Calls EnumWindows
def printWindows():    
    win_list = win32gui.EnumWindows(winEnumHandler, None)
    
#Sets target window (hwnd)
#Parameters:
    #window_name: cell name of target window
        #may have to enum windows to find correct name
def getHwnd(window_name):
    global hwnd
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == None:
        print("Window Not Found. Exiting")
        sys.exit()
        
#Forces target window (hwnd) to foreground
def activateWindow():
    user32 = ctypes.windll.user32
    user32.SetForegroundWindow(hwnd)
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)

#Gets top left and bottom right coordinate of the target window
#for precise image capture and click mapping
def getWindow():
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    
    return x, y, x2, y2

#Convert datetime format to hours minutes seconds
def toHMS(start_time):
    t = time.time() - start_time
    m = t / 60
    s = t % 60
    if m >= 60:
        h = m / 60
        m = m % 60
    else:
        h = 0
    return int(h), int(m), int(s)

def close(ctr_total, start_time, action='ACTION'):
    h, m, s = toHMS(start_time)
    today = datetime.today()
    now = datetime.now()
    cur_time = now.strftime("%H:%M:%S")
    date_stamp = today.strftime("%b-%d-%Y")
    t_stamp = date_stamp + "::" + cur_time
    f = open('log.txt', 'a')
    f.write("{}  RUN TIME: {}:{}:{}  {}: {}\n".format(t_stamp, h,m,s, action, str(ctr_total)))
    f.close()

#Generates random float between low and high inclusive
#Parameters:
    #low: float for lowest possible value to generate
    #high: float for highest possible value to generate
def randNum(low, high):
    randNum = random.uniform(low, high)
    return randNum
    
def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(randNum(0.05,0.1))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    print("Right Click")
    

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(randNum(0.05,0.1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Click")
    
def clickHold(x, y, s):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    print("Click Hold")
    moveMouse(x, y, s)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Click Release")

#TODO: pass parameter for scroll amount
#Scroll up
def mouseScrollUp():
    print("Mouse Wheel Up")
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, 500)

#scroll down
def mouseScrollDown():
    print("Mouse Wheel Down")
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -500)


#sleep for a random amount of time between floats low and high inclusive
def sleep(low, high):
    r_num = randNum(low, high)
    print("Sleeping For {}".format(round(r_num, 2)))
    time.sleep(r_num)

#Moves mouse with upwards or downwards arc
#Parameters:
    #Takes x, y coordinates of point to move cursor to
    #s for speed, set to True for faster cursor movement
def moveMouse(x, y, s):  #TODO: add angle param to allow custom set arc heights
    offset_x = 8
    offset_y = 45
    
    x1, y1, x2, y2 = getWindow()
    
    x1 += offset_x
    y1 += offset_y 
        
    pos = win32api.GetCursorPos()
    orig_dest = [x, y]
    line = pyt.getLine(pos[0], pos[1], x+x1, y+y1)
    
    t = 0.0001
    if s:
        del line[::2]
        del line[::2]
        
    lines = np.array_split(line, 3)
    vert = random.randint(1,2)

    ctr = 0
    print("Moving Mouse")
    for point in lines[0]:
        x = point[0]
        y = point[1]
        y = y + ctr
        
        p = [x, y]
        win32api.SetCursorPos(p)
        
        if vert == 1:
            ctr += 1
        else:
            ctr -= 1
            
        time.sleep(t)
        
    for point in lines[1]:
        x, y = point
        y = y + ctr
        
        p = [x, y]
        win32api.SetCursorPos(p)
        time.sleep(t)
        
    for point in lines[2]:
        x = point[0]
        y = point[1]
        y = y + ctr
        
        p = [x, y]
        win32api.SetCursorPos(p)
        
        if vert == 1:
            ctr -= 1
        else:
            ctr += 1
            
        time.sleep(t)
        
#Get screenshot of current window
def getScreenshot(hsv):
    x, y, x2, y2 = getWindow()
    
    W = x2 - x - 5
    H = y2 - y - 5

    border_pixels = 8
    titlebar_pixels = 45

    W = W - (border_pixels * 2)
    H = H - titlebar_pixels - border_pixels
    cropped_x = border_pixels
    cropped_y = titlebar_pixels
    
    #get image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, W, H)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (W, H), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)

    #convert to opencv compatible image type
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (H, W, 4)

    #Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    #Drop alpha channel of photo
    img = img[...,:3]
    img = np.ascontiguousarray(img)

    if hsv != None:
        img = applyHsvFilter(img, hsv)

    return img

#Applies an hsv filter to the image before searching for your target 
#Pass filter into find function
#FORMAT:   
                  #0   1  2   3   4    5   6  7  8  9
    #hsv_filter = [9, 99, 0, 15, 255, 255, 0, 0, 0, 0]
def applyHsvFilter(original_img, hsv_filter):
    hsv = cv.cvtColor(original_img, cv.COLOR_BGR2HSV)
    
    h, s, v = cv.split(hsv)
    s = shift_channel(s, hsv_filter[6])
    s = shift_channel(s, -hsv_filter[7])
    v = shift_channel(v, hsv_filter[8])
    v = shift_channel(v, -hsv_filter[9])
    hsv = cv.merge([h, s, v])
   
    lower = np.array([hsv_filter[0], hsv_filter[1], hsv_filter[2]])
    upper = np.array([hsv_filter[3], hsv_filter[4], hsv_filter[5]])
    
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(hsv, hsv, mask=mask)
    
    img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
    

    
    return img
    
def shift_channel(c, amount):
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

#Searches for image on screen
#Parameters:
    #img: image file to search for on screen
def find(img, hsv=None):
    img = getScreenshot(hsv)

    #cv.imshow("test" ,img)
    #cv.waitKey(0)

    res = cv.matchTemplate(img, img, cv.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    return max_val, max_loc

def printBestMatch(loc, conf):
    print("best match: %s" % str(loc))
    print("confidence: %s" % conf)
    
#Returns coordinates of center of target image where found on screen
#TODO: Add small randomizations to clicks
def getCenter(max_loc, FILE):
    run_w = FILE.shape[1]
    run_h = FILE.shape[0]
    rw = run_w / 2
    rh = run_h / 2
    
    w = max_loc[0] + rw
    h = max_loc[1] + rh
    
    return w, h

