from collections import Counter
from datetime import datetime, timedelta
from sqlalchemy import desc
from database import IntervalScore, User
from validator import Validator


class Measurer:
    """ Returns various server metrics """

    def __init__(self, logger):
        self.logger = logger


    def metrics(self, session):
        """
        Returns various server metrics in JSON format. Metrics include:
        - Last 5 IntervalScores in the last hour
        - # of IntervalScore requests by users in the last hour
        """
        result = {}
        intervalScores = session.query(IntervalScore).order_by(desc(IntervalScore.id)).limit(100)
        allUsers = session.query(User).all()

        userCounts = self.countUsers(intervalScores, allUsers)
        last10 = self.last10Intervals(intervalScores)
        result["User Counts"] = userCounts
        result["Last Scores"] = last10

        return result


    def countUsers(self, intervalScores, allUsers):
        """
        Returns an array of user counts as:
        [{
                "UserID": 1,
                "Count": 4,
        }]
        """
        userNames = {}
        for user in allUsers:
            userNames[user.id] = user.userName

        counter = Counter()
        for intervalScore in intervalScores:
            counter[intervalScore.userID] += 1

        result = []
        for userID in counter:
            result.append({
                "UserID": userID,
                "Count": counter[userID],
                "UserName": userNames[userID]
            })

        return result


    def last10Intervals(self, intervalScores):
        """
        Returns the last 10 interval scores as an array of dicts. Assumes desc ordering.
        """
        result = []
        for interval in intervalScores[:10]:
            result.append({
                "ID": interval.id,
                "UserID": interval.userID,
                "Score": interval.score,
                "StartTime": datetime.strftime(interval.startTime, Validator.DATE_FORMAT),
                "EndTime": datetime.strftime(interval.endTime, Validator.DATE_FORMAT)
            })
        return result

