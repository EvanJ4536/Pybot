# Pybot
Useful functions for making bots scripts for simple games like runescape or flash games, using OpenCV Template Matching.  
Support multiple instances at the same time.  
Supports windows only.  

# Dependencies
-pywin32    
-numpy  
-opencv-python  

```
pip install pywin32 numpy opencv-python
```

# Usage
just import it into your script.

-------------------------------------------------------------------------------------------------------------------------

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
**getHwnd(window_names):**  
&emsp;&emsp;-window_names: Type: List. Cell name/names of target window. you may have to getWindows() to find correct name.  

&emsp;-Returns a list of window handles.  

Example:
```python
HWND_LIST = pybot.getHwnd(instance_list)
```
**activateWindow(hwnd_list, instance_num=0):**  
&emsp;&emsp;-hwnd_list: List of target window handles.  
&emsp;&emsp;-instance_num: Index number for hwnd_list.  Default is 0 for one instance.  

&emsp;-Forces target window to foreground.  

Example:
```python
pybot.activateWindow(HWND, window_num)
```
