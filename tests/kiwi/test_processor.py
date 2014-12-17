from unittest import TestCase
from mock import Mock
from kiwi import Processor
from tests.helpers import Logger, HEART_JSON

class Test_Processor(TestCase):
    def setUp(self):
        self.logger = Logger()
        self.heartJSON = HEART_JSON
        self.session = Mock()
        self.processor = Processor(self.logger)

    def test_heart_successfulTransaction(self):
        queryResult = Mock()
        queryResult.first = Mock(return_value=(1,))
        self.session.query = Mock(return_value=queryResult)
        self.assertIsNone(self.processor.heart(self.heartJSON, self.session))

    def test_heart_failedTransaction(self):
        queryResult = Mock()
        queryResult.first = Mock(return_value=(1,))
        self.session.query = Mock(return_value=queryResult)
        self.session.commit = Mock(side_effect=StandardError)
        with self.assertRaises(StandardError):
            self.processor.heart(self.heartJSON, self.session)

if __name__ == '__main__':
    unittest.main()
