from Connector import Message, Connector
import copy
import random


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

