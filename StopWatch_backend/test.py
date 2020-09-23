from flask import Flask
from stopwatch import Stopwatch
import datetime, commands, test_stuf
app = Flask(__name__)

stopwatch = Stopwatch()

@app.route("/ip")
def index():
    return "IP: " + str(commands.getoutput('hostname -I'))

@app.route("/start")
def start():
    time = stopwatch.start()
    return "StartTime: " + str(time)

@app.route("/stop")
def stop():
    stopwatch.stop()
    return "<br>StartTime: " + str(stopwatch.start_time) + "<br>StopTime: " + str(stopwatch.stop_time) + "<br>Duration: " + str(stopwatch.get_duration())

@app.route("/runtime")
def runtime():
    return test_stuf.refreshcode(1) + str(stopwatch.get_runtime())

@app.route("/")
def input():
    return test_stuf.refreshcode(1) + str(stopwatch.get_input())

@app.route("/refresh")
def refresh():
    text = str(datetime.datetime.now().timestamp())
    return test_stuf.refreshcode(5) + text


if __name__ == '__main__':
    app.run(port=1337,debug=True)