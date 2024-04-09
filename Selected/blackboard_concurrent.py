import tkinter as tk
import random
import copy
import threading


# NOTE - This is the exact same as the blackboard in the Selected folder. However, all the classes are instead located
# in one script so that it can be run from the command line

class Blackboard:
    def __init__(self):
        # Initialize the board with a 6x7 grid filled with 0s.
        # 0 represents empty, 1 and 2 represent player 1 and 2's tokens.
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.opponent_type = 'Alpha-Beta Pruning AI'
        self.lock = threading.Lock()


class AlphaBeta:
    def __init__(self, blackboard, depth=2):
        self.blackboard = blackboard
        self.depth = depth
        self.player_num = blackboard.current_player
        self.opponent_num = 2 if self.player_num == 1 else 1

    def check_winner_ABP(self, board):
        # Loop through all positions on the board
        for row in range(6):
            for col in range(7):
                player = board[row][col]
                if player == 0:
                    continue  # Skip if the slot is empty

                # Horizontal check (rightwards)
                if col + 3 < 7 and all(board[row][col + i] == player for i in range(4)):
                    return player

                # Vertical check (downwards)
                if row + 3 < 6 and all(board[row + i][col] == player for i in range(4)):
                    return player

                # Diagonal check (down-right)
                if row + 3 < 6 and col + 3 < 7 and all(board[row + i][col + i] == player for i in range(4)):
                    return player

                # Diagonal check (up-right)
                if row - 3 >= 0 and col + 3 < 7 and all(board[row - i][col + i] == player for i in range(4)):
                    return player

        # If no winner is found
        return None

    def evaluate_window(self, window, player, opp):
        score = 0
        if window.count(player) == 4:
            score += 1000
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opp) == 3 and window.count(0) == 1:
            score -= 4
        return score

    def heuristic(self, board):
        score = 0
        player = 2  # AI will always be player #2
        opp = 1  # Opponent

        # Score center column
        center_array = [row[3] for row in board]  # Extract the center column values
        center_count = center_array.count(player)
        score += center_count * 3

        # Score Horizontal
        for r in range(6):  # Assuming 6 rows
            for c in range(7 - 3):  # Allows checking for horizontal sequences within bounds
                window = [board[r][c + i] for i in range(4)]
                score += self.evaluate_window(window, player, opp)

        # Score Vertical
        for c in range(7):  # Assuming 7 columns
            for r in range(6 - 3):  # Allows checking for vertical sequences within bounds
                window = [board[r + i][c] for i in range(4)]
                score += self.evaluate_window(window, player, opp)

        # Score positive sloped diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player, opp)

        # Score negative sloped diagonal
        for r in range(3, 6):
            for c in range(7 - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player, opp)

        return score

    def is_terminal_node(self, board):
        if self.check_winner_ABP(board) is not None:
            return True
        else:
            return False

    def get_valid_moves(self, board):
        return [col for col in range(7) if board[0][col] == 0]  # Assuming a column is playable if the top is empty

    def simulate_move(self, board, column, player):
        temp_board = [row[:] for row in board]  # Make a copy of the board
        for row in reversed(range(6)):  # Assuming 6 rows
            if temp_board[row][column] == 0:
                temp_board[row][column] = player
                return temp_board
        return board  # Should never reach here if move is valid

    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        valid_moves = self.get_valid_moves(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                # Still need to implement scoring for win/lose/draw but it's working in current state
                pass
            else:
                return self.heuristic(board)

        if maximizingPlayer:
            value = float("-inf")
            for col in valid_moves:
                temp_board = self.simulate_move(board, col, self.player_num)
                value = max(value, self.alphabeta(temp_board, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            return value
        else:
            value = float("inf")
            for col in valid_moves:
                temp_board = self.simulate_move(board, col, self.opponent_num)
                value = min(value, self.alphabeta(temp_board, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff
            return value

    def find_best_move(self):
        best_score = float("-inf")
        best_col = None
        for col in self.get_valid_moves(self.blackboard.board):
            temp_board = self.simulate_move(self.blackboard.board, col, self.player_num)
            score = self.alphabeta(temp_board, self.depth - 1, float("-inf"), float("inf"), False)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col


class MonteCarlo:
    def __init__(self, blackboard, simulations_per_move=100):
        self.blackboard = blackboard
        self.simulations_per_move = simulations_per_move

    def simulate_move(self, board, column, player):
        """Simulate a move on the board without changing the original game state."""
        for row in reversed(range(6)):  # Assuming a 6-row board
            if board[row][column] == 0:
                board[row][column] = player
                return row, column
        return None

    def simulate_random_playouts(self, board, player):
        """Simulate random playouts from the current state to determine the game's outcome."""
        available_moves = [c for c in range(7) if board[0][c] == 0]
        while True:
            if not available_moves:
                return 0  # Draw
            move = random.choice(available_moves)
            move_result = self.simulate_move(board, move, player)
            if move_result is None:  # If the column was full, try another move
                available_moves.remove(move)
                continue
            row, col = move_result
            if self.check_winner(board, row, col, player):  # Check if this move wins the game
                return player
            player = 3 - player  # Switch player

    def find_best_move(self):
        """Find the best move using Monte Carlo simulation."""
        original_player = self.blackboard.current_player
        move_wins = [0] * 7  # Track wins for each column

        available_moves = [c for c in range(7) if self.blackboard.board[0][c] == 0]

        for move in available_moves:
            for _ in range(self.simulations_per_move):
                board_copy = copy.deepcopy(self.blackboard.board)
                self.simulate_move(board_copy, move, original_player)
                winner = self.simulate_random_playouts(board_copy, 3 - original_player)
                if winner == original_player:
                    move_wins[move] += 1

        # Select the move with the highest win count
        best_move = max(range(7), key=lambda m: move_wins[m])
        return best_move

    def check_winner(self, board, row, col, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal Down, Diagonal Up
        for d in directions:
            count = 1  # Include the current token
            # Check one direction
            for i in range(1, 4):
                r = row + d[0] * i
                c = col + d[1] * i
                if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]) or board[r][c] != player:
                    break
                count += 1
            # Check the opposite direction
            for i in range(1, 4):
                r = row - d[0] * i
                c = col - d[1] * i
                if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]) or board[r][c] != player:
                    break
                count += 1
            # Check if player won
            if count >= 4:
                return True
        return False


class WinChecker:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def check_winner(self):
        board = self.blackboard.board
        # Loop through all positions on the board
        for row in range(6):
            for col in range(7):
                player = board[row][col]
                if player == 0:
                    continue  # Skip if the slot is empty

                # Horizontal check (rightwards)
                if col + 3 < 7 and all(board[row][col + i] == player for i in range(4)):
                    return player

                # Vertical check (downwards)
                if row + 3 < 6 and all(board[row + i][col] == player for i in range(4)):
                    return player

                # Diagonal check (down-right)
                if row + 3 < 6 and col + 3 < 7 and all(board[row + i][col + i] == player for i in range(4)):
                    return player

                # Diagonal check (up-right)
                if row - 3 >= 0 and col + 3 < 7 and all(board[row - i][col + i] == player for i in range(4)):
                    return player

        # If no winner is found
        return None


class MoveProcessor:
    def __init__(self, blackboard, move_validator):
        self.blackboard = blackboard
        self.move_validator = move_validator

    def process_move(self, column):
        # Check if the move is valid
        if not self.move_validator.is_move_valid(column):
            print(f"Move to column {column} is invalid.")
            return False

        # Find the first available row from the bottom
        for row in reversed(range(6)):  # Assuming a 6-row Connect 4 board
            if self.blackboard.board[row][column] == 0:  # If the slot is empty
                self.blackboard.board[row][column] = self.blackboard.current_player  # Place the current player's token
                break

        # self.blackboard.switch_player()
        return True


class MoveValidator:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def is_move_valid(self, column):
        # Check if the column is within the valid range
        if column < 0 or column >= len(self.blackboard.board[0]):
            return False

        # Check if there is any open position in the column
        for row in range(len(self.blackboard.board) - 1, -1, -1):  # Start from the bottom row
            if self.blackboard.board[row][column] == 0:
                return True  # Found an open position

        return False  # No open positions in this column


class PlayerManager:
    def __init__(self, blackboard):
        self.blackboard = blackboard
        # Initialize players. 'human' for real players, 'ai' for computer players. Default is two human players.
        self.player_types = {1: 'human', 2: 'human'}
        # Initialize player tokens. Player 1 is red, Player 2 is yellow.
        self.player_tokens = {1: 'red', 2: 'yellow'}

    def switch_turns(self):
        self.blackboard.current_player = 1 if self.blackboard.current_player == 2 else 2


class StartMenu(tk.Frame):
    def __init__(self, parent, start_game_callback):
        super().__init__(parent)
        self.parent = parent
        self.start_game_callback = start_game_callback

        # Increased padding for overall layout
        self.pack(padx=30, pady=30)

        # Title with specified color scheme and larger font
        self.title_frame = tk.Frame(self)
        self.title_frame.pack(pady=20)  # Increased padding around the title

        self.title_connect = tk.Label(self.title_frame, text="Connect", fg="red", font=("Helvetica", 24, "bold"))
        self.title_connect.pack(side=tk.LEFT)

        self.title_four = tk.Label(self.title_frame, text="-4", fg="yellow", font=("Helvetica", 24, "bold"))
        self.title_four.pack(side=tk.LEFT)

        # Opponent selection with larger radio buttons
        self.label = tk.Label(self, text="Choose your opponent:", font=("Helvetica", 14))
        self.label.pack(pady=20)  # Increased padding for visual separation

        self.opponent_var = tk.StringVar(value="Monte Carlo AI")  # Default selection
        self.opponents = ["Monte Carlo AI", "Alpha-Beta Pruning AI", "Player 2"]

        self.radio_frame = tk.Frame(self)
        self.radio_frame.pack(pady=10)  # Adjusted padding for the radio button frame
        for opponent in self.opponents:
            radio_button = tk.Radiobutton(self.radio_frame, text=opponent, variable=self.opponent_var, value=opponent,
                                          font=("Helvetica", 12))
            radio_button.pack(anchor=tk.W, pady=5)  # Increased padding for each radio button

        # Larger start button
        self.start_button = tk.Button(self, text="Start Game", font=("Helvetica", 14), command=self.on_start)
        self.start_button.pack(pady=20)  # Increased padding below the button

    def on_start(self):
        chosen_opponent = self.opponent_var.get()
        self.start_game_callback(chosen_opponent)


class GameBoard(tk.Canvas):
    def __init__(self, parent, blackboard, start_new_game_callback, restart_game_callback, app_ref):
        super().__init__(parent)
        self.blackboard = blackboard
        self.start_new_game_callback = start_new_game_callback
        self.restart_game_callback = restart_game_callback
        self.app_ref = app_ref  # Store the reference to the Connect4App instance
        self.create_widgets()

    def create_widgets(self):
        # Create a canvas for the board itself
        self.canvas = tk.Canvas(self, bg='blue', height=360, width=420)  # Adjust size as needed
        self.canvas.pack(side=tk.LEFT, padx=(10, 0))  # Padding to separate from buttons

        self.draw_board()

        # Create a frame on the right side for buttons
        self.right_side_frame = tk.Frame(self)
        self.right_side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10))

        # Start new game button
        self.new_game_button = tk.Button(self.right_side_frame, text="Start New Game", command=self.start_new)
        self.new_game_button.pack(pady=10)

        # Restart game button
        self.restart_button = tk.Button(self.right_side_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=10)

        # Player turn label
        self.player_turn_label = tk.Label(self, text="Yellow's turn")
        self.player_turn_label.pack(side=tk.BOTTOM, pady=(10, 10))

        # Binding the canvas click event
        self.canvas.bind("<Button-1>", self.on_board_click)

    def update_player_turn_label(self):
        # Assuming player 1 is "yellow" and player 2 is "red"
        player_color = "Yellow" if self.blackboard.current_player == 1 else "Red"
        self.player_turn_label.config(text=f"{player_color}'s turn")

    def draw_board(self):
        self.canvas.delete("token")  # Clear existing tokens before redrawing
        rows, cols = 6, 7
        cell_size = 60  # Assuming cell size to ensure circles fit well
        for row in range(rows):
            for col in range(cols):
                # Calculate the top-left and bottom-right coordinates for each cell
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                # Adjust the circle's position to be centered within the cell
                # by reducing the diameter slightly and offsetting it from the cell's edges
                self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="white", outline="blue", tags="token")

                # Drawing player tokens, if present
                if self.blackboard.board[row][col] == 1:
                    # Player 1's token (yellow)
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="yellow", tags="token")
                elif self.blackboard.board[row][col] == 2:
                    # Player 2's token (red)
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red", tags="token")
        # self.player_turn_label = tk.Label(self, text="Player "+str(self.blackboard.current_player)+"'s turn")

    def on_board_click(self, event):
        if self.blackboard.current_player == 2 and self.blackboard.opponent_type != "Player 2":
            return
        column = event.x // 60
        # print(f"Column clicked: {column}")
        MV = MoveValidator(self.blackboard)
        MP = MoveProcessor(self.blackboard, MV)
        PM = PlayerManager(self.blackboard)
        Win = WinChecker(self.blackboard)

        if MP.process_move(column):
            PM.switch_turns()
            self.draw_board()
            if self.blackboard.opponent_type != "Player 2":
                ai_move = self.ai_make_move()  # Get the AI's best move
                print(ai_move)
                if ai_move is not None:  # Ensure ai_make_move returned a valid move
                    MP.process_move(ai_move)  # Process the AI's move
                    PM.switch_turns()
                    self.draw_board()
        won = Win.check_winner()
        if won is not None:
            self.app_ref.show_winner(won)
        self.update_player_turn_label()

    def ai_make_move(self):
        if self.blackboard.opponent_type == "Monte Carlo AI":
            MC = MonteCarlo(self.blackboard)
            return MC.find_best_move()
        if self.blackboard.opponent_type == "Alpha-Beta Pruning AI":
            AB = AlphaBeta(self.blackboard)
            return AB.find_best_move()
        self.update_player_turn_label()

    def restart_game(self):
        self.restart_game_callback()

    def start_new(self):
        self.start_new_game_callback()


class WinnerDisplay(tk.Frame):
    def __init__(self, parent, winner, start_new_game_callback, replay_callback):
        super().__init__(parent, padx=30, pady=30)
        self.pack()

        winner_text = "Player 1 wins!" if winner == 1 else "Player 2 wins!" if winner == 2 else "It's a draw!"
        self.label = tk.Label(self, text=winner_text, font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.new_game_button = tk.Button(self, text="Start New Game", command=start_new_game_callback)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.replay_button = tk.Button(self, text="Replay", command=lambda: replay_callback())
        self.replay_button.pack(side=tk.RIGHT, padx=10)


class Connect4App:
    def __init__(self, root, blackboard):
        self.root = root
        self.start_menu = StartMenu(root, self.start_game)
        self.start_menu.pack()
        self.blackboard = blackboard

        self.game_board = None

    def start_game(self, opponent):
        # Hide or destroy the winner display if it exists
        if hasattr(self, 'winner_display') and self.winner_display:
            self.winner_display.pack_forget()  # or self.winner_display.destroy()

        if self.game_board:
            self.game_board.pack_forget()

        self.game_board = GameBoard(self.root, self.blackboard, self.start_new_game, self.restart_game, self)
        self.game_board.pack()
        self.start_menu.pack_forget()
        self.blackboard.opponent_type = opponent

    def show_winner(self, winner):
        # Hide the current game UI
        if self.game_board:
            self.game_board.pack_forget()

        # Create and show the winner UI
        self.winner_display = WinnerDisplay(self.root, winner, self.start_new_game, self.replay_game)

    def replay_game(self, winner=None):
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]
        self.start_game(self.blackboard.opponent_type)
        if self.winner_display:
            self.winner_display.pack_forget()

    def start_new_game(self):
        if hasattr(self, 'winner_display') and self.winner_display:
            self.winner_display.pack_forget()  # or self.winner_display.destroy()
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]
        self.game_board.pack_forget()
        self.start_menu.pack()

    def restart_game(self):
        self.blackboard.board = [[0 for _ in range(7)] for _ in range(6)]


if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4App(root, Blackboard())
    root.mainloop()
