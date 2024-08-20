#Run this script in the lumbridge cow pen
#It will attempt to detect false positives and prevent clicking on the same spot over and over
#because of this it may get stuck in certain places for a while until its certain it has a match

import pybot as pb
import keyboard as kb
import cv2 as cv

def main():
    instance_list = []
    HWND = []
    false_positives = []
    
    w = 0
    h = 0
    previous_w = 0
    previous_h = 0
    
    non_fp_ctr = 0
    fp_click_ctr = 0
    dupe_click_ctr = 0
    win_ctr = 0
    n_ctr = 0
    
    DEFAULT_COW_CONFIDENCE = 0.66
    cow_confidence = 0.66
    
    adjust_confidence = False
    fp = False
    
    windows = pb.getWindows()
    for win in windows:
        if "RuneLite - " in win:
            instance_list.append(win)
            win_ctr += 1

    HWND = pb.getHwnd(instance_list)
    window_num = 0
    
    #HSV filter to single out cows on screen, obtained from HSV_filter_tool
    cow_hsv = [0, 38, 0, 24, 184, 255, 5, 0, 0, 0]  

    #Images that my script will look for on screen
    FULLRUN = cv.imread("fullrun.png")
    COW = cv.imread("cow1.png")
    HEALTHBAR = cv.imread("healthbar.png")
    
    while True:    
        user = input("Farm Cows (Y/n)\n\n>> ")
        
        if user.lower() == 'y':
            while True:
                pb.activateWindow(HWND, window_num)
                
                max_val, max_loc = pb.find(HEALTHBAR, HWND, window_num)
                if max_val >= 0.8:  #Try changing this if youre geting too many false positive or not enough matches. 
                                    #it goes from 0 to 1. 0: match everything. 1: match only exact matches to the photo
                    print("Fighting...") 
                    
                    if adjust_confidence == True:
                        print("Lowering confidence threshold...")
                        cow_confidence = DEFAULT_COW_CONFIDENCE
                        adjust_confidence = False
                    
                    pb.sleep(1,2)
                else:
                    max_val, max_loc = pb.find(COW, HWND, window_num, cow_hsv)
                    print(max_val)
                    
                    if max_val >= cow_confidence:
                        w, h = pb.getCenter(max_loc, COW)
                        str_w = str(w)
                        str_h = str(h)
                        
                        for pos in false_positives:
                            if str_w in pos and str_h in pos:
                                print("Matched FP, preventing dupe clicks.")
                                fp = True
                                break
                                
                        if fp:
                            fp_click_ctr += 1
                            non_fp_ctr = 0
                            fp = False
                            
                            if fp_click_ctr > 10:
                                print("Raising confidence threshold...")
                                cow_confidence = max_val + 0.01
                                adjust_confidence = True
                                
                            continue
                            
                        if w == previous_w and h == previous_h:
                            dupe_click_ctr += 1
                            if dupe_click_ctr > 3:
                                print("False positive detected, adding to blacklist.")
                                t = "{},{}".format(w,h)
                                false_positives.append(t)
                                continue
                        else:
                            dupe_click_ctr = 0
                                
                        e = pb.moveMouse(HWND, w, h, True, window_num)
                        
                        if e == 1:
                            e = 0
                            continue
                            
                        pb.sleep(0.1, 0.15)
                        pb.click()
                        pb.sleep(2.5, 3)
                        
                    else:
                        n_ctr += 1
                        if n_ctr > 5:    
                            print("Not finding good matches...")
                            n_ctr = 0
                            
                if window_num < win_ctr-1:
                    window_num +=1
                    
                else:
                    window_num = 0
                    
                previous_w = w
                previous_h = h
                
        if kb.is_pressed("q"):
            print(kb.is_pressed("q"))
            break
                   
        else:
            break
        
main()