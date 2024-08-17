import pybot as pb
import keyboard as kb
import cv2 as cv
import pyautogui as pya

def main():
    acc_list = []
    win_ctr = 0
    for win in pya.getAllWindows():
        if "RuneLite - " in win.title:
            acc_list.append(win.title)
            win_ctr += 1

    pb.getHwnd(acc_list)
    window_num = 0

    scorpion_hsv = [0, 0, 0, 0, 255, 65, 0, 0, 25, 0]

    FULLRUN = cv.imread("fullrun.png")
    SCORPION = cv.imread("scorpion2.png")
    HEALTHBAR = cv.imread("healthbar.png")

    while True:    
        user = input("1.Farm Scorpions\n\n>> ")
        if user == '1':
            while True:
                pb.activateWindow(window_num)
                
                max_val, max_loc = pb.find(HEALTHBAR, window_num)
                if max_val >= 0.8:
                    print("Fighting... changing window.") 
                    pb.sleep(1,2)
                else:
                    max_val, max_loc = pb.find(SCORPION, window_num, scorpion_hsv)
                    print(max_val)
                    if max_val >= 0.5:
                        w, h = pb.getCenter(max_loc, SCORPION)
                        pb.moveMouse(w, h, True, window_num)
                        pb.sleep(0.1, 0.15)
                        pb.click()
                        pb.sleep(2.5, 3)
                if window_num < win_ctr-1:
                    window_num +=1
                else:
                    window_num = 0
                print(window_num)
            
                        
main()