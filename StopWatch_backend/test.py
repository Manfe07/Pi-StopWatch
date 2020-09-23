from flask import Flask
import datetime, commands, stopwatch, test_stuf, input
app = Flask(__name__)

l1 = stopwatch.lane()

@app.route("/")
def index():
    return "IP: " + str(commands.getoutput('hostname -I'))

@app.route("/start")
def start():
    time = l1.start()
    return "StartTime: " + str(time)

@app.route("/stop")
def stop():
    l1.stop()
    return "<br>StartTime: " + str(l1.start_time) + "<br>StopTime: " + str(l1.stop_time) + "<br>Duration: " + str(l1.get_duration())

@app.route("/runtime")
def runtime():
    return test_stuf.refreshcode(1) + str(l1.get_runtime())

@app.route("/input")
def input():
    return test_stuf.refreshcode(1) + input.get_input

@app.route("/refresh")
def refresh():
    text = str(datetime.datetime.now().timestamp())
    return test_stuf.refreshcode(5) + text


if __name__ == '__main__':
    app.run(port=1337,debug=True)