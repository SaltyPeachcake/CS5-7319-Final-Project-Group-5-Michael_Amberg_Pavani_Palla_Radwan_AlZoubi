import random
import copy

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
