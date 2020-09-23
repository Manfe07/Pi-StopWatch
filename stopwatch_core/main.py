import time, json
import paho.mqtt.client as mqtt
import stopwatch

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

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
        if(input["Button_1"] == True):
            if(stopwatch.running == False):
                stopwatch.start()
                client.publish("stopwatch/start_time", str(stopwatch.start_time),retain=True)
                time.sleep(0.5)
            else:
                stopwatch.stop()
                client.publish("stopwatch/duration", str(stopwatch.get_duration()),retain=True)
                time.sleep(0.5)
            client.publish("stopwatch/running", str(stopwatch.running),retain=True)
    if(stopwatch.running):
        client.publish("stopwatch/duration", str(stopwatch.get_runtime()),retain=True)