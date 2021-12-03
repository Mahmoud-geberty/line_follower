'''
File: motor.py
Author: Mahmoud
description: Motor control logic and responding to 
    the line_detection outputs. communicate with the API for 
    finding the shortest path to the junction requested by the 
    mobile app end.
'''

import RPi.GPIO as gpio
import time

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

# polling the server for a command from mobile app
current_state = states['wait']


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

def start():
    straight(35)

def reverse(speed):
    rm_backward(speed)
    lm_backward(speed)

''' 
given an error: that is the deviation from the center of the line, 
Use Pid controller to keep the car on the line

'''
P = 0
D = 0
def steer(curve, error, jn, I, last_error):
    # error gain
    speed = 40
    Kp = 0.05
    Ki = 0.0003
    Kd = 0.02
    P = error * Kp
    I = I * Ki
    D = (error - last_error) * Kd
    last_error = error
    print(f'received: curve: {curve}, error: {error}, jn: {jn} and PID {P + I + D}')
    r_tune = 5 # help make the base speed of each motor same

    #direction control using error only
    rm_forward(speed - (P + I + D))
    lm_forward(speed + (P + I + D))


if __name__ == '__main__':
    try:
        straight(40)
        time.sleep(3)
        stop()
        time.sleep(1)
        reverse(40)
        time.sleep(3)
        stop()

        while True:
                pass

    except Exception as e:
        print(e)
