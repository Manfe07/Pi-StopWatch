import datetime
import RPi.GPIO as GPIO
import json

with open("../config.json") as json_data_file:
    config = json.load(json_data_file)

class Stopwatch:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.stop_time_lane1 = datetime.datetime.now()
        self.button_1 = button(config["rpi"]["button_1"])
        self.button_2 = button(config["rpi"]["button_2"])
        self.button_3 = button(config["rpi"]["button_3"])
        self.button_R = button(config["rpi"]["button_R"])
        self.led_Red = led(config["rpi"]["led_armed"])
        self.lane_1 = lane()
        self.lane_2 = lane()
        self.lane_3 = lane()
        self.running = False
        self.armed = True

    def start(self):
        if(self.running == False):
            self.running = True
            self.start_time = datetime.datetime.now()
            self.lane_1.start(self.start_time)
            self.lane_2.start(self.start_time)
            self.lane_3.start(self.start_time)
            return self.start_time
        else:
            return -1

    def check_Finish(self):
        if(self.lane_1.finished and self.lane_2.finished and self.lane_3.finished):
            self.running = False
            self.armed = False
            return True
        else:
            return False

    def get_runtime(self):
        runtime = datetime.datetime.now() - self.start_time
        return runtime

    def get_input(self):
        input = {"Button_1": False, "Button_2": False, "Button_3": False, "Button_R": False}
        input["Button_1"] = self.button_1.get_state()
        input["Button_2"] = self.button_2.get_state()
        input["Button_3"] = self.button_3.get_state()
        input["Button_R"] = self.button_R.get_state()
        return input

class button:
    def __init__(self, _pin):
        GPIO.setmode(GPIO.BOARD)
        self.pin = _pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self):
        if GPIO.input(self.pin) == 0:
            return True
        else:
            return False

class lane:
    def __init__(self):
        self.finished = False
        self.startTime = datetime.datetime.now()
        self.stopTime = datetime.datetime.now()

    def start(self, _startTime):
        self.startTime = _startTime
        self.finished = False

    def stop(self):
        if(self.finished == False):
            self.stopTime = datetime.datetime.now()
            self.finished = True

    def get_duration(self):
        duration = self.stopTime - self.startTime
        return duration

class led:
    def __init__(self, _pin):
        self.pin = _pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)

    def set_state(self, _state):
        if _state == True:
            GPIO.output(self.pin, 1)
        else:
            GPIO.output(self.pin, 0)