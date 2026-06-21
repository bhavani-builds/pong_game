# 🏓 Pong

A classic 2-player Pong game built with Python and [Pygame](https://www.pygame.org/).

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.5%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

- Local 2-player gameplay on a single keyboard
- Ball speeds up slightly with each paddle hit (capped, so it stays playable)
- Ball angle depends on where it hits the paddle
- Pause / resume support
- First to 5 points wins, with a restart option
- No external assets — pure code, runs anywhere Pygame runs

## Requirements

- Python 3.8+
- Pygame 2.5+

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/bhavani-builds/pong-game.git
cd pong-game

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python pong_game.py
```

### Controls

| Key                    | Action              |
|-------------------------|---------------------|
| `W` / `S`               | Player 1 paddle up/down |
| `Up` / `Down` arrows    | Player 2 paddle up/down |
| `P`                     | Pause / unpause |
| `R`                     | Restart after a win |
| `Esc`                   | Quit |

## How It Works

The game loop (in the `PongGame` class) does three things every frame:

1. **Input** — reads which keys are held down and moves each `Paddle` accordingly, clamped to stay on screen.
2. **Update** — moves the `Ball`, bounces it off the top/bottom walls and off paddles (with angle based on hit position), and checks if it went past either side to award a point.
3. **Draw** — renders the paddles, ball, scores, and any pause/game-over overlay.

Tweak constants at the top of `pong_game.py` — `PADDLE_SPEED`, `BALL_SPEED_START`, `BALL_SPEEDUP`, `WINNING_SCORE`, colors, etc. — to change the feel of the game.

## Possible Improvements

Contributions and forks welcome! Some ideas:

- [ ] Add a single-player mode with a simple AI opponent
- [ ] Add sound effects for hits/scores
- [ ] Add a main menu / difficulty selector
- [ ] Persist match history to a file
- [ ] Add gamepad/controller support

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
