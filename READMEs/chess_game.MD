# `chess_game.py` - Code Explanation

This document explains every function in `scripts/chess_game.py` in detail, including code snippets and thorough commentary. The file implements a chess engine with board representation, move generation, validation, and game state management.

---

## Imports

```python
import copy
from typing import List, Tuple, Optional, Dict
from enum import Enum
```

- `copy`: Used for deep copying the board state (important for move validation).
- `typing`: Provides type hints for lists, tuples, optionals, and dictionaries.
- `enum`: Used to define enumerations for piece types and colors.

---

## PieceType Enum

```python
class PieceType(Enum):
    PAWN = 'p'
    ROOK = 'r'
    KNIGHT = 'n'
    BISHOP = 'b'
    QUEEN = 'q'
    KING = 'k'
```

Defines all chess piece types, each with a single-character code for easy identification and display.

---

## Color Enum

```python
class Color(Enum):
    WHITE = 'white'
    BLACK = 'black'
```

Defines the two possible colors for pieces and players.

---

## Piece Class

```python
class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False
```

- Represents a chess piece.
- `has_moved` is used for castling and pawn movement rules.

```python
    def __str__(self):
        symbol = self.type.value
        return symbol.upper() if self.color == Color.WHITE else symbol.lower()
```

- Returns a single-character string for the piece, uppercase for white.

```python
    def __repr__(self):
        return f"{self.color.value} {self.type.value}"
```

- Returns a string like `"white p"` for debugging.

---

## Move Class

```python
class Move:
    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                 promotion: Optional[PieceType] = None, is_castling: bool = False,
                 is_en_passant: bool = False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
```

- Represents a move, including special moves like promotion, castling, and en passant.

```python
    def __str__(self):
        from_square = chr(ord('a') + self.from_pos[1]) + str(8 - self.from_pos[0])
        to_square = chr(ord('a') + self.to_pos[1]) + str(8 - self.to_pos[0])
        promotion_str = f"={self.promotion.value.upper()}" if self.promotion else ""
        return f"{from_square}{to_square}{promotion_str}"
```

- Converts the move to standard chess notation (e.g., "e2e4", "e7e8=Q").

```python
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (self.from_pos == other.from_pos and
                self.to_pos == other.to_pos and
                self.promotion == other.promotion)
```

- Allows moves to be compared for equality.

---

## ChessBoard Class

### Initialization

```python
class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.move_history = []
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.setup_initial_position()
```

- Initializes the board, sets the current player, and prepares the game state.

---

### Setting Up the Board

```python
    def setup_initial_position(self):
        """Set up the initial chess position"""
        # Place pawns
        for col in range(8):
            self.board[1][col] = Piece(PieceType.PAWN, Color.BLACK)
            self.board[6][col] = Piece(PieceType.PAWN, Color.WHITE)

        # Place other pieces
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
                      PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
                      PieceType.KNIGHT, PieceType.ROOK]

        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece(piece_type, Color.BLACK)
            self.board[7][col] = Piece(piece_type, Color.WHITE)
```

- Places all pieces in their standard starting positions.

---

### Board Access and Modification

```python
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
```

- Returns the piece at `(row, col)` or `None` if out of bounds.

```python
    def set_piece(self, row: int, col: int, piece: Optional[Piece]):
        """Set piece at given position"""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
```

- Places a piece at `(row, col)` if valid.

```python
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
```

- Checks if a position is on the board.

---

### Piece and King Search

```python
    def get_all_pieces(self, color: Color) -> List[Tuple[int, int, Piece]]:
        """Get all pieces of a given color with their positions"""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    pieces.append((row, col, piece))
        return pieces
```

- Returns all pieces of a given color with their positions.

```python
    def find_king(self, color: Color) -> Optional[Tuple[int, int]]:
        """Find the king of the given color"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    return (row, col)
        return None
```

- Finds the king's position for a given color.

---

### Attack and Move Validation

```python
    def is_square_attacked(self, row: int, col: int, by_color: Color) -> bool:
        """Check if a square is attacked by pieces of the given color"""
        for piece_row, piece_col, piece in self.get_all_pieces(by_color):
            if self.can_piece_attack_square(piece_row, piece_col, row, col):
                return True
        return False
```

- Checks if a square is attacked by any piece of the given color.

```python
    def can_piece_attack_square(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if a piece can attack a specific square"""
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False

        if piece.type == PieceType.PAWN:
            return self.can_pawn_attack(from_row, from_col, to_row, to_col, piece.color)
        elif piece.type == PieceType.ROOK:
            return self.can_rook_move(from_row, from_col, to_row, to_col)
        elif piece.type == PieceType.KNIGHT:
            return self.can_knight_move(from_row, from_col, to_row, to_col)
        elif piece.type == PieceType.BISHOP:
            return self.can_bishop_move(from_row, from_col, to_row, to_col)
        elif piece.type == PieceType.QUEEN:
            return (self.can_rook_move(from_row, from_col, to_row, to_col) or
                   self.can_bishop_move(from_row, from_col, to_row, to_col))
        elif piece.type == PieceType.KING:
            return self.can_king_move(from_row, from_col, to_row, to_col)

        return False
```

- Checks if a piece can attack a specific square, using piece-specific logic.

---

### Piece-Specific Move Checks

```python
    def can_pawn_attack(self, from_row: int, from_col: int, to_row: int, to_col: int, color: Color) -> bool:
        """Check if pawn can attack a square"""
        direction = -1 if color == Color.WHITE else 1
        return (to_row == from_row + direction and
                abs(to_col - from_col) == 1)
```

- Checks if a pawn can attack a square diagonally forward.

```python
    def can_rook_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if rook can move to target square"""
        if from_row != to_row and from_col != to_col:
            return False
        return self.is_path_clear(from_row, from_col, to_row, to_col)
```

- Checks if a rook can move to the target square (same row or column, path clear).

```python
    def can_knight_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if knight can move to target square"""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
```

- Checks if a knight can move to the target square (L-shape).

```python
    def can_bishop_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if bishop can move to target square"""
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        return self.is_path_clear(from_row, from_col, to_row, to_col)
```

- Checks if a bishop can move to the target square (diagonal, path clear).

```python
    def can_king_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if king can move to target square"""
        return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1
```

- Checks if a king can move to the target square (one square in any direction).

---

### Path Checking

```python
    def is_path_clear(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Check if path between two squares is clear"""
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        current_row, current_col = from_row + row_step, from_col + col_step

        while (current_row, current_col) != (to_row, to_col):
            if self.get_piece(current_row, current_col) is not None:
                return False
            current_row += row_step
            current_col += col_step

        return True
```

- Checks if all squares between two positions are empty.

---

### Check Detection

```python
    def is_in_check(self, color: Color) -> bool:
        """Check if the king of given color is in check"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False

        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_square_attacked(king_pos[0], king_pos[1], opponent_color)
```

- Returns `True` if the king of the given color is under attack.

---

### Move Generation

```python
    def generate_legal_moves(self, color: Color) -> List[Move]:
        """Generate all legal moves for the given color"""
        moves = []

        for row, col, piece in self.get_all_pieces(color):
            piece_moves = self.generate_piece_moves(row, col, piece)
            for move in piece_moves:
                if self.is_legal_move(move):
                    moves.append(move)

        return moves
```

- Generates all legal moves for the given color, filtering out moves that would leave the king in check.

```python
    def generate_piece_moves(self, row: int, col: int, piece: Piece) -> List[Move]:
        """Generate all possible moves for a piece"""
        moves = []

        if piece.type == PieceType.PAWN:
            moves.extend(self.generate_pawn_moves(row, col, piece.color))
        elif piece.type == PieceType.ROOK:
            moves.extend(self.generate_rook_moves(row, col))
        elif piece.type == PieceType.KNIGHT:
            moves.extend(self.generate_knight_moves(row, col))
        elif piece.type == PieceType.BISHOP:
            moves.extend(self.generate_bishop_moves(row, col))
        elif piece.type == PieceType.QUEEN:
            moves.extend(self.generate_queen_moves(row, col))
        elif piece.type == PieceType.KING:
            moves.extend(self.generate_king_moves(row, col, piece.color))

        return moves
```

- Generates all possible moves for a specific piece.

---

#### Pawn Moves

```python
    def generate_pawn_moves(self, row: int, col: int, color: Color) -> List[Move]:
        """Generate pawn moves"""
        moves = []
        direction = -1 if color == Color.WHITE else 1
        start_row = 6 if color == Color.WHITE else 1
        promotion_row = 0 if color == Color.WHITE else 7

        # Forward moves
        new_row = row + direction
        if self.is_valid_position(new_row, col) and not self.get_piece(new_row, col):
            if new_row == promotion_row:
                # Promotion
                for promotion_piece in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                    moves.append(Move((row, col), (new_row, col), promotion_piece))
            else:
                moves.append(Move((row, col), (new_row, col)))

                # Double move from starting position
                if row == start_row and not self.get_piece(new_row + direction, col):
                    moves.append(Move((row, col), (new_row + direction, col)))

        # Captures
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if self.is_valid_position(new_row, new_col):
                target_piece = self.get_piece(new_row, new_col)
                if target_piece and target_piece.color != color:
                    if new_row == promotion_row:
                        # Promotion capture
                        for promotion_piece in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                            moves.append(Move((row, col), (new_row, new_col), promotion_piece))
                    else:
                        moves.append(Move((row, col), (new_row, new_col)))

                # En passant
                if (self.en_passant_target and
                    self.en_passant_target == (new_row, new_col)):
                    moves.append(Move((row, col), (new_row, new_col), is_en_passant=True))

        return moves
```

- Generates all pawn moves, including promotions, double moves, captures, and en passant.

---

#### Rook, Knight, Bishop, Queen, King Moves

- `generate_rook_moves`, `generate_knight_moves`, `generate_bishop_moves`, `generate_queen_moves`, and `generate_king_moves` generate all possible moves for their respective pieces, including castling for the king.

---

### Move Legality and Execution

```python
    def is_legal_move(self, move: Move) -> bool:
        """Check if a move is legal (doesn't leave king in check)"""
        # Make a copy of the board and try the move
        temp_board = copy.deepcopy(self)
        temp_board.make_move(move, check_legality=False)

        # Check if the king is in check after the move
        return not temp_board.is_in_check(self.current_player)
```

- Checks if a move is legal by simulating it and checking for check.

```python
    def make_move(self, move: Move, check_legality: bool = True) -> bool:
        """Make a move on the board"""
        if check_legality:
            legal_moves = self.generate_legal_moves(self.current_player)
            if move not in legal_moves:
                return False

        from_row, from_col = move.from_pos
        to_row, to_col = move.to_pos

        piece = self.get_piece(from_row, from_col)
        if not piece:
            return False

        # Handle special moves
        if move.is_castling:
            self.handle_castling(move)
        elif move.is_en_passant:
            self.handle_en_passant(move)
        else:
            # Regular move
            self.set_piece(to_row, to_col, piece)
            self.set_piece(from_row, from_col, None)

            # Handle pawn promotion
            if move.promotion:
                self.set_piece(to_row, to_col, Piece(move.promotion, piece.color))

        # Mark piece as moved
        moved_piece = self.get_piece(to_row, to_col)
        if moved_piece:
            moved_piece.has_moved = True

        # Update en passant target
        self.update_en_passant_target(move, piece)

        # Update move counters
        self.move_history.append(move)
        if piece.type == PieceType.PAWN or self.get_piece(to_row, to_col):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.current_player == Color.BLACK:
            self.fullmove_number += 1

        # Switch players
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

        return True
```

- Executes a move, updates the board and game state, and handles special moves.

---

### Special Move Handlers

```python
    def handle_castling(self, move: Move):
        """Handle castling move"""
        from_row, from_col = move.from_pos
        to_row, to_col = move.to_pos

        # Move king
        king = self.get_piece(from_row, from_col)
        self.set_piece(to_row, to_col, king)
        self.set_piece(from_row, from_col, None)

        # Move rook
        if to_col == 6:  # Kingside
            rook = self.get_piece(from_row, 7)
            self.set_piece(from_row, 5, rook)
            self.set_piece(from_row, 7, None)
        else:  # Queenside
            rook = self.get_piece(from_row, 0)
            self.set_piece(from_row, 3, rook)
            self.set_piece(from_row, 0, None)
```

- Handles castling by moving both the king and rook.

```python
    def handle_en_passant(self, move: Move):
        """Handle en passant capture"""
        from_row, from_col = move.from_pos
        to_row, to_col = move.to_pos

        # Move pawn
        pawn = self.get_piece(from_row, from_col)
        self.set_piece(to_row, to_col, pawn)
        self.set_piece(from_row, from_col, None)

        # Remove captured pawn
        self.set_piece(from_row, to_col, None)
```

- Handles en passant pawn capture.

```python
    def update_en_passant_target(self, move: Move, piece: Piece):
        """Update en passant target square"""
        self.en_passant_target = None

        if (piece.type == PieceType.PAWN and
            abs(move.to_pos[0] - move.from_pos[0]) == 2):
            # Pawn moved two squares
            target_row = (move.from_pos[0] + move.to_pos[0]) // 2
            self.en_passant_target = (target_row, move.to_pos[1])
```

- Updates the en passant target square after a pawn moves two squares.

---

### Game State Checks

```python
    def is_checkmate(self, color: Color) -> bool:
        """Check if the given color is in checkmate"""
        return self.is_in_check(color) and len(self.generate_legal_moves(color)) == 0
```

- Returns `True` if the given color is in checkmate.

```python
    def is_stalemate(self, color: Color) -> bool:
        """Check if the given color is in stalemate"""
        return not self.is_in_check(color) and len(self.generate_legal_moves(color)) == 0
```

- Returns `True` if the given color is in stalemate.

```python
    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """Check if the game is over and return the result"""
        if self.is_checkmate(self.current_player):
            winner = "White" if self.current_player == Color.BLACK else "Black"
            return True, f"Checkmate! {winner} wins!"
        elif self.is_stalemate(self.current_player):
            return True, "Stalemate! It's a draw!"
        elif self.halfmove_clock >= 100:  # 50-move rule
            return True, "Draw by 50-move rule!"

        return False, None
```

- Checks if the game is over due to checkmate, stalemate, or the 50-move rule.

---

## Main Block

```python
if __name__ == "__main__":
    # Test the chess board
    board = ChessBoard()
    print("Chess board initialized successfully!")
    print(f"Current player: {board.current_player.value}")
    print(f"Legal moves for white: {len(board.generate_legal_moves(Color.WHITE))}")
```

- Initializes a chess board and prints basic info for testing.

---

## Summary

This file provides a complete, object-oriented chess engine backend. It covers all standard chess rules, including special moves and endgame detection, and is suitable for use in a chess bot or GUI.
