import json
import paho.mqtt.client as mqtt
import stopwatch
import schedule
import time
from camera import Camera

with open("../config.json") as json_data_file:
    config = json.load(json_data_file)


if (config["x750"]["enable"] == True):
    import x750ups as x750

elif (config["INA819"]["enable"] == True):
    import INA219 as INA219

mqttHost = config["mqtt"]["host"]
mqttPort = config["mqtt"]["port"]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("stopwatch/webInput/#")
#    subscribe.callback(on_message_print, "stopwatch/webInput/#", hostname="localhost")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('UTF-8')))
    if(msg.topic == "stopwatch/webInput/armed"):
        if(msg.payload.decode('UTF-8') == "true"):
            arm(True)
        else:
            arm(False)


cam = Camera(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttHost, mqttPort, 60)

client.loop_start()

stopwatch = stopwatch.Stopwatch()

old_input = stopwatch.get_input()

first = True

def doIfFirst():
    global first
    if first:
        first = False
        if cam.cameraEnabled:
            cam.takePicture()

def arm(_state):
    if _state == True:
        stopwatch.armed = True
        stopwatch.led_Red.set_state(True)
        client.publish("stopwatch/armed", "true", retain=True)
    else:
        stopwatch.armed = False
        stopwatch.led_Red.set_state(False)
        client.publish("stopwatch/armed", "false", retain=True)


def post_UPS():
    if(config["x750"]["enable"] == True):
        voltage = "{:10.2f}".format(float(x750.getVolage()))
        capacity = "{:0.0f}".format(float(x750.getCapacity()))
        current = 0
    elif(config["INA819"]["enable"] == True):
        ups = INA219.INA219(addr=0x42)
        ups_data = ups.getData()
        voltage = "{:10.2f}".format(float(ups_data["voltage"]))
        capacity = "{:0.0f}".format(float(ups_data["percent"]))
        current = "{:10.2f}".format(float(ups_data["current"]))
    else:
        voltage = 0
        capacity = 0
        current = 0

    data = {
        "voltage": voltage,
        "capacity": capacity,
        "current": current
    }
    client.publish("stopwatch/ups", json.dumps(data), retain=True)

def checkCam():
    if (stopwatch.running == False and cam.cameraEnabled() == False):
        cam.check()

schedule.every(5).seconds.do(post_UPS)
schedule.every(10).seconds.do(checkCam)

if __name__ == '__main__':
    schedule.run_all()
    while(1):
        schedule.run_pending()
        time.sleep(.01)
        input = stopwatch.get_input()
        if(old_input != input):
            old_input = input
            print(input)
            if(input["Button_R"] == True):
                if(stopwatch.armed):
                    arm(False)
                else:
                    arm(True)

            client.publish("stopwatch/button", json.dumps(input),retain=True)
            if ((input["Button_1"] == True) or (input["Button_2"] == True) or (input["Button_3"] == True)) and (stopwatch.armed == True or stopwatch.running == True):
                if(stopwatch.running == False):
                    stopwatch.start()
                    client.publish("stopwatch/start_time", str(stopwatch.start_time),retain=True)
                    client.publish("stopwatch/time_1", "0.0", retain=True)
                    client.publish("stopwatch/time_2", "0.0", retain=True)
                    client.publish("stopwatch/time_3", "0.0", retain=True)
                    time.sleep(0.5)
                else:
                    if(input["Button_1"] == True):
                        stopwatch.lane_1.stop()
                        doIfFirst()
                        client.publish("stopwatch/time_1", str(stopwatch.lane_1.get_duration().total_seconds()), retain=True)
                    if(input["Button_2"] == True):
                        stopwatch.lane_2.stop()
                        doIfFirst()
                        client.publish("stopwatch/time_2", str(stopwatch.lane_2.get_duration().total_seconds()), retain=True)
                    if(input["Button_3"] == True):
                        stopwatch.lane_3.stop()
                        doIfFirst()
                        client.publish("stopwatch/time_3", str(stopwatch.lane_3.get_duration().total_seconds()), retain=True)

                    if(stopwatch.check_Finish() == True):
                        arm(False)
                        first = True #Reset first to True for the next Finisher
                        time.sleep(0.5)
                client.publish("stopwatch/running", str(stopwatch.running),retain=True)
        if(stopwatch.running):
            if cam.cameraEnabled():
                cam.idle()
            client.publish("stopwatch/runtime", stopwatch.get_runtime().total_seconds(),retain=True)