# Snake Apple Game (Python)

A classic Snake game built with Python's built-in `tkinter`, so there is nothing to install. It runs in a fixed-size 600×600 window on a 20×20 grid.

## Play

```bash
python3 snake.py
```

- **Move:** Arrow keys or WASD. You cannot turn directly back on yourself.
- **Pause:** P
- **Restart after game over:** R

Eat the red apple to grow by one segment and score a point. A new apple appears on a random free square each time. The snake starts at 140 ms per move and gets 3 ms faster with each apple, down to 70 ms. Hitting a wall or your own tail ends the game; the game-over screen shows your score, and you can press R to play again. Your current score and best score are shown below the board as `Score: X  Best: Y`, and a new best score is saved in `highscore.txt` when you beat it. The snake is red on Saturday and Sunday, blue on Monday to Friday.

## Requirements

Python 3 with `tkinter` (part of Python's standard library). No other packages are needed.

## Files

- `snake.py` — the whole game, one file
- `highscore.txt` — created when you set a new best score (not committed)
- `.gitignore` — keeps `highscore.txt` and Python bytecode out of the repo
