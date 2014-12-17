class Request:
    def __init__(self, json=None):
        self.json = json

class Logger:
    def __init__(self):
        self.log = ""

    def warning(self, *args):
        self.log = args[0] % args[1:]

    def info(self, *args):
        pass

HEART_JSON = {
    "Samples": [{
    "ID": 1,
    "Device": u"Wahoo TICKR",
    "Time": u"2014-03-31 19:13:44",
    "Movement": False,
    "HR": 69,
    "HRV": [696]
}]}

SCORE_JSON = {
    "ID": 1,
    "StartTime": u"2014-03-31 19:13:44",
    "EndTime": u"2014-03-31 19:20:00"
}