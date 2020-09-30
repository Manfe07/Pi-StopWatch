import commands
import json, random, datetime

from flask_mqtt import Mqtt
from flask import Flask, render_template, request

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
    "time_1": "000.00",
    "armed": False,
    "running": False,
    "button_1": False,
    "button_2": False,
    "button_3": False,
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
            stuff["running"] = True
        else:
            stuff["running"] = False
    elif(data["topic"] == "stopwatch/runtime"):
        stuff["runtime"] = "{:10.2f}".format(float(data['payload']))
        print(data['payload'])
    elif(data["topic"] == "stopwatch/start_time"):
        stuff["start_time"] = data["payload"]
    elif(data["topic"] == "stopwatch/time_1"):
        stuff["time_1"] = "{:10.2f}".format(float(data['payload']))
    elif(data["topic"] == "stopwatch/button"):
        buttons = json.loads(data['payload'])
        stuff["button_1"] = bool(buttons["Button_1"])
        stuff["button_2"] = bool(buttons["Button_2"])
        stuff["button_3"] = bool(buttons["Button_3"])
    elif(data["topic"] == "stopwatch/armed"):
        if(data["payload"] == "true"):
            stuff["armed"] = True
        else:
            stuff["armed"] = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webInput/<data1>")
def webInput(data1):
    if (data1 == "arm"):
        mqtt.publish("stopwatch/webInput/armed", "true")
        stuff["armed"] = True
        return "armed"
    elif (data1 == "disarm"):
        mqtt.publish("stopwatch/webInput/armed", "false")
        stuff["armed"] = False
        return "disarmed"
    return "error"

@app.route("/data")
def data():
    global stuff
    return json.dumps(stuff)

@app.route("/get_ip")
def get_ip():
    ip = commands.getoutput('hostname -I')
    data = {"ip": str(ip)}
    return json.dumps(data)

if __name__ == '__main__':
    app.run(port=1337,debug=True)
