# Pybot
Useful functions for making bot scripts for simple games like runescape or flash games.  
Uses OpenCV Template Matching and HSV filtering for more refined image detection.  
Supports multiple instances at the same time.  
Supports windows only.  

**Be mindful with the use of the functions that manipulate the mouse and active window in loops, a simple logic error could have the window stuck on the foreground**

## Dependencies
-pywin32    
-numpy  
-opencv-python  

```
pip install pywin32 numpy opencv-python
```

## HSV Filter Format  

```
FORMAT:   
0 - Hue min, 1 - Saturation min, 2 - Value min, 3 - Hue max, 4 - Sat max, 5 - Val max, 6 - Sat add, 7 - Sat sub, 8 - Val add, 9 - Val sub
                      0   1  2   3   4    5   6  7  8  9
hsv_filter_example = [9, 99, 0, 15, 255, 255, 0, 0, 0, 0]
```

## Usage
### Pybot  
Just import it into your script.

To use the find function you will want to use the windows snipping tool to take screenshots of what you want to find on screen and either put it  
in the same folder as your script or supply the path when reading it.

**Check the examples folder and the function usage below, the scripts are very easy to write**  


### HSV Filter Tool  
Download the HSV_filter_tool folder and run main.py while Runescape is running.  

-----------------------------------------------------------------------------------------------------------------------------------------
**getScreenshot(hwnd_list, hsv, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of window handles  
&emsp;&emsp;-hsv: List of HSV filter values  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp;-Returns image bitmap as contiguous array  

Example:
```python
img = getScreenshot(hwnd_list, hsv, instance_num)

target = "locate_me.png"
res = cv.matchTemplate(img, target, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
```

-----------------------------------------------------------------------------------------------------------------------------------------
**find(target, hwnd_list, instance_num=0, hsv=None):**  
&emsp;&emsp;-target: Path to image target image file  
&emsp;&emsp;-hwnd_list: List of window handles  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  
&emsp;&emsp;-hsv: List of HSV filter values  

&emsp;-Returns the confidence level and a list containing a point x, y where x and y are the coordinates of the best match found.

Example:
```python
pybot.activateWindow(hwnd_list, instance_num)

max_val, max_loc = pybot.find(HEALTHBAR, hwnd_list, instance_num)
if max_val >= 0.8:  #Confidence value. Try changing this if youre geting too many false positive or not enough matches. 
  ...               #it goes from 0 to 1. 0: match everything. 1: match only exact matches to the photo
```

-----------------------------------------------------------------------------------------------------------------------------------------
**getWindows():**  
&emsp;-Returns a list of true open window names.

  Example:
```python
instance_list = []
win_ctr = 0
windows = pybot.getWindows()
for win in windows:
    if "RuneLite - " in win:
        instance_list.append(win)
        win_ctr += 1
```

-----------------------------------------------------------------------------------------------------------------------------------------
**getHwnd(instance_list):**  
&emsp;&emsp;-window_names: Type: List. Cell name/names of target window. you may have to getWindows() to find correct name.  

&emsp;-Returns a list of window handles.  

Example:
```python
HWND_LIST = pybot.getHwnd(instance_list)
```

-----------------------------------------------------------------------------------------------------------------------------------------
**activateWindow(hwnd_list, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of target window handles.  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp;-Forces target window to foreground.  

Example:
```python
pybot.activateWindow(hwnd_list, instance_num)
```

-----------------------------------------------------------------------------------------------------------------------------------------
**getWindowPos(hwnd_list, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of target window handles.  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp;-Returns top left and bottom right coordinates of the target window for precise image capture and click mapping.  

Example:  
```python
topLeftX, topLeftY, bottomRightX, bottomRightY = pybot.getWindowPos(hwnd_list, instance_num)
```

-----------------------------------------------------------------------------------------------------------------------------------------
**moveMouse(hwnd_list, x, y, s, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of window handles  
&emsp;&emsp;-x, y: coordinates to move cursor to  
&emsp;&emsp;-s: speed, set to True for faster cursor movement  
&emsp;&emsp;instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp-Gets all integer coordinates from the current cursor position to the destination and moves the mouse along the line. Applies an upward or downward slope.  

Example:
```python
e = pybot.moveMouse(hwnd_list, w, h, True, instance_num)
if e == 1:  #Error occurred calculating points on line
    e = 0
    continue
```

-----------------------------------------------------------------------------------------------------------------------------------------
**getCenter(loc, FILE):**  
&emsp;&emsp;-loc: Top left coordinates of detected match  
&emsp;&emsp;-FILE: image file loaded by open-cv2  

&emsp;-returns coordinates of the center of an image loaded by open-cv2

Example:
```python
SCORPION = cv.imread("scorpion.png")
scorpion_hsv = [0, 0, 0, 0, 255, 65, 0, 0, 25, 0]

max_val, max_loc = pybot.find(SCORPION, hwnd_list, instance_num, scorpion_hsv)

if max_val >= 0.5:
    x, y = pybot.getCenter(max_loc, SCORPION)
    e = pybot.moveMouse(hwnd_list, x, y, True, instance_num)
    if e == 1:  #Error Occurred
        e = 0
        return 1
```

-----------------------------------------------------------------------------------------------------------------------------------------
**randNum(low, high):**  
&emsp;&emsp;-low: float for lowest possible value to generate.  
&emsp;&emsp;-high: float for highest possible value to generate.  

&emsp;-Returns random float between low and high inclusive.  

```python
time.sleep(randNum(0.05,0.1))
```

-----------------------------------------------------------------------------------------------------------------------------------------
**rightClick():**  
&emsp;-Presses the right mouse button  

-----------------------------------------------------------------------------------------------------------------------------------------
**click():**  
&emsp;-Presses the left mouse button  

-----------------------------------------------------------------------------------------------------------------------------------------
**clickHold(hwnd_list, x, y, s=False, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of window handles  
&emsp;&emsp;-x: Destination x  
&emsp;&emsp;-y: Destination y  
&emsp;&emsp;-s: Speed, False=normal, True=fast  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp;-Presses the left mouse button and drags the cursor to x, y

-----------------------------------------------------------------------------------------------------------------------------------------
**mouseScrollUp():**  
&emsp;-Scrolls the mouse wheel up  

-----------------------------------------------------------------------------------------------------------------------------------------
**mouseScrollDown():**  
&emsp;-Scrolls the mouse wheel down  

-----------------------------------------------------------------------------------------------------------------------------------------
**sleep(low, high):**  
&emsp;-Sleep for a random amount of time between floats low and high inclusive  

-----------------------------------------------------------------------------------------------------------------------------------------
**getLine(x1, y1, x2, y2):**  
&emsp;&emsp;-x1: Current x  
&emsp;&emsp;-y1: Current y  
&emsp;&emsp;-x2: Destination x  
&emsp;&emsp;-y2: Destination y  

&emsp;-Returns list of all coordinates of a line between two points.  

-----------------------------------------------------------------------------------------------------------------------------------------
**applyHsvFilter(original_img, hsv_filter):**  
&emsp;&emsp;-original_img: contiguous array of a bitmap  
&emsp;&emsp;-hsv_filter: HSV values list  

&emsp;-Returns altered image  

Example:
```python
scorpion_hsv = [0, 0, 0, 0, 255, 65, 0, 0, 25, 0]

altered_img = applyHsvFilter(img, scorpion_hsv):
```

-----------------------------------------------------------------------------------------------------------------------------------------
**printMatch(loc, conf):**  
&emsp;&emsp;-loc: Coordinates of match found on screen  
&emsp;&emsp;-conf: Confidence of match found on screen  


