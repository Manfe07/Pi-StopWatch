#import commands
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
        "time":00,
        "Name":"Manuel"
    }

if __name__ == '__main__':
    app.run(port=1337,debug=True)