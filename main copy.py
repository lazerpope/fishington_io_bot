from cv2 import cv2
import mss

def main1():
    with mss.mss() as sct:
        filename = sct.shot()
        print(filename)
    a = 100,50
    print(a[1])

def main(): 

    with mss.mss() as sct:
            monitor = {"top": 780, "left": 610, "width": 700, "height": 100}
            output = "monitor-1.png".format(**monitor)
            sct_img = sct.grab(monitor)
            #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) 
    screen_img = cv2.imread('3.png', cv2.IMREAD_GRAYSCALE)    
    float_img = cv2.imread('5.png', cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen_img,float_img,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
    if max_val >0.9:
        print(max_loc)
        print("Start catching") 

if __name__ == "__main__":
	main1()

#cv2.imshow('screen_img',screen_img)
#cv2.waitKey()