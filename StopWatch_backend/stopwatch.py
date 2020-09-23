import datetime

class lane:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.stop_time = datetime.datetime.now()

    def start(self):
        self.start_time = datetime.datetime.now()
        return self.start_time

    def stop(self):
        self.stop_time = datetime.datetime.now()
        return self.stop_time

    def get_duration(self):
        duration = self.stop_time - self.start_time
        return duration

    def get_runtime(self):
        runtime = datetime.datetime.now() - self.start_time
        return runtime