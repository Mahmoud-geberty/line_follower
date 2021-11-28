import cv2
import numpy as np
# from djitellopy import tello  #not important for ur part (drone library )
# connect with drone
# me = tello.Tello()
# me.connect()
# print(me.get_battery()) # get battery value
# start stream and capture video
# me.streamon()
# me.takeoff()
# end of drone insruct


cap = cv2.VideoCapture(0)     #opencv reads video from camera ---- if couldnt read then change from 0 to 1
hsvValues = [0, 0, 117, 179, 22, 219]  # values to reccog the the line --- numbers is givin by a script i will send it to u
sensors = 3   # numbers of sensors == numbers of sub screens
threshold = 0.2
width , height = 488 , 360  # width and height of the screen ---- should be divisible by the number of sub screen/sensors
sensitivity = 3 # if number is high less sensitive
wighits = [-25,-15,0,15,25]
curve = 0
FWspeed = 15



# dont change this func
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


def getSensorOutput(imgT,sensors): ## if the sensor have problem in detecting check here
    imgs = np.hsplit(imgT,sensors)
    totalpixels = (img.shape[1]//sensors) * img.shape[0]
    senout= []
    for x,im in enumerate(imgs):
        pixilcount = cv2.countNonZero(im)
        if pixilcount > threshold*totalpixels :
            senout.append(1)
        else:
            senout.append(0)
        cv2.imshow(str(x),im)
    print(senout)
    return senout


def sendCommands(senout,cx): ## this function to send comands to the vieihecle ---- u can change here to command
    global curve
    ## translation
    lr = (cx - width//2)//sensitivity
    lr = int(np.clip(lr,-10,10))
    if lr < 2 and lr >-2 : lr = 0 # tolerance for drone so it doesnt move always

    # rotation
    #normal cases
    if senout == [1,0,0]: curve = wighits[0]
    elif senout == [1, 0, 0]: curve = wighits[0]
    elif senout == [1, 1, 0]: curve = wighits[1]
    elif senout == [0, 1, 0]: curve = wighits[0]
    elif senout == [0, 1, 1]: curve = wighits[3]
    elif senout == [0, 0, 1]: curve = wighits[4]
    ## hard cases to happen
    elif senout == [0, 0, 0]: curve = wighits[2]
    elif senout == [1, 1, 1]: curve = wighits[2]
    elif senout == [1, 0, 1]: curve = wighits[2]
	# me.send_rc_control(lr,FWspeed,0,curve)



while True:
    ret, img = cap.read()
	# img = me.get_frame_read().frame
    img = cv2.resize(img, (width, height)) #size shoudle be divisible by the nubmer of the sensors otherwise it wont work
    # img=cv2.flip(img,0) #flip the camera cuz i am using mirror in the drone
    imgT = thresholding(img)
    cx = getCountours(imgT,img) ## translation
    senout = getSensorOutput(imgT,sensors) ## rotation

    sendCommands(senout,cx)


    #diplay normal and hsv adjusted
    cv2.imshow('final', img)   ## showing actual video
    cv2.imshow('black and white',imgT) ## shows black and white
    cv2.waitKey(1)

    #escape key to break
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

