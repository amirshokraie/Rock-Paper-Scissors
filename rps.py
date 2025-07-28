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


class AbstractPlayer(ABC):
    def __init__(self, name=None):
        self.name = name if isinstance(name, str) else str(id(self))
        self.score = 0

    def win(self):
        self.score += 1

    @abstractmethod
    def make_move(self):
        """Return a move, e.g., 'R', 'P', or 'S'"""
        pass

class Player(AbstractPlayer):

    def __init__(self, name=None):
        self.name = name if isinstance(name, str) else str(id(self))
        self.score = 0


class ComputerPlayer(AbstractPlayer):
    def __init__(self, name=None):
        super().__init__(name)
        self.name = "Computer " + self.name

    def make_move(self):
        return random.choice([_ROCK, _PAPER, _SCISSORS])


