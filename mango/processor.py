from sqlalchemy import func
from datetime import datetime, timedelta
from database import User, HeartRate, IntervalScore, TrainingInterval
from authenticator import Authenticator
from validator import Validator


def getHeartrateIntervals(session, userID, startTime, endTime):
        queryHeartRate = session.query(HeartRate).filter(HeartRate.userID == userID, HeartRate.time >= startTime, HeartRate.time <= endTime).all()
        queryHeartRate.sort(key=lambda x: x.time)
        heartRates = []
        intervals = []
        for heartRate in queryHeartRate:
            heartRates.append(heartRate.hr)
            if heartRate.hrv is not None:
                intervals.append(heartRate.hrv) 
        return heartRates, intervals

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

        for sample in json["Samples"]:
            time = datetime.strptime(sample["Time"], Validator.DATE_FORMAT)

            if sample["HRV"] is not None:
                for hrv in sample["HRV"]:
                    session.add(HeartRate(logTime=datetime.now(), userID=json["ID"], device=sample["Device"], time=time, hasMovement=sample["Movement"], hr=sample["HR"], hrv=hrv))
            else:
                session.add(HeartRate(logTime=datetime.now(), userID=json["ID"], device=sample["Device"], time=time, hasMovement=sample["Movement"], hr=sample["HR"], hrv=None))
        session.commit()


    def getScore(self, userID, json, session):
        """
        Calculates the stress score for that user over the interval.
        @param json: the JSON from the request
        @return: an int representing the stress score, or None if a stress score could not be calculated over that interval
        """

        endTime = datetime.strptime(json["time"])
        startTime = endTime - timedelta(minutes=5)

        self.logger.info("Score query: {Start: %s, End: %s}", startTime, endTime)
 
        # checking the cache
        queryIntervalScore = session.query(IntervalScore).filter(IntervalScore.userID == userID, IntervalScore.startTime == startTime, IntervalScore.endTime == endTime).first()
        if queryIntervalScore is not None:
            return queryIntervalScore.score

        # otherwise do machine learning
        heartRates, intervals = getHeartrateIntervals(session, id, startTime, endTime) 
        output = self.scorer.score(userID, heartRates, intervals, session)
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

