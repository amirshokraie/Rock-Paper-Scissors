import random
from abc import ABC, abstractmethod
from enum import Enum
from inspect import isclass


def _get_class_name(obj):
    """
    Return the class name of the given instance or class.

    Args:
        obj: An instance or a class object.

    Returns:
        str: The name of the class if obj is an instance, or
             the name of the class itself if obj is a class.
    """
    return obj.__name__ if isclass(obj) else type(obj).__name__


class Move(Enum):
    ROCK = "R"
    PAPER = "P"
    SCISSORS = "S"

    @classmethod
    def get_move(cls, raw_move: str):
        """Sanitize and validate raw_move (e.g., 'R', 'P', 'S') and return corresponding Move enum."""
        if not isinstance(raw_move, str):
            raise TypeError(
                f"Expected a string for raw_move, but got {_get_class_name(raw_move)} instead."
            )

        sanitized = raw_move.strip().upper()
        for move in cls:
            if move.value == sanitized:
                return move
        raise ValueError(
            f"Invalid move '{raw_move}'. Choose from: {[m.value for m in cls]}"
        )

    def __str__(self):
        return self.name.capitalize()


class BaseMove:
    """
    Abstract base class for Rock, Paper, and Scissors classes.
    """

    _dominance = {
        Move.ROCK: [Move.SCISSORS],
        Move.SCISSORS: [Move.PAPER],
        Move.PAPER: [Move.ROCK],
    }
    _move = None

    def __init__(self):
        if self._move is None:
            raise NotImplementedError("Subclasses must define '_move'.")
        if not isinstance(self._move, Move):
            raise TypeError(
                f"_move must be of type Move, not {_get_class_name(self._move)}"
            )

    def __eq__(self, other):
        if not isinstance(other, BaseMove):
            raise TypeError
        return self._move == other._move

    def __gt__(self, other):
        if not isinstance(other, BaseMove):
            raise TypeError
        return other._move in self._dominance[self._move]

    def __lt__(self, other):
        return not (self > other or self == other)

    def __str__(self):
        return self._move.name.capitalize()

    def __hash__(self):
        return hash(self._move)


class Rock(BaseMove):
    _move = Move.ROCK


class Paper(BaseMove):
    _move = Move.PAPER


class Scissors(BaseMove):
    _move = Move.SCISSORS


class BasePlayer(ABC):
    def __init__(self, name=None):
        self._name = name if isinstance(name, str) else str(id(self))
        self._score = 0
        self.last_move = None

    def win(self):
        self._score += 1

    def reset_score(self):
        self._score = 0

    @property
    def name(self):
        return self._name.title()

    @property
    def score(self):
        return self._score

    def __str__(self):
        return f"{self.name} has {self._score} point{'s' if self._score != 1 else ''}."

    @staticmethod
    def _resolve_move(move: str | BaseMove | Move):
        if isinstance(move, BaseMove):
            return move
        if isinstance(move, Move):
            match move:
                case Move.ROCK:
                    return Rock()
                case Move.PAPER:
                    return Paper()
                case Move.SCISSORS:
                    return Scissors()
        if isinstance(move, str):
            move_enum = Move.get_move(move)
            return BasePlayer._resolve_move(move_enum)

        raise TypeError(f"Invalid move type: {_get_class_name(move)}")

    @abstractmethod
    def make_move(self, move=None):
        """Return a move object, e.g., Rock(), Paper(), or Scissors()"""
        pass


class Player(BasePlayer):

    def make_move(self, move):
        move_instance = self._resolve_move(move)
        self.last_move = move_instance
        return move_instance


class ComputerPlayer(BasePlayer):
    def __init__(self, name=None):
        super().__init__(name)
        if not name or not name.lower().startswith("computer"):
            self._name = f"Computer {self._name}"

    def make_move(self, move=None):
        if move is None:
            move = random.choice(list(Move))  # choose a Move enum, not a string
        move_instance = self._resolve_move(move)
        self.last_move = move_instance
        return move_instance


class RPSGame:

    def __init__(self, player1=None, player2=None, winner_score: int = 3):
        self.player1 = player1 if isinstance(player1, BasePlayer) else ComputerPlayer()
        self.player2 = player2 if isinstance(player2, BasePlayer) else ComputerPlayer()

        self.winner_score = winner_score

    def play_one_hand(self, player1_move=None, player2_move=None):
        move1 = self.player1.make_move(player1_move)
        move2 = self.player2.make_move(player2_move)

        # Determine result
        if move1 > move2:
            self.player1.win()
        elif move2 > move1:
            self.player2.win()

    def get_winner(self):
        if self.player1.score >= self.winner_score:
            return self.player1
        elif self.player2.score >= self.winner_score:
            return self.player2
        return None

    def reset_scores(self):
        self.player1.reset_score()
        self.player2.reset_score()


if __name__ == "__main__":
    player_name = input("Your name: ")
    game = RPSGame(Player(player_name), ComputerPlayer(), winner_score=2)

    play_again = True
    while play_again:
        try:
            user_input = input(
                f"Enter your move ({', '.join(m.value for m in Move)}): "
            )
            player_move = Move.get_move(user_input)
        except ValueError as e:
            print(e)
            continue

        game.play_one_hand(player_move)

        print(
            f"{game.player1.name}: {game.player1.last_move}\t{game.player2.name}: {game.player2.last_move}"
        )
        print(
            f"{game.player1.name}: {game.player1.score},\t{game.player2.name}: {game.player2.score}"
        )

        winner = game.get_winner()
        if winner:
            print(f"{winner.name} wins the game with {winner.score} points!")
            response = input("Do you want to play again? (Y/N): ").strip().upper()
            play_again = response == "Y"
            if play_again:
                game.reset_scores()
