from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
button_1 = 40
button_2 = 38
button_3 = 36

GPIO.setup(button_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_3, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while(1):
    if GPIO.input(button_1) == 0:
        print "Button 1"
        sleep(.1)
    if GPIO.input(button_2) == 0:
        print "Button 2"
        sleep(.1)
    if GPIO.input(button_3) == 0:
        print "Button 3"
        sleep(.1)