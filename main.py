from pynput.mouse import Button, Controller
import pynput
import time
import keyboard
import mss,mss.tools
from cv2 import cv2
from threading import Thread
mouse = Controller()
kb = pynput.keyboard.Controller()

tank = 0
is_rollin = True
def click(x,y):
    global mouse
    mouse.release(Button.left)
    time.sleep(0.1)
    mouse.position = (x,y)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.2)
    mouse.release(Button.left)
    time.sleep(0.5)

def stop():
    global is_rollin
    is_rollin = False


keyboard.add_hotkey("q", lambda: stop())
keyboard.add_hotkey("r", lambda: start_sequence())
keyboard.add_hotkey("f", lambda: sell())
keyboard.add_hotkey("g", lambda: reset())
keyboard.add_hotkey("e", lambda: start_main_loop())
def sell():
    click(900,500) #click onto shop  
    click(475,320) #select all
    click(950,900) #sell
    click(1100,780) #confirm
    click(70,780) #exit  

def reset():
    global tank
    tank = 0
    kb.press('w')
    time.sleep(5)
    kb.release('w')
    sell()
    kb.press('s')
    time.sleep(5)
    kb.release('s')

def start_sequence():
    reset()
    catch()

def throw():
    global mouse
    mouse.release(Button.left)
    time.sleep(0.1)
    mouse.position = (900,900)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(1.5)
    mouse.release(Button.left)
    time.sleep(0.5)
    
exc_img = cv2.imread('exc.png', cv2.IMREAD_GRAYSCALE) 
float_img = cv2.imread('float.png', cv2.IMREAD_GRAYSCALE)
side_img = cv2.imread('side.png', cv2.IMREAD_GRAYSCALE) 
button_img = cv2.imread('x_button.png', cv2.IMREAD_GRAYSCALE)  
def catch():
    global tank
    while is_rollin:
        if tank >=6:
            reset()
        throw()
         
        print('Finding fish')
        for i in range(20):
            time.sleep(1)
            with mss.mss() as sct:
                monitor = {"top": 400, "left": 880, "width": 170, "height": 125}
                output = "monitor-1.png".format(**monitor)
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) 

            screen_img = cv2.imread('monitor-1.png', cv2.IMREAD_GRAYSCALE)  
            result = cv2.matchTemplate(screen_img,exc_img,cv2.TM_CCOEFF_NORMED)            
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
            if max_val >0.9:
                print("Fish found") 
                break
        click(900,900)
        

        with mss.mss() as sct:
                monitor = {"top": 780, "left": 610, "width": 700, "height": 100}
                output = "monitor-1.png".format(**monitor)
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) 
        screen_img = cv2.imread('monitor-1.png', cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screen_img,float_img,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
        if max_val >0.9:
            print("Start catching") 
        else:
            print("Fish not found") 
            catch()

        rep = 0
        elapsed = time.time()
        i = 0
        while True:
            i+=1            
            with mss.mss() as sct:
                    monitor = {"top": 810, "left": 620, "width": 660, "height": 60}
                    output = "monitor-1.png".format(**monitor)
                    sct_img = sct.grab(monitor)
                    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) 
            screen_img = cv2.imread('monitor-1.png', cv2.IMREAD_GRAYSCALE)  
            result = cv2.matchTemplate(screen_img,float_img,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)         
            if max_val<0.7:
                break
            x_float = max_loc[0] 
            result = cv2.matchTemplate(screen_img,side_img,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
            x_side = max_loc[0] +30            
            # cv2.line(screen_img, (x_side, 0), (x_side, 41), (0, 0, 0), 2)
            # cv2.line(screen_img, (x_float, 0), (x_float, 41), (0, 255, 0), 2)
            # cv2.imwrite(f'1//{i}.png', screen_img)  
            rep+=1               
            if x_side>x_float and x_side<=750:                
                mouse.press(Button.left)
            else:                
                mouse.release(Button.left)
        elapsed = time.time() - elapsed
        print(f'speed {rep/elapsed}')
        print ('End of catching') 
        time.sleep(2)
        with mss.mss() as sct:
                monitor = {"top": 600, "left": 600, "width": 800, "height": 400}
                output = "monitor-1.png".format(**monitor)
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) 
        screen_img = cv2.imread('monitor-1.png', cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screen_img,button_img,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)        
        if max_val>0.8:
            tank+=1        
            print(f'Fish catched, total: {tank}')            
            click(70,780) #exit 
            click(70,780) #exit 
        else:
            print('Fish escaped')


def main():    
    while True:
        pass

def start_main_loop():
    t = Thread(target=catch, daemon=True)
    t.start()
    
if __name__ == "__main__":
	main()