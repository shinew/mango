from datetime import datetime

class Validator:
    """ Validates the JSON inputs. """
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, logger, authenticator):
        self.logger = logger
        self.authenticator = authenticator

    def commonAuthenticate(self, request, session):
        if not request.json:
            self.logger.warning("Request did not send JSON")
            return False
        return True
        """
        if "ID" not in request.json or "Password" not in request.json:
            self.logger.warning("Missing ID or Password")
            return False
        if type(request.json["ID"]) is not int or type(request.json["Password"]) is not unicode:
            self.logger.warning("ID or Password in wrong format(s)")
            return False
        if not self.authenticator.authenticate(request.json["ID"], request.json["Password"], session):
            self.logger.warning("Authentication failed")
            return False
        """

    def addSensorData(self, request, session):
        if not self.commonAuthenticate(request, session):
            return False

        if "resources" not in request.json or type(request.json["resources"]) is not list:
            self.logger.warning('"resources" not in request')
            return False

        for item in request.json["resources"]:
            if "sensorType" not in item or type(item["sensorType"]) is not unicode or \
                "time" not in item or type(item["time"]) is not unicode or \
                "value" not in item:
                self.logger.warning("basic types not in request")
                return False
            if not self.verifyTime(item["time"]):
                self.logger.warning("time is in wrong format")
                return False

            if item["sensorType"] == u"heartRate":
                if type(item["value"]) is not int:
                    self.logger.warning('"hr" is in wrong format')
                    return False
            elif item["sensorType"] == u"hrv":
                if type(item["value"]) is not list:
                    self.logger.warning('"hrv" is in wrong format')
                    return False
                for value in item["value"]:
                    if type(value) is not int:
                        self.logger.warning('"hrv" values are in wrong format')
                        return False
            else:
                self.logger.warning("format does not exist")
                return False

        return True

    def getScore(self, request, session):
        if not self.commonAuthenticate(request, session):
            return False

        if "time" not in request.json or type(request.json["time"]) is not unicode or \
            "format" not in request.json or type(request.json["format"]) is not unicode:
            return False

        if not self.verifyTime(request.json["time"]):
            return False

        if request.json["format"] not in [u"state", u"score"]:
            return False

        return True

    def verifyTime(self, time):
        try:
            datetime.strptime(time, Validator.DATE_FORMAT)
            return True
        except ValueError:
            return False

