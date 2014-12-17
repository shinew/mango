from sqlalchemy import func
from datetime import datetime, timedelta
from database import User, Resource, IntervalScore, TrainingInterval
from authenticator import Authenticator
from validator import Validator


def getHRVIntervals(session, userID, startTime, endTime):
        queryResource = session.query(Resource).filter(Resource.userID == userID, Resource.time >= startTime, Resource.time <= endTime, Resource.type == "hrv").all()
        queryResource.sort(key=lambda x: x.time)
        intervals = []
        for resource in queryResource:
            intervals.append(resource.hrv) 
        return intervals

class Processor:
    """ Sends the JSON data to Database, or outputs JSON data. """

    def __init__(self, logger, scorer, authenticator):
        self.logger = logger
        self.scorer = scorer
        self.authenticator = authenticator

    def addSensorData(self, userID, json, session):
        """
        Processes HR and HRV data from users.
        @param json: the JSON from the request
        @return: None
        """

        for sample in json["resources"]:
            time = datetime.strptime(sample["time"], Validator.DATE_FORMAT)

            if sample["sensorType"] == u"heartRate":
                session.add(Resource(logTime=datetime.now(), userID=json["ID"], time=time, type="heartRate", value=sample["value"]))
            else:
                for value in sample["value"]:
                    session.add(Resource(logTime=datetime.now(), userID=json["ID"], time=time, type="hrv", value=value))
        session.commit()


    def getScore(self, userID, json, session):
        """
        Calculates the stress score for that user over the interval.
        @param json: the JSON from the request
        @return: an int representing the stress score, or None if a stress score could not be calculated over that interval
        """

        endTime = datetime.strptime(json["time"], Validator.DATE_FORMAT)
        startTime = endTime - timedelta(minutes=5)

        self.logger.info("Score query: {Start: %s, End: %s}", startTime, endTime)
 
        # checking the cache
        queryIntervalScore = session.query(IntervalScore).filter(IntervalScore.userID == userID, IntervalScore.startTime == startTime, IntervalScore.endTime == endTime).first()
        if queryIntervalScore is not None:
            return queryIntervalScore.score

        # otherwise do machine learning
        intervals = getHRVIntervals(session, id, startTime, endTime) 
        output = self.scorer.score(userID, intervals, session)
        if output is None:
            if json["format"] == u"state":
                return {"state": None}
            else:
                return {"score": None}

        score = int(round(output))
        session.add(IntervalScore(logTime=datetime.now(), userID=userID, startTime=startTime, endTime=endTime, score=score))
        session.commit()

        if json["format"] == u"state":
            if score <= 70:
                state = "calm"
            elif score <= 90:
                state = "tense"
            else:
                state = "stressed"
            return {"state": state}
        else:
            return {"score": score}

