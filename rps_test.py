import unittest
import rps as _rps


class TestRPSComparison(unittest.TestCase):

    def setUp(self):
        self.rock = _rps.Rock()
        self.paper = _rps.Paper()
        self.scissors = _rps.Scissors()

    def test_initialization_errors(self):

        # Case 1 : _value is not set (is None) -> NotImplementedError:
        class NoneValue(_rps.BaseMove):
            pass

        with self.assertRaises(NotImplementedError):
            NoneValue()

        # Case 2 : _value is not str -> TypeError
        class NotStringValue(_rps.BaseMove):
            _value = 1234
        
        with self.assertRaises(TypeError):
            NotStringValue()

        # case 3 : _value is a string but invalid -> ValueError
        class InvalidStringValue(_rps.BaseMove):
            _value = "Invalid text for test"

        with self.assertRaises(ValueError):
            InvalidStringValue()

    def test_greater_than(self):
        self.assertGreater(self.rock, self.scissors)
        self.assertGreater(self.scissors, self.paper)
        self.assertGreater(self.paper, self.rock)

        self.assertFalse(self.scissors > self.rock)
        self.assertFalse(self.paper > self.scissors)
        self.assertFalse(self.rock > self.paper)
    
    def test_less_than(self):
        self.assertLess(self.scissors, self.rock)  
        self.assertLess(self.paper, self.scissors)
        self.assertLess(self.rock,  self.paper)

        self.assertFalse(self.rock < self.scissors)
        self.assertFalse(self.scissors < self.paper)
        self.assertFalse(self.paper < self.rock)
    
    def test_equal(self):
        self.assertEqual(self.rock, _rps.Rock())
        self.assertEqual(self.paper, _rps.Paper())
        self.assertEqual(self.scissors, _rps.Scissors())

    def test_not_equal(self):
        self.assertNotEqual(self.rock, self.paper)
        self.assertNotEqual(self.paper, self.scissors)
        self.assertNotEqual(self.scissors, self.rock)


class TestPlayers(unittest.TestCase):
    def test_score(self):
        # checking both player and computer player score changing
        for player in [_rps.Player(), _rps.ComputerPlayer()]:
            self.assertEqual(player.score, 0)
            player.win() 
            self.assertEqual(player.score, 1)
            player.win() 
            self.assertEqual(player.score, 2) 
    

    def test_computer_player_name(self):
        computer1 = _rps.ComputerPlayer()
        computer2 = _rps.ComputerPlayer("smart pc")
        self.assertTrue(computer1.name.startswith("Computer"))
        self.assertTrue(computer2.name.startswith("Computer"))

if __name__ == "__main__":
    unittest.main()