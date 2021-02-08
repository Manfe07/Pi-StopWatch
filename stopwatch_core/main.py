import time, json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import stopwatch

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("stopwatch/webInput/#")
#    subscribe.callback(on_message_print, "stopwatch/webInput/#", hostname="localhost")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "stopwatch/webInput/armed"):
        if(msg.payload == "true"):
            arm(True)
        else:
            arm(False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

stopwatch = stopwatch.Stopwatch()

old_input = stopwatch.get_input()

def arm(_state):
    if _state == True:
        stopwatch.armed = True
        stopwatch.led_Red.set_state(True)
        client.publish("stopwatch/armed", "true", retain=True)
    else:
        stopwatch.armed = False
        stopwatch.led_Red.set_state(False)
        client.publish("stopwatch/armed", "false", retain=True)

while(1):
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
                    client.publish("stopwatch/time_1", str(stopwatch.lane_1.get_duration().total_seconds()), retain=True)
                if(input["Button_2"] == True):
                    stopwatch.lane_2.stop()
                    client.publish("stopwatch/time_2", str(stopwatch.lane_2.get_duration().total_seconds()), retain=True)
                if(input["Button_3"] == True):
                    stopwatch.lane_3.stop()
                    client.publish("stopwatch/time_3", str(stopwatch.lane_3.get_duration().total_seconds()), retain=True)

                if(stopwatch.check_Finish() == True):
                    arm(False)
                    time.sleep(0.5)
            client.publish("stopwatch/running", str(stopwatch.running),retain=True)
    if(stopwatch.running):
        client.publish("stopwatch/runtime", stopwatch.get_runtime().total_seconds(),retain=True)