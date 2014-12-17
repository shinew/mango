import os.path
from unittest import TestCase
from machine import Scorer
from tests.helpers import Logger

class Test_Scorer(TestCase):
    PATH_TO_HRV_FILE = os.path.join("res", "input.txt")

    def setUp(self):
        self.logger = Logger()
        self.scorer = Scorer(self.logger, None, None)

    def test_passToExe_goodIntervals(self):
        with open(os.path.join(os.path.split(__file__)[0], Test_Scorer.PATH_TO_HRV_FILE)) as f:
            input = f.readlines()[1:] # remove the total at the beginning
        intervals = map(int, input)
        stdout = self.scorer.passToProgram(intervals)
        print stdout
        stdout = map(lambda x: float(x.split()[2]), stdout.splitlines())

        expected = [0.690, 0.091, 0.028, 0.085, 0.009, 0.001, 0.000, 4.261]
        for i in range(len(expected)):
            self.assertAlmostEqual(expected[i], stdout[i], places=3)
