"""
Command Line Interface for Chess Game
"""
import sys
import os
from typing import Optional
from chess_game import ChessBoard, Color, Move
from chess_bot import ChessBot
from chess_utils import (
    display_board, 
    find_move_from_input, 
    get_move_list_display, 
    get_game_status,
    format_move_history
)

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.human_color = None
        self.bot = None
        self.game_mode = None
    
    def show_menu(self):
        """Show the main menu"""
        print("\n" + "="*50)
        print("🏰 CHESS GAME 🏰")
        print("="*50)
        print("1. Play vs Computer (White)")
        print("2. Play vs Computer (Black)")
        print("3. Computer vs Computer")
        print("4. Human vs Human")
        print("5. Show Rules")
        print("6. Quit")
        print("="*50)
    
    def get_difficulty_level(self) -> int:
        """Get bot difficulty level from user"""
        while True:
            print("\nSelect difficulty level:")
            print("1. Beginner (Random moves)")
            print("2. Easy (Depth 2)")
            print("3. Medium (Depth 3)")
            print("4. Hard (Depth 4)")
            print("5. Expert (Depth 5)")
            print("6. Master (Depth 6)")
            
            try:
                choice = int(input("Enter difficulty (1-6): ").strip())
                if 1 <= choice <= 6:
                    return choice
                else:
                    print("Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")
    
    def setup_game(self, mode: int):
        """Setup the game based on selected mode"""
        self.game_mode = mode
        
        if mode == 1:  # Human (White) vs Computer (Black)
            self.human_color = Color.WHITE
            difficulty = self.get_difficulty_level()
            self.bot = ChessBot(Color.BLACK, difficulty)
            print(f"\nYou are playing as White against the computer (Difficulty: {difficulty})")
        
        elif mode == 2:  # Human (Black) vs Computer (White)
            self.human_color = Color.BLACK
            difficulty = self.get_difficulty_level()
            self.bot = ChessBot(Color.WHITE, difficulty)
            print(f"\nYou are playing as Black against the computer (Difficulty: {difficulty})")
        
        elif mode == 3:  # Computer vs Computer
            difficulty1 = self.get_difficulty_level()
            print("Select difficulty for second bot:")
            difficulty2 = self.get_difficulty_level()
            self.bot = ChessBot(Color.WHITE, difficulty1)
            self.bot2 = ChessBot(Color.BLACK, difficulty2)
            print(f"\nComputer vs Computer: White (Difficulty {difficulty1}) vs Black (Difficulty {difficulty2})")
        
        elif mode == 4:  # Human vs Human
            self.human_color = None  # Both players are human
            print("\nHuman vs Human mode selected")
    
    def show_rules(self):
        """Display chess rules and commands"""
        print("\n" + "="*60)
        print("♟️  CHESS RULES & COMMANDS ♟️")
        print("="*60)
        print("\n📋 HOW TO PLAY:")
        print("• Enter moves in algebraic notation: e2e4, d7d5, etc.")
        print("• For pawn promotion, add the piece: e7e8q (for queen)")
        print("• Castling is done by moving the king: e1g1 (kingside)")
        print("\n🎯 SPECIAL MOVES:")
        print("• Castling: Move king two squares toward rook")
        print("• En passant: Automatic when conditions are met")
        print("• Promotion: Add q/r/b/n after pawn reaches end")
        print("\n⌨️  COMMANDS:")
        print("• 'help' - Show available moves")
        print("• 'history' - Show recent moves")
        print("• 'status' - Show game status")
        print("• 'quit' - Exit the game")
        print("• 'flip' - Flip board view")
        print("\n🏆 WIN CONDITIONS:")
        print("• Checkmate: King is in check and cannot escape")
        print("• Stalemate: No legal moves but king not in check")
        print("• Draw: 50 moves without pawn move or capture")
        print("="*60)
    
    def get_human_move(self) -> Optional[Move]:
        """Get move input from human player"""
        while True:
            try:
                move_input = input(f"\n{self.board.current_player.value.title()}'s turn. Enter move (or 'help'): ").strip().lower()
                
                if move_input == 'quit':
                    return 'quit'
                elif move_input == 'help':
                    legal_moves = self.board.generate_legal_moves(self.board.current_player)
                    print(f"\n{get_move_list_display(legal_moves, 20)}")
                    continue
                elif move_input == 'history':
                    print(f"\n{format_move_history(self.board)}")
                    continue
                elif move_input == 'status':
                    print(f"\n{get_game_status(self.board)}")
                    continue
                elif move_input == 'flip':
                    return 'flip'
                
                move = find_move_from_input(self.board, move_input)
                if move:
                    return move
                else:
                    print("❌ Invalid move! Try again or type 'help' for available moves.")
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                return 'quit'
            except EOFError:
                print("\n\nGame ended.")
                return 'quit'
    
    def play_game(self):
        """Main game loop"""
        flip_board = False
        
        while True:
            # Display board
            display_board(self.board, flip=flip_board)
            print(get_game_status(self.board))
            
            # Check if game is over
            game_over, result = self.board.is_game_over()
            if game_over:
                print(f"\n🎉 GAME OVER: {result}")
                print(format_move_history(self.board, 20))
                break
            
            move = None
            
            # Determine who should move
            if self.game_mode == 3:  # Computer vs Computer
                if self.board.current_player == Color.WHITE:
                    print("\n🤖 White bot is thinking...")
                    move = self.bot.get_best_move(self.board)
                else:
                    print("\n🤖 Black bot is thinking...")
                    move = self.bot2.get_best_move(self.board)
                
                if move:
                    print(f"Bot plays: {move}")
                    input("Press Enter to continue...")
            
            elif self.game_mode == 4:  # Human vs Human
                move = self.get_human_move()
            
            else:  # Human vs Computer
                if self.board.current_player == self.human_color:
                    move = self.get_human_move()
                else:
                    print(f"\n🤖 Computer is thinking...")
                    move = self.bot.get_best_move(self.board)
                    if move:
                        print(f"Computer plays: {move}")
            
            # Handle special commands
            if move == 'quit':
                print("Thanks for playing! 👋")
                break
            elif move == 'flip':
                flip_board = not flip_board
                continue
            
            # Make the move
            if move and isinstance(move, Move):
                success = self.board.make_move(move)
                if not success:
                    print("❌ Move failed! This shouldn't happen.")
            elif move is None:
                print("❌ No move available!")
                break
    
    def run(self):
        """Main application loop"""
        print("Welcome to Chess! 🏰")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("Select option (1-6): ").strip()
                
                if choice == '1':
                    self.setup_game(1)
                    self.play_game()
                elif choice == '2':
                    self.setup_game(2)
                    self.play_game()
                elif choice == '3':
                    self.setup_game(3)
                    self.play_game()
                elif choice == '4':
                    self.setup_game(4)
                    self.play_game()
                elif choice == '5':
                    self.show_rules()
                elif choice == '6':
                    print("Thanks for playing! Goodbye! 👋")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-6.")
                
                # Reset for new game
                self.board = ChessBoard()
                self.human_color = None
                self.bot = None
                self.game_mode = None
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except EOFError:
                print("\n\nGoodbye! 👋")
                break

if __name__ == "__main__":
    game = ChessGame()
    game.run()
