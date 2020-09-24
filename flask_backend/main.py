#import commands
import json, random

from flask import Flask, render_template
#import paho.mqtt.subscribe as subscribe

app = Flask(__name__)

#ip = commands.getoutput('hostname -I')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    stuff = {
        "Button_1": False,
        "Button_2": False,
        "Button_3": False,
        "Name": "Manuel"
    }
    stuff["Button_1"] = bool(random.getrandbits(1))
    stuff["Button_2"] = bool(random.getrandbits(1))
    stuff["Button_3"] = bool(random.getrandbits(1))
    return json.dumps(stuff)

@app.route("/get_ip")
def get_ip():
    data = {"ip": "192.168.0.1"}
    data["ip"] = str(random.randrange(0,255,1)) + "." + str(random.randrange(0,255,1)) + "." + str(random.randrange(0,255,1)) + "." + str(random.randrange(0,255,1))
    return json.dumps(data)
if __name__ == '__main__':
    app.run(port=1337,debug=True)