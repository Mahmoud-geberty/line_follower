import cv2
import sys, os
from time import sleep

import path
import motor as robot
import sensor
from sensor import width, height, sensors

cap = cv2.VideoCapture(0)     #opencv reads video from camera ---- if couldnt read then change from 0 to 1

# initial values for I controller
I = 0
last_Error = 0

# set initial robot state
robot.state = robot.states['wait']
directions = []
junction = 0

loopCount = 0
while True:
    loopCount += 1
    try:
        ret, img = cap.read()
        img = cv2.resize(img, (width, height))
        imgT = sensor.thresholding(img)
        cx = sensor.getCountours(imgT,img)
        senout = sensor.getSensorOutput(imgT, sensors, img)
        bla, error = sensor.get_error(senout,cx)

        junction = senout[1]


        # setup and start moving
        if robot.state == robot.states['start']:
            if error > 10:
                print(f'minimize the error first: {error}')
            else: 
                print('about to start, let go of the robot')
                sleep(3)
                robot.state = robot.states['follow']

        # TEMP: stop when junction is detected
        if junction: 
            robot.state = robot.states['j_turn']

        # stop and call api if state is 'wait'
        if robot.state == robot.states['wait']:
            robot.stop()
            msg = path.get_path()
            if msg != 'None':
                directions = path.normalize_path(msg) 
                print(f'received directions: {directions}')
                robot.state = robot.states['start']

        # handle junctions and go to the correct direction as per the path
        if robot.state == robot.states['j_turn']:
            if len(directions): inst = directions.pop(0)
            else: inst = ''
            
            if inst == 'straight':
                robot.go_straight()
            elif inst == 'right':
                robot.turn_right()
            elif inst == 'left':
                robot.turn_left()
            else:
                robot.state = robot.states['end']
                continue

            robot.state = robot.states['follow']

        # command robot to follow line
        if robot.state == robot.states['follow']:
            I = I + error
            robot.steer(error, junction, I, last_Error)
            last_Error = error

        # handle end state
        if robot.state == robot.states['end']:
            robot.stop()
            print("It seems that the destination is reached.")

        #diplay normal and hsv adjusted
        #cv2.imshow('final', img)   ## showing actual video
        #cv2.imshow('black and white',imgT) ## shows black and white
        #cv2.waitKey(1)

        #escape key to break
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)
        break

