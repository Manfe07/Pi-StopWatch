import commands
import json, random

from flask_mqtt import Mqtt
from flask import Flask, render_template

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
#app.config['MQTT_BROKER_URL'] = '192.168.11.213'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.1
mqtt = Mqtt(app)
mqtt.init_app(app)

ip = "131.123.123.123"

stuff = {
    "start_time": "",
    "runtime": "000.00",
    "running": False,
    "Button_1": False,
    "Button_2": False,
    "Button_3": False,
}

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('stopwatch/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global stuff
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    if(data["topic"] == "stopwatch/running"):
        if(data["payload"] == "True"):
            stuff["running"] = True;
        else:
            stuff["running"] = False;
    elif(data["topic"] == "stopwatch/duration"):
        stuff["runtime"] = data["payload"]
    elif(data["topic"] == "stopwatch/start_time"):
        stuff["start_time"] = data["payload"]
        print("startTime")



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    global stuff
    stuff["Button_1"] = bool(random.getrandbits(1))
    stuff["Button_2"] = bool(random.getrandbits(1))
    stuff["Button_3"] = bool(random.getrandbits(1))
    return json.dumps(stuff)

@app.route("/get_ip")
def get_ip():
    ip = commands.getoutput('hostname -I')
    data = {"ip": str(ip)}
    return json.dumps(data)

if __name__ == '__main__':
    app.run(port=1337,debug=True)
