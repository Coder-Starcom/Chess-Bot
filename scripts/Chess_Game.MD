Here’s a function-by-function explanation for the code in your selection (lines 370–end):

---

### `is_legal_move(self, move: Move) -> bool`
Checks if a move is legal (i.e., does not leave the current player's king in check).
- Makes a deep copy of the board.
- Executes the move on the copy (without legality checks).
- Returns `True` if the king is not in check after the move.

---

### `make_move(self, move: Move, check_legality: bool = True) -> bool`
Executes a move on the board, updating all relevant state.
- If `check_legality` is `True`, checks if the move is legal.
- Handles special moves: castling and en passant.
- Handles pawn promotion.
- Updates the board, move history, en passant target, move counters, and switches the current player.

---

### `handle_castling(self, move: Move)`
Handles the movement of both the king and rook during a castling move.
- Moves the king to its castling destination.
- Moves the rook to the correct square (depending on kingside or queenside castling).

---

### `handle_en_passant(self, move: Move)`
Handles the en passant pawn capture.
- Moves the capturing pawn.
- Removes the captured pawn from the board.

---

### `update_en_passant_target(self, move: Move, piece: Piece)`
Updates the en passant target square after a pawn moves two squares.
- If a pawn moves two squares, sets the en passant target to the square it passed over.
- Otherwise, clears the en passant target.

---

### `is_checkmate(self, color: Color) -> bool`
Returns `True` if the given color is in checkmate (king is in check and there are no legal moves).

---

### `is_stalemate(self, color: Color) -> bool`
Returns `True` if the given color is in stalemate (king is not in check and there are no legal moves).

---

### `is_game_over(self) -> Tuple[bool, Optional[str]]`
Checks if the game is over due to checkmate, stalemate, or the 50-move rule, and returns the result as a tuple `(True, message)` or `(False, None)`.

---

### Main Block
```python
if __name__ == "__main__":
    # Test the chess board
    board = ChessBoard()
    print("Chess board initialized successfully!")
    print(f"Current player: {board.current_player.value}")
    print(f"Legal moves for white: {len(board.generate_legal_moves(Color.WHITE))}")
```
- Initializes a chess board and prints some basic info for testing.

---

Let me know if you want a deeper dive into any specific function!