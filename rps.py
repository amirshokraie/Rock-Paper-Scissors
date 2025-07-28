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
    