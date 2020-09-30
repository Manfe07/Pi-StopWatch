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
            stopwatch.armed = True
            client.publish("stopwatch/armed", "true")
        else:
            stopwatch.armed = False
            client.publish("stopwatch/armed", "false")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

stopwatch = stopwatch.Stopwatch()

old_input = stopwatch.get_input()
while(1):
    time.sleep(.01)
    input = stopwatch.get_input()
    if(old_input != input):
        old_input = input
        client.publish("stopwatch/button", json.dumps(input),retain=True)
        if(input["Button_1"] == True and stopwatch.armed == True):
            if(stopwatch.running == False):
                stopwatch.start()
                client.publish("stopwatch/start_time", str(stopwatch.start_time),retain=True)
                time.sleep(0.5)
            else:
                stopwatch.stop()
                client.publish("stopwatch/time_1", stopwatch.get_duration().total_seconds(),retain=True)
                client.publish("stopwatch/armed", "false",retain=True)
                stopwatch.armed = False
                time.sleep(0.5)
            client.publish("stopwatch/running", str(stopwatch.running),retain=True)
    if(stopwatch.running):
        client.publish("stopwatch/runtime", stopwatch.get_runtime().total_seconds(),retain=True)