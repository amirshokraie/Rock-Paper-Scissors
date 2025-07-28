import random
from abc import ABC, abstractmethod


_ROCK = 'R'
_PAPER = 'P'
_SCISSORS = 'S'

class BaseMove:
    """
    Abstract base class for Rock, Paper and Scissors classes.
    """

    _dominance = {
        _ROCK: [_SCISSORS],     # Rock beats Scissors
        _SCISSORS: [_PAPER],    # Scissors beats Paper
        _PAPER: [_ROCK],        # Paper beats Rock
    }
    _value = None


    def __init__(self):
        if self._value is None:
            raise NotImplementedError("Subclasses must define '_value'.")
        elif not isinstance(self._value, str):
            raise TypeError(f"_value must be a string, got {type(self._value).__name__}")
        elif self._value.upper() not in self._dominance:
            raise ValueError(f"Invalid move: {self._value!r}. Must be one of: {_ROCK}, {_PAPER}, {_SCISSORS}")

    def __eq__(self, other):
        if not isinstance(other, BaseMove):
            raise TypeError("Can only compare with another BaseMove")
        
        return self._value.upper() == other._value.upper()
    
    def __gt__(self, other):
        if not isinstance(other, BaseMove):
            raise TypeError("Can only compare with another BaseMove")
        
        me = self._value.upper()
        them = other._value.upper()
        return them in self._dominance.get(me, [])
    
    def __lt__(self, other):
        return (not self == other) and (not self > other)


class Rock(BaseMove):
    _value = _ROCK


class Paper(BaseMove):
    _value = _PAPER


class Scissors(BaseMove):
    _value = _SCISSORS


class BasePlayer(ABC):
    def __init__(self, name=None):
        self._name = name if isinstance(name, str) else str(id(self))
        self._score = 0

    def win(self):
        self._score += 1
    
    @property
    def name(self):
        return self._name.title()
    
    @property
    def score(self):
        return self._score

    def __str__(self):
        return f"{self._score} point{'s' if self._score != 1 else ''}."
    
    def _resolve_move(self, move: str | BaseMove):
        if isinstance(move, BaseMove):
            return move
        elif not isinstance(move, str):
            type_name = (
                move.__name__
                if isclass(move)
                else type(move).__name__
            )
            raise TypeError(
                f"'choice' must be of type 'str' or 'BaseMove', \
                but got type '{type_name}' instead."
                )

        if move.upper() == _ROCK:
            return Rock()
        elif move.upper() == _PAPER:
            return Paper()
        elif move.upper() == _SCISSORS:
            return Scissors()
        else:
            raise ValueError(f"Invalid move: {move}")

    @abstractmethod
    def make_move(self, move=None):
        """Return a move object, e.g., Rock(), Paper(), or Scissors()"""
        pass

class Player(BasePlayer):
    
    def make_move(self, move):
        return self._resolve_move(move)


class ComputerPlayer(BasePlayer):
    def __init__(self, name=None):
        super().__init__(name)
        self._name = "Computer " + self._name

    def make_move(self, move=None):
        move = move or random.choice([_ROCK, _PAPER, _SCISSORS])
        return self._resolve_move(move)


class RPSGame:

    def __init__(self, player1 = None, player2 = None):
        player1 = player1 if isinstance(player1, BasePlayer) else ComputerPlayer()
        player2 = player2 if isinstance(player2, BasePlayer) else ComputerPlayer()

    
    def play_one_hand(self, player1_move=None, player2_move=None):
        pass

    