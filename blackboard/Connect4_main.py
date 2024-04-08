import tkinter as tk
from Blackboard import Blackboard

from MoveProcessor import MoveProcessor
from MoveValidator import MoveValidator
from MonteCarlo import MonteCarlo
from AlphaBetaPrune import AlphaBeta
from WinCheck import WinChecker
from PlayerManager import PlayerManager


# The last 3 components are located within this file as their own class, separating them out was too difficult


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
        #self.player_turn_label = tk.Label(self, text="Player "+str(self.blackboard.current_player)+"'s turn")

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
