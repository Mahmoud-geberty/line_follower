import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)

gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(32, gpio.OUT)

gpio.output(18, True)
gpio.output(16, False)

# output pwm for motor 1
pwm = gpio.PWM(32, 1000)
pwm.start(50)

while True:
	pass
