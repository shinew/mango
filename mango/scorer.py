import os.path
import numpy
from subprocess import Popen, PIPE, STDOUT
from sklearn.ensemble import RandomForestClassifier
from database import HeartRate, TrainingInterval
from processor import getHeartrateIntervals


def passToProgram(intervals):
    """ Passes the intervals (given as [int]) to the executable """
    executablePath = os.path.join(os.path.split(__file__)[0], Scorer.HRV_STATS_EXE)
    stdin = " ".join(map(str, [len(intervals)] + intervals))
    process = Popen([executablePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout = process.communicate(input=stdin)[0]
    return stdout

class Scorer:
    """
    Computes a score for given heart rate data
    """

    HRV_STATS_EXE = os.path.join("bin", "heart")
    CURRENT_FEATURE_VERSION = 2

    def __init__(self, logger):
        self.logger = logger

    def score(self, userID, heartrates, intervals, session):
        """
        Input: list of heartrates (int, beats/min) and intervals (int, ms)
        Output: a float representing the score and the feature string, or None if it cannot be calculated
        """

        # minimal interval requirements
        if len(intervals) < 256:
            return None

        featuresList, valuesList, sampleWeights = self.trainCalibrationIntervals(session, userID)

        classifier = RandomForestClassifier(n_estimators=200)
        if len(featuresList) != 0 and len(valuesList) != 0:
            classifier.fit(featuresList, valuesList, sample_weight=numpy.array(sampleWeights))
        session.commit()

        # right now, we're not using heart rate stats (though we could)
        stdout = passToProgram(intervals)
        features = map(lambda x: float(x.split()[2]), stdout.splitlines())
        certainties = classifier.predict_proba([features])[0]
        score = 0.0
        for i, n in enumerate(certainties):
            score += i * n
        return score * 100

    def trainCalibrationIntervals(self, session, userID):
        # new design: train intervals on every request (should be optimized later!)
        trainingIntervals = session.query(TrainingInterval) \
            .filter((TrainingInterval.isDefaultSet == True) | (TrainingInterval.userID == userID)) \
            .all()
        featuresList = []
        valuesList = []
        sampleWeights = []
        for interval in trainingIntervals:
            if interval.featureCache is not None and interval.featureCacheVersion == Scorer.CURRENT_FEATURE_VERSION:
                features = map(lambda x: float(x.split()[2]), interval.featureCache.splitlines()) 
            else:
                heartrate, intervals = getHeartrateIntervals(session, interval.userID, interval.startTime, interval.endTime)
                if len(intervals) < 128:
                    # Warning: this value is deliberately different from 256 as some legacy training intervals have shorter lengths due to truncation)
                    self.logger.warning(
                        "Invalid training interval: ID: %s, StartTime: %s, EndTime: %s",
                        interval.userID,
                        interval.startTime,
                        interval.endTime
                    )
                    session.delete(interval)
                    continue
                else:
                    stdout = passToProgram(intervals)
                    interval.featureCache = stdout
                    interval.featureCacheVersion = Scorer.CURRENT_FEATURE_VERSION
                    features = map(lambda x: float(x.split()[2]), stdout.splitlines()) 

            featuresList.append(features)
            valuesList.append(interval.category)

            # prioritizes the user's weights
            if interval.userID == userID:
                sampleWeights.append(5.0)
            else:
                sampleWeights.append(1.0)

        return featuresList, valuesList, sampleWeights

