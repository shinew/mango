from copy import deepcopy
from unittest import TestCase
from kiwi import Validator
from tests.helpers import Logger, Request, HEART_JSON, SCORE_JSON

class Test_Validator(TestCase):
    def setUp(self):
        self.logger = Logger()
        self.heartJSON = HEART_JSON
        self.scoreJSON = SCORE_JSON
        self.validator = Validator(self.logger)

    """ Unit tests for heart() """
    def test_heart_validJSON(self):
        self.assertTrue(self.validator.heart(Request(self.heartJSON)))

    def test_heart_noJSON(self):
        self.assertFalse(self.validator.heart(Request()))
        self.assertEqual(self.logger.log, "Request did not send JSON")

    def test_heart_missingKey(self):
        for key in HEART_JSON["Samples"][0]:
            self.heartJSON = {"Samples": [0]}
            self.heartJSON["Samples"][0] = deepcopy(HEART_JSON["Samples"][0])
            del self.heartJSON["Samples"][0][key]
            self.assertFalse(self.validator.heart(Request(self.heartJSON)))
            self.assertEqual(self.logger.log, "Key %s not in JSON" % key)

    def test_heart_wrongType(self):
        self.heartJSON["Samples"][0]["ID"] = "not integer"
        self.assertFalse(self.validator.heart(Request(self.heartJSON)))
        self.assertEqual(self.logger.log, "Key %s is not of type %s" % ("ID", int))

    def test_heart_wrongTimeFormat(self):
        wrongTime = u"Nov 21 2013 11:22:31"
        self.heartJSON["Samples"][0]["Time"] = wrongTime
        self.assertFalse(self.validator.heart(Request(self.heartJSON)))
        self.assertEqual(self.logger.log, "Time %s is formatted incorrectly" % wrongTime)

    """ Unit tests for score() """
    def test_score_validISON(self):
        self.assertTrue(self.validator.score(Request(self.scoreJSON)))

    def test_score_noJSON(self):
        self.assertFalse(self.validator.score(Request()))
        self.assertEqual(self.logger.log, "Request did not send JSON")

    def test_score_missingKey(self):
        for key in SCORE_JSON:
            self.scoreJSON = SCORE_JSON.copy()
            del self.scoreJSON[key]
            self.assertFalse(self.validator.score(Request(self.scoreJSON)))
            self.assertEqual(self.logger.log, "Key %s not in JSON" % key)

    def test_score_wrongTimeFormat(self):
        self.scoreJSON["StartTime"] = "Nov 2013 11:42"
        self.assertFalse(self.validator.score(Request(self.scoreJSON)))

    def test_score_startTimeAfterEndTime(self):
        self.scoreJSON["EndTime"], self.scoreJSON["StartTime"] = self.scoreJSON["StartTime"], self.scoreJSON["EndTime"]
        self.assertFalse(self.validator.score(Request(self.scoreJSON)))

if __name__ == '__main__':
    unittest.main()
