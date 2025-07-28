import unittest
from rps import Rock,Paper,Scissors, BaseMove


class TestRPSComparison(unittest.TestCase):

    def setUp(self):
        self.rock = Rock()
        self.paper = Paper()
        self.scissors = Scissors()

    def test_initialization_errors(self):

        # Case 1 : _value is not set (is None) -> NotImplementedError:
        class NoneValue(BaseMove):
            pass

        with self.assertRaises(NotImplementedError):
            NoneValue()

        # Case 2 : _value is not str -> TypeError
        class NotStringValue(BaseMove):
            _value = 1234
        
        with self.assertRaises(TypeError):
            NotStringValue()

        # case 3 : _value is a string but invalid -> ValueError
        class InvalidStringValue(BaseMove):
            _value = "Invalid text for test"

        with self.assertRaises(ValueError):
            InvalidStringValue()
    
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