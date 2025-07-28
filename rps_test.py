import unittest
from rps import Rock,Paper,Scissors, BaseMove


class TestRPSComparison(unittest.TestCase):

    def setUp(self):
        self.rock = Rock()
        self.paper = Paper()
        self.scissors = Scissors()

    def test_equal(self):
        self.assertEqual(self.rock, Rock())
        self.assertEqual(self.paper, Paper())
        self.assertEqual(self.scissors, Scissors())

    def test_not_equal(self):
        self.assertNotEqual(self.rock, self.paper)
        self.assertNotEqual(self.paper, self.scissors)
        self.assertNotEqual(self.scissors, self.rock)


if __name__ == "__main__":
    unittest.main()