# `chess_utils.py` - Line-by-Line Explanation

This file provides utility functions for displaying the chess board, parsing user input, formatting move lists, and reporting game status. Below is a detailed, line-by-line explanation with code snippets.

---

## Imports

```python
from typing import Optional, Tuple
from chess_game import ChessBoard, Move, Color, PieceType
```

- `Optional`, `Tuple`: Type hints for function signatures.
- Imports core chess classes and enums from `chess_game.py`.

---

## display_board

```python
def display_board(board: ChessBoard, flip: bool = False):
    """Display the chess board in ASCII format"""
    print("\n" + "="*50)
    print(f"Current player: {board.current_player.value.title()}")

    if board.is_in_check(board.current_player):
        print("*** CHECK! ***")

    print("="*50)
```

- Prints a header, current player, and a warning if the player is in check.

```python
    # Column labels
    if flip:
        print("    h  g  f  e  d  c  b  a")
    else:
        print("    a  b  c  d  e  f  g  h")

    print("  " + "+"*25)
```

- Prints column labels, optionally flipped for black's perspective.

```python
    rows = range(8) if not flip else range(7, -1, -1)

    for row in rows:
        row_num = 8 - row
        print(f"{row_num} |", end="")

        cols = range(8) if not flip else range(7, -1, -1)
        for col in cols:
            piece = board.get_piece(row, col)
            if piece:
                symbol = str(piece)
                # Add color coding for better visibility
                if piece.color == Color.WHITE:
                    print(f" {symbol} ", end="")
                else:
                    print(f" {symbol} ", end="")
            else:
                # Show square color pattern
                if (row + col) % 2 == 0:
                    print(" . ", end="")
                else:
                    print("   ", end="")

        print(f"| {row_num}")

    print("  " + "+"*25)
```

- Loops through each row and column, printing pieces or empty squares with a checkerboard pattern.

```python
    if flip:
        print("    h  g  f  e  d  c  b  a")
    else:
        print("    a  b  c  d  e  f  g  h")

    print()
```

- Prints column labels again at the bottom.

---

## parse_move_input

```python
def parse_move_input(move_str: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], Optional[PieceType]]]:
    """Parse move input like 'e2e4' or 'e7e8q' for promotion"""
    move_str = move_str.strip().lower()

    if len(move_str) < 4 or len(move_str) > 5:
        return None
```

- Cleans the input and checks for valid length (4 for normal, 5 for promotion).

```python
    try:
        # Parse from square
        from_col = ord(move_str[0]) - ord('a')
        from_row = 8 - int(move_str[1])

        # Parse to square
        to_col = ord(move_str[2]) - ord('a')
        to_row = 8 - int(move_str[3])

        # Check bounds
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and
                0 <= to_row < 8 and 0 <= to_col < 8):
            return None
```

- Converts algebraic notation (e.g., 'e2') to board coordinates.
- Checks if all coordinates are within bounds.

```python
        # Parse promotion
        promotion = None
        if len(move_str) == 5:
            promotion_char = move_str[4]
            promotion_map = {
                'q': PieceType.QUEEN,
                'r': PieceType.ROOK,
                'b': PieceType.BISHOP,
                'n': PieceType.KNIGHT
            }
            promotion = promotion_map.get(promotion_char)
            if not promotion:
                return None

        return ((from_row, from_col), (to_row, to_col), promotion)

    except (ValueError, IndexError):
        return None
```

- Handles pawn promotion input (e.g., 'e7e8q').
- Returns a tuple of from-position, to-position, and promotion type, or `None` if invalid.

---

## find_move_from_input

```python
def find_move_from_input(board: ChessBoard, move_input: str) -> Optional[Move]:
    """Find a legal move that matches the input"""
    parsed = parse_move_input(move_input)
    if not parsed:
        return None

    from_pos, to_pos, promotion = parsed
    legal_moves = board.generate_legal_moves(board.current_player)

    for move in legal_moves:
        if (move.from_pos == from_pos and
            move.to_pos == to_pos and
            move.promotion == promotion):
            return move

    return None
```

- Parses the input and searches for a matching legal move in the current position.
- Returns the `Move` object if found, otherwise `None`.

---

## get_move_list_display

```python
def get_move_list_display(moves: list, max_moves: int = 10) -> str:
    """Get a formatted string of available moves"""
    if not moves:
        return "No legal moves available"

    move_strs = [str(move) for move in moves[:max_moves]]
    result = "Available moves: " + ", ".join(move_strs)

    if len(moves) > max_moves:
        result += f" ... and {len(moves) - max_moves} more"

    return result
```

- Formats a list of moves for display, showing up to `max_moves` and indicating if more are available.

---

## get_game_status

```python
def get_game_status(board: ChessBoard) -> str:
    """Get current game status as a string"""
    game_over, result = board.is_game_over()

    if game_over:
        return result

    status = f"{board.current_player.value.title()} to move"

    if board.is_in_check(board.current_player):
        status += " (in check)"

    legal_moves = board.generate_legal_moves(board.current_player)
    status += f" - {len(legal_moves)} legal moves"

    return status
```

- Returns a string describing the current game status, including check, number of legal moves, and game over messages.

---

## format_move_history

```python
def format_move_history(board: ChessBoard, last_n: int = 10) -> str:
    """Format the last N moves from the game history"""
    if not board.move_history:
        return "No moves played yet"

    moves = board.move_history[-last_n:]
    formatted_moves = []

    for i, move in enumerate(moves):
        move_num = len(board.move_history) - len(moves) + i + 1
        if move_num % 2 == 1:  # White's move
            formatted_moves.append(f"{(move_num + 1) // 2}. {move}")
        else:  # Black's move
            if len(formatted_moves) > 0:
                formatted_moves[-1] += f" {move}"
            else:
                formatted_moves.append(f"{move_num // 2}... {move}")

    return "Recent moves: " + " ".join(formatted_moves)
```

- Formats the last `last_n` moves for display, grouping white and black moves together in standard chess notation.

---

## Main Block (Testing)

```python
if __name__ == "__main__":
    # Test utility functions
    from chess_game import ChessBoard

    board = ChessBoard()
    print("Testing chess utilities...")

    display_board(board)
    print(get_game_status(board))

    # Test move parsing
    test_moves = ["e2e4", "e7e8q", "invalid", "a1h8"]
    for move_str in test_moves:
        parsed = parse_move_input(move_str)
        print(f"'{move_str}' -> {parsed}")
```

- Runs a simple test if the script is executed directly:
  - Initializes a board.
  - Displays the board and game status.
  - Tests move parsing with several example inputs.

---

**Summary:**  
This utility module provides all the necessary functions for displaying the board, parsing user input, formatting move lists, and reporting game status, making it easier to build a user interface or command-line chess application.
