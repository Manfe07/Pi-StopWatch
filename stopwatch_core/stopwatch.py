import datetime
import RPi.GPIO as GPIO
import json

class Stopwatch:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.stop_time = datetime.datetime.now()
        self.button_1 = button(40)
        self.button_2 = button(38)
        self.button_3 = button(36)

    def start(self):
        self.start_time = datetime.datetime.now()
        return self.start_time

    def stop(self):
        self.stop_time = datetime.datetime.now()
        return self.stop_time

    def get_duration(self):
        duration = self.stop_time - self.start_time
        return duration

    def get_runtime(self):
        runtime = datetime.datetime.now() - self.start_time
        return runtime

    def get_input(self):
        input = {"Button_1": False, "Button_2": False, "Button_3": False}
        input["Button_1"] = self.button_1.get_state()
        input["Button_2"] = self.button_2.get_state()
        input["Button_3"] = self.button_3.get_state()
        return json.dumps(input)

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