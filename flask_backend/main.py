import os
#import commands
import json

from flask_mqtt import Mqtt
from flask import Flask, render_template, send_file

with open("../config.json") as json_data_file:
    config = json.load(json_data_file)

if (config["x750"]["enable"] == True):
    from flask_backend.modules import x750ups as x750

elif (config["INA819"]["enable"] == True):
    from flask_backend.modules.INA219 import INA219
    ups = INA219(addr=0x42)

mqttHost = config["mqtt"]["host"]
mqttPort = config["mqtt"]["port"]

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = mqttHost
#app.config['MQTT_BROKER_URL'] = '192.168.11.213'
app.config['MQTT_BROKER_PORT'] = mqttPort
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.1
mqtt = Mqtt(app)
mqtt.init_app(app)

ip = "123.123.123.123"

stuff = {
    "start_time": "",
    "runtime": "000.00",
    "time_1": "000.00",
    "time_2": "000.00",
    "time_3": "000.00",
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
    elif(data["topic"] == "stopwatch/time_2"):
        stuff["time_2"] = "{:10.2f}".format(float(data['payload']))
    elif(data["topic"] == "stopwatch/time_3"):
        stuff["time_3"] = "{:10.2f}".format(float(data['payload']))
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

@app.route("/settings")
def settings():
    return render_template("settings.html")

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

@app.route("/get_image")
def get_image():
    file = "../stopwatch_core/test.jpg"
    return send_file(file, mimetype='image/gif')


@app.route("/ups")
def ups():
    if(config["x750"]["enable"] == True):
        voltage = "{:10.2f}".format(float(x750.getVolage()))
        capacity = "{:0.0f}".format(float(x750.getCapacity()))
        current = 0
    elif(config["INA819"]["enable"] == True):
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
    return json.dumps(data)


@app.route("/get_ip")
def get_ip():
    stream = os.popen('hostname -I')
    ip = stream.read()

    #ip = commands.getoutput('hostname -I')
    data = {"ip": str(ip)}
    return json.dumps(data)

if __name__ == '__main__':
    app.run(port=1337,debug=True)
