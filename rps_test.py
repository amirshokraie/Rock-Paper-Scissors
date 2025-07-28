import unittest
from rps import Rock,Paper,Scissors, BaseMove


class TestRPSComparison(unittest.TestCase):

    def setUp(self):
        self.rock = Rock()
        self.paper = Paper()
        self.scissors = Scissors()


if __name__ == "__main__":
    unittest.main()