import pybot as pb
import keyboard as kb
import cv2 as cv

def main():
    instance_list = []
    HWND = []
    win_ctr = 0
    n_ctr = 0
    windows = pb.getWindows()
    for win in windows:
        if "RuneLite - " in win:
            instance_list.append(win)
            win_ctr += 1

    HWND = pb.getHwnd(instance_list)
    window_num = 0

    scorpion_hsv = [0, 0, 0, 0, 255, 65, 0, 0, 25, 0]

    FULLRUN = cv.imread("fullrun.png")
    SCORPION = cv.imread("scorpion2.png")
    HEALTHBAR = cv.imread("healthbar.png")

    while True:    
        user = input("1.Farm Scorpions\n\n>> ")
        if user == '1':
            while True:
                pb.activateWindow(HWND, window_num)
                
                max_val, max_loc = pb.find(HEALTHBAR, HWND, window_num)
                if max_val >= 0.8:  #Try changing this if youre geting too many false positive or not enough matches. 
                                    #it goes from 0 to 1. 0: match everything. 1: match only exact matches to the photo
                    print("Fighting... changing window.") 
                    pb.sleep(1,2)
                else:
                    max_val, max_loc = pb.find(SCORPION, HWND, window_num, scorpion_hsv)
                    print(max_val)
                    if max_val >= 0.5:
                        w, h = pb.getCenter(max_loc, SCORPION)
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
        if keyboard.is_pressed("q"):
            print(keyboard.is_pressed("q"))
            break
                        
main()