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
        else: return False

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
