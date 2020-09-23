from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
button_1 = 12

GPIO.setup(button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(1):
    if GPIO.input(button_1) == 0:
        print "Button 1"
        sleep(.1)