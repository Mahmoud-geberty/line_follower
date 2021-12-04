'''
File: motor.py
Author: Mahmoud
description: Motor control logic and responding to 
    the line_detection outputs. communicate with the API for 
    finding the shortest path to the junction requested by the 
    mobile app end.
'''

import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(32, gpio.OUT)
gpio.setup(33, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
rm = gpio.PWM(32, 1000)
lm = gpio.PWM(33, 1000)
rm.start(0)
lm.start(0)

# manage the state of the car
states = {
        "wait": 0,
        "follow": 1,
        "j_turn": 2,
        "start": 3,
        "end": 4
    }


def setup():
    pass


def rm_forward(speed):
    gpio.output(18, True)
    gpio.output(16, False)
    rm.ChangeDutyCycle(speed)

def lm_forward(speed):
    gpio.output(11, False)
    gpio.output(13, True)
    lm.ChangeDutyCycle(speed)

def rm_backward(speed):
    gpio.output(18, False)
    gpio.output(16, True)
    rm.ChangeDutyCycle(speed);

def lm_backward(speed):
    gpio.output(11, True)
    gpio.output(13, False)
    lm.ChangeDutyCycle(speed)

def stop():
    gpio.output(18, False)
    gpio.output(16, False)
    gpio.output(11, False)
    gpio.output(13, False)

def straight(speed):
    rm_forward(speed)
    lm_forward(speed + 3)

def go_straight():
    print('going straight')
    rm_forward(35)
    lm_forward(35 + 3)
    sleep(0.4)

def start():
    straight(35)

def reverse(speed):
    rm_backward(speed)
    lm_backward(speed + 8)

def turn_right():
    sleep(0.5)
    stop()
    print('turning right')
    sleep(0.4)
    lm_forward(48)
    rm_backward(41)
    sleep(0.6)
    reverse(35)
    sleep(0.5)
    stop()

def turn_left():
    sleep(0.6)
    stop()
    print('turning left')
    sleep(0.4)
    rm_forward(41)
    lm_backward(48)
    sleep(0.7)
    reverse(35)
    sleep(0.5)
    stop()

''' 
given an error: that is the deviation from the center of the line, 
Use Pid controller to keep the car on the line

'''
P = 0
D = 0
def steer(error, jn, I, last_error):
    # error gain
    speed = 35
    Kp = 0.03
    Ki = 0#.0003
    Kd = 0.001
    P = error * Kp
    I = I * Ki
    D = (error - last_error) * Kd
    last_error = error
    print(f'error: {error}, jn: {jn} and PID {P + I + D}')
    r_tune = 5 # help make the base speed of each motor same

    #direction control using error only
    rm_forward(speed - (P + I + D))
    lm_forward(speed + (P + I + D))

# run the file as main to test the motors
if __name__ == '__main__':
    try:
        straight(35)
        sleep(4)
        stop()

        while True:
                pass

    except Exception as e:
        print(e)
