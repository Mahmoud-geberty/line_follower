import cv2
import sys, os
import motor as robot
import sensor
from sensor import width, height, sensors

cap = cv2.VideoCapture(0)     #opencv reads video from camera ---- if couldnt read then change from 0 to 1

I = 0
last_Error = 0
while True:
    try:
        ret, img = cap.read()
        img = cv2.resize(img, (width, height))
        imgT = sensor.thresholding(img)
        cx = sensor.getCountours(imgT,img) ## translation
        senout = sensor.getSensorOutput(imgT, sensors, img) ## rotation
        direction = sensor.get_error(senout,cx)

        # some computation that couldn't be done in the robot module
        I = I + direction[1]
        robot.steer(direction[0], direction[1], senout[1], I, last_Error)
        last_Error = direction[1]

        #diplay normal and hsv adjusted
        cv2.imshow('final', img)   ## showing actual video
        cv2.imshow('black and white',imgT) ## shows black and white
        cv2.waitKey(1)

        #escape key to break
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)

    finally: 

        pass
        # robot.gpio.cleanup()
