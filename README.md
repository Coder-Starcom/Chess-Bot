# ♟️ Chess Bot 🤖

## 📝 Overview

Welcome to **Chess Bot**!  
This project lets you play chess against a smart computer opponent or another human, right from your terminal.  
It features:

- A command-line interface 🖥️
- Multiple game modes (Human vs Bot, Bot vs Bot, Human vs Human)
- A chess engine powered by the Minimax algorithm with alpha-beta pruning for strong, strategic play!
- Move history, hints, and more!

---

## ⚙️ Prerequisites

- 🐍 **Python 3.x** installed on your machine.
- ♟️ Basic understanding of chess rules and algebraic notation.

---

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Coder-Starcom/Chess-Bot.git
   cd Chess-Bot
   ```

2. **Install dependencies:**  
   _(No external dependencies required for basic play!)_  
   But if you add any, install them with:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Chess Bot

To start playing, simply run:

```bash
python scripts/chess_cli.py
```

---

## 🎮 Usage & Features

- 🕹️ **Game Modes:**

  - Play as White or Black against the computer
  - Watch two bots battle it out
  - Play against a friend locally

- ⌨️ **Controls:**

  - Enter moves in algebraic notation (e.g., `e2e4`, `g1f3`, `e7e8q` for promotion)
  - Type `help` to see all legal moves
  - Type `history` to view recent moves
  - Type `status` to see the current game state
  - Type `flip` to flip the board view
  - Type `quit` to exit the game

- 💡 **Features:**
  - Move validation and hints
  - Pawn promotion, castling, and en passant supported
  - Move history and game status display
  - Adjustable bot difficulty (from random to deep search)
  - ASCII board display with clear piece symbols

---

## 📦 Project Structure

```
Chess-Bot/
├── scripts/
│   ├── chess_game.py      # Core chess logic and board representation
│   ├── chess_utils.py     # Display, input parsing, and helpers
│   ├── chess_bot.py       # Chess AI (Minimax with alpha-beta pruning)
│   └── chess_cli.py       # Command-line interface
└── README.md
```

---

## 🏁 Example Session

```
🏰 CHESS GAME 🏰
1. Play vs Computer (White)
2. Play vs Computer (Black)
3. Computer vs Computer
4. Human vs Human
5. Show Rules
6. Quit

Select option (1-6): 1

You are playing as White against the computer (Difficulty: 3)

Current player: White
    a  b  c  d  e  f  g  h
  +-------------------------+
8 | r  n  b  q  k  b  n  r | 8
7 | p  p  p  p  p  p  p  p | 7
6 | .     .     .     .     | 6
5 |     .     .     .     . | 5
4 | .     .     .     .     | 4
3 |     .     .     .     . | 3
2 | P  P  P  P  P  P  P  P | 2
1 | R  N  B  Q  K  B  N  R | 1
  +-------------------------+
    a  b  c  d  e  f  g  h

White's turn. Enter move (or 'help'):
```

---

## 🙏 Acknowledgements

- Thanks to the open-source chess community for inspiration!
- Built with ❤️ and Python.

---

Enjoy your game! If you like this project, ⭐️ star it on GitHub!
