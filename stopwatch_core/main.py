import time
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
        client.publish("stopwatch/button", input)
        time.sleep(0.5)
        if((input["Button_1"] == True) or (input["Button_2"] == True) or (input["Button_3"] == True)):
            if(stopwatch.running == False):
                stopwatch.start()
            else:
                stopwatch.stop()

    client.publish("stopwatch/duration", stopwatch.get_duration())