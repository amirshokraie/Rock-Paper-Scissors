import random
from abc import ABC, abstractmethod
from inspect import isclass

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

    def __str__(self):
        return self.__class__.__name__
    
    def __hash__(self):
        return hash(self._value.upper())
    

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
        self.last_move = None

    def win(self):
        self._score += 1
    
    @property
    def name(self):
        return self._name.title()
    
    @property
    def score(self):
        return self._score

    def __str__(self):
        return f"{self.name} has {self._score} point{'s' if self._score != 1 else ''}."
    
    @staticmethod
    def _resolve_move(move: str | BaseMove):
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
        move_instance = self._resolve_move(move)
        self.last_move = move_instance
        return move_instance


class ComputerPlayer(BasePlayer):
    def __init__(self, name=None):
        super().__init__(name)
        if not name or not name.lower().startswith("computer"):
            self._name = f"Computer {self._name}"

    def make_move(self, move=None):
        move_instance =  self._resolve_move(move or random.choice([_ROCK, _PAPER, _SCISSORS]))
        self.last_move = move_instance
        return move_instance


class RPSGame:

    def __init__(self, player1 = None, player2 = None, winner_score: int = 3):
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
    

if __name__ == "__main__":
    player_name = input("Your name: ")
    game = RPSGame(Player(player_name), ComputerPlayer(), winner_score=2)

    while not game.get_winner():
        player_input = input(f"Enter your move ({_ROCK}, {_PAPER}, {_SCISSORS}): ")
        game.play_one_hand(player_input)
        print(f"{game.player1.name}: : {game.player1.last_move}.\t{game.player2.name}: {game.player2.last_move}")
        print(f"{game.player1.name}: {game.player1.score},\t{game.player2.name}: {game.player2.score}")

    winner = game.get_winner()
    print(f"{winner.name} wins the game with {winner.score} points!")
