import commands
from flask import Flask, render_template
import paho.mqtt.subscribe as subscribe

app = Flask(__name__)

ip = commands.getoutput('hostname -I')

@app.route("/")
def index():
    start_time = subscribe.simple("stopwatch/start_time", hostname="127.0.0.1")
    runtime = subscribe.simple("stopwatch/runtime", hostname="127.0.0.1")
    duration = subscribe.simple("stopwatch/duration", hostname="127.0.0.1")
    return render_template("index.html", adress=ip, start_time=start_time.payload, runtime=runtime.payload, duration=duration.payload )

if __name__ == '__main__':
    app.run(port=1337,debug=True)