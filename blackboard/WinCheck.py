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
