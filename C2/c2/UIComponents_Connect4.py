import tkinter as tk
from Connector import Message, Connector
import blackboardComponent
import PlayerManagerComponent
import MoveComponents
import AiComponents


class StartMenuComponent:
    def __init__(self, connector, parent):
        self.connector = connector
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.opponent_var = tk.StringVar(value="Monte Carlo AI")

        # Initialize UI components
        self.initialize_ui()

    def initialize_ui(self):
        self.frame.pack(padx=30, pady=30)

        # Title setup
        title_frame = tk.Frame(self.frame)
        title_frame.pack(pady=20)
        title_connect = tk.Label(title_frame, text="Connect", fg="red", font=("Helvetica", 24, "bold"))
        title_connect.pack(side=tk.LEFT)
        title_four = tk.Label(title_frame, text="-4", fg="yellow", font=("Helvetica", 24, "bold"))
        title_four.pack(side=tk.LEFT)

        # Opponent selection setup
        label = tk.Label(self.frame, text="Choose your opponent:", font=("Helvetica", 14))
        label.pack(pady=20)
        radio_frame = tk.Frame(self.frame)
        radio_frame.pack(pady=10)
        for opponent in ["Monte Carlo AI", "Alpha-Beta Pruning AI", "Player 2"]:
            radio_button = tk.Radiobutton(radio_frame, text=opponent, variable=self.opponent_var, value=opponent,
                                          font=("Helvetica", 12))
            radio_button.pack(anchor=tk.W, pady=5)

        # Start game button setup
        start_button = tk.Button(self.frame, text="Start Game", font=("Helvetica", 14), command=self.on_start)
        start_button.pack(pady=20)

    def on_start(self):
        # When the start game button is clicked, publish a StartGame message
        chosen_opponent = self.opponent_var.get()
        self.connector.publish(Message(self, "StartGame", chosen_opponent))

    def show(self):
        # Show or pack the frame
        self.frame.pack(padx=30, pady=30)

    def hide(self):
        # Hide or unpack the frame
        self.frame.pack_forget()


class GameBoardComponent:
    def __init__(self, connector, parent, opponent):
        self.connector = connector
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.canvas = tk.Canvas(self.frame, bg='blue', height=360, width=420)
        self.canvas.pack(side=tk.LEFT, padx=(10, 0))
        self.connector.subscribe(self)  # Listen for messages
        self.opponent = opponent
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.canvas.bind("<Button-1>", self.on_board_click)

        self.draw_board()
        self.create_widgets()
        self.frame.pack()

    def receive(self, message):
        if message.type == "UpdateBoard":
            self.board = message.data  # Assuming message.data is the new board state
            self.draw_board()

    def on_board_click(self, event):
        column = event.x // 60
        self.connector.publish(Message(self, "BoardClick", column))

    def draw_board(self):
        self.canvas.delete("all")  # Clear the canvas to redraw
        rows, cols = 6, 7
        cell_size = 60  # Cell size for each spot on the board
        for row in range(rows):
            for col in range(cols):
                x0, y0 = col * cell_size, row * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='blue')
                if self.board[row][col] == 0:
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="white", outline="blue")
                elif self.board[row][col] == 1:  # Adjust colors as needed
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="yellow")
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red")

    def create_widgets(self):
        self.new_game_button = tk.Button(self.frame, text="New Game",
                                         command=lambda: self.connector.publish(Message(self, "StartNewGame")))
        self.new_game_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.restart_button = tk.Button(self.frame, text="Restart Game",
                                        command=lambda: self.connector.publish(Message(self, "RestartGame")))
        self.restart_button.pack(side=tk.RIGHT, padx=(10, 0))

    def ai_make_move(self):
        self.connector.publish(Message(self, self.opponent, self.board))

    def restart_game(self):
        self.connector.publish(Message(self, "RestartGame"))

    def start_new(self):
        self.connector.publish(Message(self, "StartNewGame"))

    def show(self):
        self.frame.pack(padx=500, pady=500)  # Adjust padding as needed

    def hide(self):
        self.frame.pack_forget()


class WinnerDisplayComponent:
    def __init__(self, connector, parent):
        self.connector = connector
        self.parent = parent
        self.frame = tk.Frame(parent)  # Main frame for the winner display
        self.label = tk.Label(self.frame, font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Buttons for "Start New Game" and "Replay"
        self.new_game_button = tk.Button(self.frame, text="Start New Game", command=self.start_new_game)
        self.replay_button = tk.Button(self.frame, text="Replay", command=self.replay_game)

        self.connector.subscribe(self)

        self.hide()  # Initially hide the component

    def receive(self, message):
        if message.type == "ShowWinner":
            self.show_winner(message.data)

    def show_winner(self, winner):
        if winner == 1 or winner == 2:
            winner_text = f"Player {winner} wins!"

            self.label.config(text=winner_text)

            self.new_game_button.pack(side=tk.LEFT, padx=10)
            self.replay_button.pack(side=tk.RIGHT, padx=10)

            self.show()

    def start_new_game(self):
        self.hide()  # Hide the winner display
        self.connector.publish(Message(self, "StartNewGame"))

    def replay_game(self):
        self.hide()  # Hide the winner display
        self.connector.publish(Message(self, "ReplayGame"))

    def show(self):
        self.frame.pack(padx=30, pady=30)

    def hide(self):
        self.frame.pack_forget()


class Connect4App:
    def __init__(self, root):
        self.root = root
        self.connector = Connector()
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1  # Player 1 starts
        self.opponent_type = None

        # Initialize components
        self.start_menu_component = StartMenuComponent(self.connector, root)
        self.game_board_component = None
        self.winner_display_component = WinnerDisplayComponent(self.connector, root)

        # Hide components that are not needed at start
        self.winner_display_component.hide()

        self.blackboard = blackboardComponent.BlackboardComponent(self.connector)
        self.PM = PlayerManagerComponent.PlayerManagerComponent(self.connector)

        self.MC = AiComponents.MonteCarlo(self.connector)
        self.AB = AiComponents.AlphaBeta(self.connector)

        self.validate = MoveComponents.MoveValidator(self.connector)
        self.move = MoveComponents.MoveProcessor(self.connector, self.validate)
        self.wincheck = MoveComponents.WinChecker(self.connector)

        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "StartGame":
            self.handle_start_game(message.data)
        elif message.type == "BoardClick":
            self.handle_board_click(message.data)
        elif message.type == "MoveProcessed":
            self.switch_logic(message.data)
        elif message.type == "RestartGame" or message.type == "StartNewGame":
            self.handle_game_reset()
        elif message.type == "WinnerCheckResult":
            self.handle_winner_check_result(message.data)
        elif message.type == "AIMoveChosen":
            self.ai_move(message.data)
        elif message.type == "StartNewGame":
            self.handle_newgame()
        elif message.type == "PlayerSwitched":
            self.switch_player(message.data)

    def handle_start_game(self, opponent_type):
        self.opponent_type = opponent_type
        self.start_menu_component.hide()
        self.game_board_component = GameBoardComponent(self.connector, self.root, opponent_type)

    def handle_board_click(self, column):
        if self.current_player == 2 and self.opponent_type != "Player 2":
            return

        self.connector.publish(Message(self, "ProcessMove", (self.board, column, self.current_player)))

    def handle_newgame(self):
        # Reset game state as necessary
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1  # Reset to player 1 starts
        self.opponent_type = None  # Reset opponent type

        # Hide game board and winner display, and show start menu
        if self.game_board_component:
            self.game_board_component.frame.pack_forget()  # Hide the game board
        self.winner_display_component.hide()
        self.start_menu_component.show()
        self.game_board_component.hide()

    def ai_move(self, data):
        column = data
        self.connector.publish(Message(self, "ProcessMove", (self.board, column, 2)))
        self.current_player = 1  # Switch back to the human player
        self.connector.publish(Message(self, "UpdateBoard", self.board))  # Update the board state
        self.connector.publish(Message(self, "CheckForWinner", self.board))  # Check for a winner

    def switch_logic(self, data):
        column, valid, game = data
        if valid:
            self.board = game
            self.connector.publish(Message(self, "SwitchPlayer", self.current_player))
            self.connector.publish(Message(self, "UpdateBoard", self.board))

            if self.current_player == 2 and self.opponent_type != "Player 2":
                self.connector.publish(Message(self, self.opponent_type, self.board))

            self.connector.publish(Message(self, "CheckForWinner", self.board))

    def switch_player(self, data):
        self.current_player = data

    def handle_game_reset(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.connector.publish(Message(self, "UpdateBoard", self.board))


    def handle_winner_check_result(self, winner):
        if winner == 0:
            return
        self.winner_display_component.show_winner(winner)

    def run(self):
        self.start_menu_component.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4App(root)
    app.run()
    root.mainloop()