import time, stopwatch
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883, 60)

client.loop_start()

stopwatch = Stopwatch()

while(1):
    time.sleep(.01)
    client.publish("stopwatch/buttons",stopwatch.get_input())
