# `chess_bot.py` - Line-by-Line Explanation

This file implements a chess AI (bot) using the minimax algorithm with alpha-beta pruning and positional evaluation tables. Below is a detailed, line-by-line explanation with code snippets.

---

## Imports

```python
import random
import time
from typing import Optional, Tuple, List
from chess_game import ChessBoard, Color, Move, PieceType, Piece
```

- `random`: For random move selection at the lowest difficulty.
- `time`: For timing bot calculations.
- `typing`: Type hints for clarity.
- Imports all chess logic and data structures from `chess_game.py`.

---

## ChessBot Class

### Initialization

```python
class ChessBot:
    def __init__(self, color: Color, difficulty: int = 3):
        self.color = color
        self.difficulty = max(1, min(difficulty, 6))  # Depth 1-6
        self.piece_values = {
            PieceType.PAWN: 100,
            PieceType.KNIGHT: 320,
            PieceType.BISHOP: 330,
            PieceType.ROOK: 500,
            PieceType.QUEEN: 900,
            PieceType.KING: 20000
        }
```

- Sets the bot's color and search depth (difficulty).
- Defines the material value for each piece type.

#### Piece-Square Tables

```python
        # Position tables for piece-square evaluation
        self.pawn_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        # ... (similar tables for knight, bishop, rook, queen, king)
```

- These tables give positional bonuses/penalties for each piece type depending on its square.

```python
        self.nodes_searched = 0
```

- Tracks the number of nodes (positions) searched during minimax.

---

### get_best_move

```python
    def get_best_move(self, board: ChessBoard) -> Optional[Move]:
        """Get the best move using minimax with alpha-beta pruning"""
        self.nodes_searched = 0
        start_time = time.time()

        legal_moves = board.generate_legal_moves(self.color)
        if not legal_moves:
            return None

        if self.difficulty == 1:
            # Random move for easiest difficulty
            return random.choice(legal_moves)

        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Order moves to improve alpha-beta pruning
        ordered_moves = self.order_moves(board, legal_moves)

        for move in ordered_moves:
            # Make move on a copy of the board
            temp_board = self.copy_board(board)
            temp_board.make_move(move, check_legality=False)

            # Evaluate the position
            score = self.minimax(temp_board, self.difficulty - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        end_time = time.time()
        print(f"Bot searched {self.nodes_searched} nodes in {end_time - start_time:.2f} seconds")
        print(f"Best move evaluation: {best_score}")

        return best_move
```

- Finds the best move using minimax with alpha-beta pruning.
- At difficulty 1, picks a random move.
- For higher difficulties, evaluates each move using minimax, tracks the best score, and prints search stats.

---

### minimax

```python
    def minimax(self, board: ChessBoard, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        self.nodes_searched += 1

        # Check for terminal conditions
        game_over, result = board.is_game_over()
        if game_over:
            if "wins" in result:
                if (self.color == Color.WHITE and "White wins" in result) or \
                   (self.color == Color.BLACK and "Black wins" in result):
                    return 10000 + depth  # Prefer quicker wins
                else:
                    return -10000 - depth  # Avoid slower losses
            else:
                return 0  # Draw

        if depth == 0:
            return self.evaluate_position(board)

        current_color = board.current_player
        legal_moves = board.generate_legal_moves(current_color)

        if not legal_moves:
            return 0  # Stalemate

        if maximizing:
            max_eval = float('-inf')
            for move in self.order_moves(board, legal_moves):
                temp_board = self.copy_board(board)
                temp_board.make_move(move, check_legality=False)

                eval_score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.order_moves(board, legal_moves):
                temp_board = self.copy_board(board)
                temp_board.make_move(move, check_legality=False)

                eval_score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break
            return min_eval
```

- Implements the minimax algorithm with alpha-beta pruning.
- Recursively evaluates moves up to the given depth.
- Returns a high score for quick wins, low for losses, 0 for draws/stalemate.
- Uses maximizing/minimizing logic depending on whose turn it is.

---

### evaluate_position

```python
    def evaluate_position(self, board: ChessBoard) -> float:
        """Evaluate the current position"""
        score = 0

        # Material and positional evaluation
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    piece_value = self.get_piece_value(piece, row, col)
                    if piece.color == self.color:
                        score += piece_value
                    else:
                        score -= piece_value

        # Add mobility bonus
        our_moves = len(board.generate_legal_moves(self.color))
        opponent_color = Color.BLACK if self.color == Color.WHITE else Color.WHITE

        # Temporarily switch to opponent to count their moves
        original_player = board.current_player
        board.current_player = opponent_color
        opponent_moves = len(board.generate_legal_moves(opponent_color))
        board.current_player = original_player

        score += (our_moves - opponent_moves) * 10

        # King safety
        if board.is_in_check(self.color):
            score -= 50
        if board.is_in_check(opponent_color):
            score += 50

        return score
```

- Evaluates a board position based on material, piece positions, mobility (number of legal moves), and king safety.

---

### get_piece_value

```python
    def get_piece_value(self, piece: Piece, row: int, col: int) -> float:
        """Get the value of a piece including positional bonus"""
        base_value = self.piece_values[piece.type]

        # Adjust for piece color (flip table for black pieces)
        table_row = row if piece.color == Color.WHITE else 7 - row

        positional_bonus = 0
        if piece.type == PieceType.PAWN:
            positional_bonus = self.pawn_table[table_row][col]
        elif piece.type == PieceType.KNIGHT:
            positional_bonus = self.knight_table[table_row][col]
        elif piece.type == PieceType.BISHOP:
            positional_bonus = self.bishop_table[table_row][col]
        elif piece.type == PieceType.ROOK:
            positional_bonus = self.rook_table[table_row][col]
        elif piece.type == PieceType.QUEEN:
            positional_bonus = self.queen_table[table_row][col]
        elif piece.type == PieceType.KING:
            positional_bonus = self.king_middle_game_table[table_row][col]

        return base_value + positional_bonus
```

- Returns the value of a piece, including its positional bonus from the relevant table.

---

### order_moves

```python
    def order_moves(self, board: ChessBoard, moves: List[Move]) -> List[Move]:
        """Order moves for better alpha-beta pruning"""
        def move_priority(move):
            score = 0

            # Prioritize captures
            target_piece = board.get_piece(move.to_pos[0], move.to_pos[1])
            if target_piece:
                score += self.piece_values[target_piece.type]

                # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                attacker = board.get_piece(move.from_pos[0], move.from_pos[1])
                if attacker:
                    score += self.piece_values[target_piece.type] - self.piece_values[attacker.type]

            # Prioritize promotions
            if move.promotion:
                score += self.piece_values[move.promotion]

            # Prioritize checks
            temp_board = self.copy_board(board)
            temp_board.make_move(move, check_legality=False)
            opponent_color = Color.BLACK if self.color == Color.WHITE else Color.WHITE
            if temp_board.is_in_check(opponent_color):
                score += 100

            return score

        return sorted(moves, key=move_priority, reverse=True)
```

- Orders moves to improve pruning efficiency: captures, promotions, and checks are prioritized.

---

### copy_board

```python
    def copy_board(self, board: ChessBoard) -> ChessBoard:
        """Create a deep copy of the board"""
        import copy
        return copy.deepcopy(board)
```

- Returns a deep copy of the board for safe move simulation.

---

## Main Block (Testing)

```python
if __name__ == "__main__":
    # Test the chess bot
    from chess_game import ChessBoard, Color

    board = ChessBoard()
    bot = ChessBot(Color.WHITE, difficulty=3)

    print("Testing chess bot...")
    best_move = bot.get_best_move(board)
    print(f"Bot's best move: {best_move}")
```

- If run directly, creates a board and bot, then prints the bot's best move for the starting position.

---

**Summary:**  
This module provides a chess AI using minimax with alpha-beta pruning, positional evaluation, and move ordering for efficient and strong play at various difficulty levels.
