# Rock Paper Scissors Game

A Python implementation of the classic Rock, Paper, Scissors game with an object-oriented design.

## Features

- **Object-oriented design**: Uses classes and enums to represent moves, players, and the game logic.
- **Custom players**: Supports human players and computer-controlled players.
- **Flexible input**: Accepts moves as strings ("R", "P", "S"), enums, or move objects.
- **Scoring system**: First player to reach a configurable winning score wins the game.
- **Interactive gameplay**: Play against the computer from the command line.

## How to Play

1. Run the script:
   ```bash
   python rps_game.py
   ```
2. Enter your name when prompted.
3. Enter your move using:
   - `R` for Rock
   - `P` for Paper
   - `S` for Scissors
4. The game will display both players' moves and scores after each round.
5. The game continues until one player reaches the winning score (default 2 in the CLI).
6. Choose whether to play again or quit after each game.

## Code Structure

- **Move enum**: Represents Rock, Paper, and Scissors.
- **BaseMove and subclasses (Rock, Paper, Scissors)**: Define move behavior and comparisons.
- **BasePlayer abstract class**: Defines player interface and scoring.
- **Player**: Human player implementation.
- **ComputerPlayer**: Computer-controlled player with random move selection.
- **RPSGame**: Manages the game rounds, scoring, and winner determination.

## Example

```bash
Your name: Alice
Enter your move (R, P, S): R
Alice: Rock   Computer 123456: Paper
Alice: 0,    Computer 123456: 1
Enter your move (R, P, S):
...
```

## Requirements

- Python 3.8+

## License

MIT License
