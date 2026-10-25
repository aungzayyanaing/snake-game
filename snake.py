"""
Snake Apple Game - Python + tkinter (no extra packages needed).

How to play:
    python3 snake.py
    Arrow keys or WASD to move, P to pause, R to restart after game over.
    Eat the red apple to grow and score. Don't hit the walls or yourself!

Controls are the whole game: one apple at a time, the snake gets
a little faster with every apple, and your best score is saved
in highscore.txt next to this file.
"""

import random
import tkinter as tk
from pathlib import Path

CELL = 30
COLS = 20
ROWS = 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS
START_DELAY = 140  # ms between moves, shrinks as you eat
MIN_DELAY = 70

BG = "#0f1a12"
GRID = "#16241b"
SNAKE_HEAD = "#4ade80"
SNAKE_BODY = "#22c55e"
APPLE = "#ef4444"
TEXT = "#e7f5e9"


def load_highscore() -> int:
    try:
        return int(Path(__file__).with_name("highscore.txt").read_text().strip())
    except (OSError, ValueError):
        return 0


def save_highscore(score: int) -> None:
    try:
        Path(__file__).with_name("highscore.txt").write_text(str(score))
    except OSError:
        pass


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Apple Game")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()
        self.score_label = tk.Label(
            root, text="", font=("Helvetica", 14, "bold"),
            bg=BG, fg=TEXT)
        self.score_label.pack(fill="x")
        self.highscore = load_highscore()
        self.reset()
        root.bind("<Up>", lambda e: self.turn(0, -1))
        root.bind("<Down>", lambda e: self.turn(0, 1))
        root.bind("<Left>", lambda e: self.turn(-1, 0))
        root.bind("<Right>", lambda e: self.turn(1, 0))
        root.bind("w", lambda e: self.turn(0, -1))
        root.bind("s", lambda e: self.turn(0, 1))
        root.bind("a", lambda e: self.turn(-1, 0))
        root.bind("d", lambda e: self.turn(1, 0))
        root.bind("p", lambda e: self.toggle_pause())
        root.bind("P", lambda e: self.toggle_pause())
        root.bind("r", lambda e: self.restart())
        root.bind("R", lambda e: self.restart())
        self.tick()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.pending = (1, 0)
        self.score = 0
        self.delay = START_DELAY
        self.alive = True
        self.paused = False
        self.apple = self.spawn_apple()

    def spawn_apple(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def turn(self, dx, dy):
        # Never reverse straight into yourself.
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.pending = (dx, dy)

    def toggle_pause(self):
        if self.alive:
            self.paused = not self.paused

    def restart(self):
        if not self.alive:
            self.reset()

    def step(self):
        if not self.alive or self.paused:
            return
        self.direction = self.pending
        hx, hy = self.snake[0]
        dx, dy = self.direction
        head = (hx + dx, hy + dy)
        x, y = head
        if not (0 <= x < COLS and 0 <= y < ROWS) or head in self.snake:
            self.alive = False
            if self.score > self.highscore:
                self.highscore = self.score
                save_highscore(self.highscore)
            return
        self.snake.insert(0, head)
        if head == self.apple:
            self.score += 1
            self.delay = max(MIN_DELAY, self.delay - 3)
            self.apple = self.spawn_apple()
            if self.apple is None:
                self.alive = False
        else:
            self.snake.pop()

    def draw(self):
        c = self.canvas
        c.delete("all")
        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    c.create_rectangle(x * CELL, y * CELL,
                                       (x + 1) * CELL, (y + 1) * CELL,
                                       fill=GRID, outline="")
        if self.apple:
            ax, ay = self.apple
            c.create_oval(ax * CELL + 4, ay * CELL + 4,
                          (ax + 1) * CELL - 4, (ay + 1) * CELL - 4,
                          fill=APPLE, outline="")
            c.create_rectangle(ax * CELL + 13, ay * CELL + 1,
                               ax * CELL + 17, ay * CELL + 7,
                               fill="#22c55e", outline="")
        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pad = 2 if i == 0 else 4
            c.create_rectangle(x * CELL + pad, y * CELL + pad,
                               (x + 1) * CELL - pad, (y + 1) * CELL - pad,
                               fill=color, outline="")
        self.score_label.config(
            text=f"Score: {self.score}   Best: {self.highscore}")
        if self.paused:
            c.create_text(WIDTH // 2, HEIGHT // 2, text="PAUSED - press P",
                          fill=TEXT, font=("Helvetica", 20, "bold"))
        if not self.alive:
            c.create_text(WIDTH // 2, HEIGHT // 2 - 20,
                          text="GAME OVER", fill=TEXT,
                          font=("Helvetica", 28, "bold"))
            c.create_text(WIDTH // 2, HEIGHT // 2 + 20,
                          text=f"Score: {self.score}  -  press R to restart",
                          fill=TEXT, font=("Helvetica", 14))

    def tick(self):
        self.step()
        self.draw()
        if self.alive or self.paused:
            self.root.after(self.delay, self.tick)
        else:
            # Keep the game-over screen painted; R restarts via reset+tick.
            self.root.after(500, self._wait_restart)

    def _wait_restart(self):
        if not self.alive:
            self.draw()
            self.root.after(500, self._wait_restart)
        else:
            self.tick()


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
