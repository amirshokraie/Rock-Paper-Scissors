import unittest
import rps as _rps


class TestRPSComparison(unittest.TestCase):

    def setUp(self):
        self.rock = _rps.Rock()
        self.paper = _rps.Paper()
        self.scissors = _rps.Scissors()

    def test_initialization_errors(self):
        # Case 1: _move is not set (None) → NotImplementedError
        class NoneValue(_rps.BaseMove):
            pass

        with self.assertRaises(NotImplementedError):
            NoneValue()

        # Case 2: _move is not a Move enum  → TypeError
        class NotEnumValue(_rps.BaseMove):
            _move = 1234

        with self.assertRaises(TypeError):
            NotEnumValue()

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
        self.assertLess(self.rock, self.paper)

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

    def base_player_initialization_error(self):
        with self.assertRaises(
            TypeError, msg="BasePlayer should not be instantiable directly"
        ):
            # trying to instantiate BasePlayer directly must raise a TypeError
            # Becuase BasePlayer inherites from ABC class
            _rps.BasePlayer()

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

    def test_player_name(self):
        # name attr should return .title()
        test_name = "pyTHON COder"

        player1 = _rps.Player()
        player2 = _rps.Player(test_name)
        self.assertEqual(player1.name, str(id(player1)))
        self.assertEqual(player2.name, test_name.title())

    def test_move_resolution_from_str(self):
        # checking both player and computer player's make_move resolution from string
        for player in [_rps.Player(), _rps.ComputerPlayer()]:
            self.assertIsInstance(player.make_move("r"), _rps.Rock)
            self.assertIsInstance(player.make_move("P"), _rps.Paper)
            self.assertIsInstance(player.make_move("s"), _rps.Scissors)

    def test_move_resolution_from_instance(self):
        # checking both player and computer player's make_move resolution from instances
        for player in [_rps.Player(), _rps.ComputerPlayer()]:
            self.assertIsInstance(player.make_move(_rps.Rock()), _rps.Rock)
            self.assertIsInstance(player.make_move(_rps.Paper()), _rps.Paper)
            self.assertIsInstance(player.make_move(_rps.Scissors()), _rps.Scissors)

    def test_invalid_move(self):
        # checking both player and computer player's make_move raising errors
        for player in [_rps.Player(), _rps.ComputerPlayer()]:
            with self.assertRaises(ValueError):
                player.make_move("X")
            with self.assertRaises(TypeError):
                player.make_move(123)

    def test_computer_random_move(self):
        computer = _rps.ComputerPlayer()
        moves = set()

        for _ in range(100):  # Used 100 iterations to reduce randomness bias
            move = computer.make_move()
            self.assertIsInstance(move, _rps.BaseMove)
            moves.add(move)

        # Confirm that all 3 move types were used
        self.assertEqual(moves, {_rps.Rock(), _rps.Paper(), _rps.Scissors()})


class TestRPSGame(unittest.TestCase):

    def test_default_initialization(self):
        game = _rps.RPSGame()
        self.assertIsInstance(game.player1, _rps.ComputerPlayer)
        self.assertIsInstance(game.player2, _rps.ComputerPlayer)
        self.assertEqual(game.winner_score, 3)

    def test_custom_players(self):
        p1 = _rps.Player("Python")
        p2 = _rps.Player("tester")
        game = _rps.RPSGame(p1, p2, winner_score=5)

        self.assertEqual(game.player1.name, "Python")
        self.assertEqual(game.player2.name, "Tester")
        self.assertEqual(game.winner_score, 5)

    def test_draw_does_not_affect_score(self):
        p1 = _rps.Player("DrawTester1")
        p2 = _rps.Player("DrawTester2")
        game = _rps.RPSGame(p1, p2, winner_score=1)

        game.play_one_hand(_rps.Move.ROCK, _rps.Move.ROCK)
        game.play_one_hand(_rps.Move.PAPER, _rps.Move.PAPER)
        game.play_one_hand(_rps.Move.SCISSORS, _rps.Move.SCISSORS)

        self.assertEqual(p1.score, 0)
        self.assertEqual(p2.score, 0)
        self.assertIsNone(game.get_winner())

    def test_get_winner_with_second_player_winning(self):
        p1 = _rps.Player("Player1")
        p2 = _rps.Player("Player2")
        game = _rps.RPSGame(p1, p2, winner_score=2)

        game.play_one_hand(_rps.Move.SCISSORS, _rps.Move.ROCK)  # Player2 wins
        game.play_one_hand(_rps.Move.PAPER, _rps.Move.SCISSORS)  # Player2 wins
        self.assertEqual(game.get_winner(), p2)


if __name__ == "__main__":
    unittest.main()
