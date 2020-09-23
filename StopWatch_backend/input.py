from time import sleep
import RPi.GPIO as GPIO
import json

GPIO.setmode(GPIO.BOARD)
button_1 = 40
button_2 = 38
button_3 = 36

GPIO.setup(button_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_3, GPIO.IN, pull_up_down = GPIO.PUD_UP)

input = {"Button_1": False, "Button_2": False, "Button_3": False}

def get_input():
    if GPIO.input(button_1) == 0:
        input["Button_1"] = True
    else:
        input["Button_1"] = False

    if GPIO.input(button_2) == 0:
        input["Button_2"] = True
    else:
        input["Button_2"] = False

    if GPIO.input(button_3) == 0:
        input["Button_3"] = True
    else:
        input["Button_3"] = False

    return json.dumps(input)