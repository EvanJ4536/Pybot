import pybot as pb
import cv2 as cv
import keyboard as kb
import sys

def main():
    pb.getHwnd('Old School RuneScape')
    
    print("Initializing Images...")
    OPERATOR = cv.imread('sawmilloperator.png')
    TRADE = cv.imread('trade.png')
    NAILSIRON = cv.imread('nailshop.png')
    NAILS = cv.imread('bronzenail.png')
    BUYNAILS = cv.imread('buybronze.png')
    BUYNAILSIRON = cv.imread('buynails.png')
    XBUTTON = cv.imread('x.png')
    WORLDSWITCHER = cv.imread('worldswitcher.png')
    WORLD = cv.imread('world.png')
    SWITCH = cv.imread('switch.png')
    
    print("Success.\nForcing Window To Foreground")
    
    pb.activateWindow()
    
    scroll_ctr = 0
    scroll = True
    
    #hsv_filter = [9, 0, 0, 200, 255, 255, 0, 0, 0, 0]
    
    print("Starting Bot")
    while True:
        world_ctr = 1
        while world_ctr <= 1:
            kb.send('esc')
            max_val, max_loc = pb.find(OPERATOR)
            if max_val >= 0.6:
                w, h = pb.getCenter(max_loc, OPERATOR)
                pb.moveMouse(w, h, False)
                pb.sleep(0.3, 0.5)
                pb.rightClick()

                max_val, max_loc = pb.find(TRADE)
                if max_val >= 0.9:
                    w, h = pb.getCenter(max_loc, TRADE)
                    pb.moveMouse(w, h, False)
                    pb.sleep(0.2, 0.4)
                    pb.click()
                    pb.sleep(2.3, 2.5)
                    
                    ctr = 0
                    while ctr <= 4:
                        max_val, max_loc = pb.find(NAILSIRON)
                        if max_val >= 0.6:
                            w, h = pb.getCenter(max_loc, NAILSIRON)
                            pb.moveMouse(w, h+20, False)
                            pb.sleep(0.7, 0.9)
                            
                            pb.rightClick()
                            
                            max_val, max_loc = pb.find(BUYNAILSIRON)
                            if max_val >= 0.9:
                                w, h = pb.getCenter(max_loc, BUYNAILSIRON)
                                pb.moveMouse(w, h, False)
                                pb.click()
                            pb.sleep(0.3, 0.5)
                            ctr += 1
                    while ctr <= 8:        
                            max_val, max_loc = pb.find(NAILS)
                            if max_val >= 0.6:
                                w, h = pb.getCenter(max_loc, NAILS)
                                pb.moveMouse(w, h+20, False)
                                pb.sleep(0.7, 0.9)
                                
                                pb.rightClick()
                                
                                max_val, max_loc = pb.find(BUYNAILS)
                                if max_val >= 0.9:
                                    w, h = pb.getCenter(max_loc, BUYNAILS)
                                    pb.moveMouse(w, h, False)
                                    pb.click()
                                pb.sleep(0.7, 0.9)
                                ctr += 1
                            
                    kb.send('esc')
                    pb.sleep(0.3, 0.5)
                    
                    print("searching for x button")
                    max_val, max_loc = pb.find(XBUTTON)
                    if max_val >= 0.6:
                        w, h = pb.getCenter(max_loc, XBUTTON)
                        pb.moveMouse(w, h ,False)
                        pb.click()
                        pb.sleep(0.5, 0.7)
                        
                        max_val, max_loc = pb.find(WORLDSWITCHER)
                        if max_val >= 0.9:
                            w, h = pb.getCenter(max_loc, WORLDSWITCHER)
                            pb.moveMouse(w, h, False)
                            pb.click()
                            pb.sleep(2, 2.5)
                            
                        max_val, max_loc = pb.find(WORLD)
                        if max_val >= 0.45:
                            w, h = pb.getCenter(max_loc, WORLD)
                            pb.moveMouse(w, h, False)
                            pb.click()
                            pb.sleep(2, 2.5)
                        
                            max_val, max_loc = pb.find(SWITCH)
                            if max_val >= 0.7:
                                w, h = pb.getCenter(max_loc, SWITCH)
                                pb.moveMouse(w, h, False)
                                pb.click()
                                pb.sleep(15, 17)
                        world_ctr += 1
            else:
                max_val, max_loc = pb.find(XBUTTON)
                if max_val >= 0.7:
                    w, h = pb.getCenter(max_loc, XBUTTON)
                    pb.moveMouse(w, h ,False)
                    pb.click()
                    pb.sleep(0.5, 0.7)
                    
                    max_val, max_loc = pb.find(WORLDSWITCHER)
                    if max_val >= 0.9:
                        w, h = pb.getCenter(max_loc, WORLDSWITCHER)
                        pb.moveMouse(w, h, False)
                        pb.click()
                        pb.sleep(2, 2.5)
                        
                    max_val, max_loc = pb.find(WORLD)
                    if max_val >= 0.45:
                        w, h = pb.getCenter(max_loc, WORLD)
                        pb.moveMouse(w, h, False)
                        pb.click()
                        pb.sleep(2, 2.5)
                    
                        max_val, max_loc = pb.find(SWITCH)
                        if max_val >= 0.7:
                            w, h = pb.getCenter(max_loc, SWITCH)
                            pb.moveMouse(w, h, False)
                            pb.click()
                            pb.sleep(15, 17)
                    world_ctr += 1
                
        max_val, max_loc = pb.find(WORLD)
        if max_val >= 0.45:
            w, h = pb.getCenter(max_loc, WORLD)
            pb.moveMouse(w, h, False)
 
            pb.sleep(0.5, 0.7)
            
            if scroll:
                pb.mouseScrollUp()
                scroll_ctr += 1
                if scroll_ctr >= 9:
                    scroll = False
            else:
                pb.mouseScrollDown()
                scroll_ctr -= 1
                if scroll_ctr <= 0:
                    scroll = True
                
            pb.sleep(0.7, 1)
            world_ctr = 1
                            

main()