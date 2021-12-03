import cv2
import numpy as np

import RPi.GPIO as gpio
import motor as robot


hsvValues = [0, 0, 0, 179, 185, 105]  # values to reccog the the line 
# 0,0,0,179,72,148 (initial value tests on the pc)
sensors = 3   # numbers of sensors == numbers of sub screens
threshold = 0.2
vthreshold = 0.1
width , height = 480 , 360  # width and height of the screen ---- should be divisible by the number of sub screen/sensors
sensitivity = 4 # if number is high less sensitive
weights = [-25,-15,0,15,25]
curve = 0


def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvValues[0], hsvValues[1], hsvValues[2]])
    upper = np.array([hsvValues[3], hsvValues[4], hsvValues[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def getCountours(imgT, img ):
    countours, _ = cv2.findContours(imgT, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(countours) != 0 :
        biggest = max(countours,key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(biggest)
        cx = x+ w//2
        cy = y + h//2
        cv2.drawContours(img,countours,-1,(0,0,255),3)
        cv2.circle(img,(cx,cy),18,(255,0,0),3)

    return cx


def getSensorOutput(imgT, sensors, img): ## if the sensor have problem in detecting check here
    imgv = np.vsplit(imgT, sensors)
    imgs = np.hsplit(imgv[1],sensors)
    totalpixels = (img.shape[1]//(sensors * sensors)) * img.shape[0]
    senout= []

    # junction detection
    imgv = np.vsplit(imgv[0], sensors)[2]
    vpixels = (img.shape[1]//sensors ) * img.shape[0]
    vpix_count = cv2.countNonZero(imgv) 
    if vpix_count > vthreshold * vpixels:
        jn = 1
    else: jn = 0

    for x,im in enumerate(imgs):
        pixilcount = cv2.countNonZero(im)
        if pixilcount > threshold*totalpixels :
            senout.append(1)
        else:
            senout.append(0)
        cv2.imshow(str(x),im)


    return [senout, jn]


def get_error(senout,cx): 
    curve = 0
    ## translation
    lr = (cx - width//2) #//sensitivity
    lr = int(np.clip(lr,-200,200))
    if lr < 4 and lr >-4 : lr = 0 # tolerance for drone so it doesnt move always

    # rotation
    #normal cases
    if senout == [1,0,0]: curve = weights[0]
    elif senout == [1, 0, 0]: curve = weights[0]
    elif senout == [1, 1, 0]: curve = weights[1]
    elif senout == [0, 1, 0]: curve = weights[2]
    elif senout == [0, 1, 1]: curve = weights[3]
    elif senout == [0, 0, 1]: curve = weights[4]
    ## hard cases to happen
    elif senout == [0, 0, 0]: curve = weights[2]
    elif senout == [1, 1, 1]: curve = weights[2]
    elif senout == [1, 0, 1]: curve = weights[2]

    
    return [curve, lr]


        

