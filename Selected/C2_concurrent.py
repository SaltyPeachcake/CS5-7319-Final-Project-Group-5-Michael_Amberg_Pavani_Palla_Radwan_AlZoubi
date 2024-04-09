import copy
import random
import tkinter as tk

class Connector:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, component):
        self.subscribers.append(component)

    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)


class Message:
    def __init__(self, sender, type, data=None):
        self.sender = sender
        self.type = type
        self.data = data


class BlackboardComponent:
    def __init__(self, connector):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.connector = connector
        connector.subscribe(self)


class AlphaBeta:
    def __init__(self, connector, depth=2):
        self.depth = depth
        self.connector = connector
        self.connector.subscribe(self)

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
            return False  # Placeholder for terminal state check

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
                # Implement scoring for win/lose/draw
                pass  # Placeholder for terminal score
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

    def find_best_move(self, board):
        self.player_num = 2
        self.opponent_num = 1
        best_score = float("-inf")
        best_col = None

        for col in self.get_valid_moves(board):
            temp_board = copy.deepcopy(board)  # Ensure we don't modify the original board
            temp_board = self.simulate_move(temp_board, col, self.player_num)
            score = self.alphabeta(temp_board, self.depth - 1, float("-inf"), float("inf"), False)
            if score > best_score:
                best_score = score
                best_col = col

        # Instead of returning, it should now send a message with the best move
        # Assuming a global or passed-in connector object for message passing
        self.connector.publish(Message(self, "AIMoveChosen", best_col))

    def receive(self, message):
        if message.type == "Alpha-Beta Pruning AI":
            self.find_best_move(message.data)


class MonteCarlo:
    def __init__(self, connector, simulations_per_move=100):
        self.connector = connector
        self.simulations_per_move = simulations_per_move
        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "Monte Carlo AI":
            board = message.data
            self.find_best_move(board)

    def simulate_move(self, board, column, player):
        for row in reversed(range(6)):
            if board[row][column] == 0:
                board[row][column] = player
                return row, column
        return None

    def simulate_random_playouts(self, board, player):
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

    def find_best_move(self, board):
        player = 2 # AI will always be player 2

        move_wins = [0] * 7
        available_moves = [c for c in range(7) if board[0][c] == 0]

        for move in available_moves:
            for _ in range(self.simulations_per_move):
                board_copy = copy.deepcopy(board)
                self.simulate_move(board_copy, move, player)
                winner = self.simulate_random_playouts(board_copy, 3 - player)
                if winner == player:
                    move_wins[move] += 1

        best_move = max(range(7), key=lambda m: move_wins[m])

        self.connector.publish(Message(self, "AIMoveChosen", best_move))

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


class MoveProcessor:
    def __init__(self, connector, move_validator):
        self.connector = connector
        self.move_validator = move_validator  # Assuming move_validator is now also a messaging component
        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "ProcessMove":
            board, column, current_player = message.data
            # Validate move first
            if not self.move_validator.is_move_valid(board, column):
                print(f"Move to column {column} is invalid.")
                self.connector.publish(Message(self, "MoveProcessed", (column, False)))
                return

            # Process the valid move
            for row in reversed(range(6)):
                if board[row][column] == 0:
                    board[row][column] = current_player
                    # Notify the system that a move has been processed successfully
                    self.connector.publish(Message(self, "MoveProcessed", (column, True, board)))
                    break


class MoveValidator:
    def __init__(self, connector):
        self.connector = connector
        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "ValidateMove":
            board, column = message.data
            is_valid = self.is_move_valid(board, column)
            # Respond with a validation result message
            self.connector.publish(Message(self, "MoveValidationResult", (column, is_valid)))

    def is_move_valid(self, board, column):
        if column < 0 or column >= len(board[0]):
            return False

        for row in range(len(board) - 1, -1, -1):
            if board[row][column] == 0:
                return True

        return False


class WinChecker:
    def __init__(self, connector):
        self.connector = connector
        # Subscribe to relevant messages, such as requests to check for a winner
        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "CheckForWinner":
            board = message.data  # Assuming the message contains the current board state
            winner = self.check_winner(board)
            # Respond with a message indicating the check's outcome
            self.connector.publish(Message(self, "WinnerCheckResult", winner))

    def check_winner(self, board):
        for row in range(6):
            for col in range(7):
                player = board[row][col]
                if player == 0:
                    continue

                if col + 3 < 7 and all(board[row][col + i] == player for i in range(4)):
                    return player

                if row + 3 < 6 and all(board[row + i][col] == player for i in range(4)):
                    return player

                if row + 3 < 6 and col + 3 < 7 and all(board[row + i][col + i] == player for i in range(4)):
                    return player

                if row - 3 >= 0 and col + 3 < 7 and all(board[row - i][col + i] == player for i in range(4)):
                    return player

        return None  # No winner found


class PlayerManagerComponent:
    def __init__(self, connector):
        self.connector = connector
        self.player_types = {1: 'human', 2: 'human'}
        self.player_tokens = {1: 'red', 2: 'yellow'}
        connector.subscribe(self)

    def receive(self, message):
        if message.type == "SwitchPlayer":
            self.switch_turns(message.data)

    def switch_turns(self, player):
        player = 3 - player
        self.connector.publish(Message(self, "PlayerSwitched", player))



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

        #self.blackboard = BlackboardComponent(self.connector)
        self.PM = PlayerManagerComponent(self.connector)

        self.MC = MonteCarlo(self.connector)
        self.AB = AlphaBeta(self.connector)

        self.validate = MoveValidator(self.connector)
        self.move = MoveProcessor(self.connector, self.validate)
        self.wincheck = WinChecker(self.connector)

        self.connector.subscribe(self)

    def receive(self, message):
        if message.type == "StartGame":
            self.handle_start_game(message.data)
        elif message.type == "BoardClick":
            self.handle_board_click(message.data)
        elif message.type == "MoveProcessed":
            self.switch_logic(message.data)
        elif message.type == "RestartGame":
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

