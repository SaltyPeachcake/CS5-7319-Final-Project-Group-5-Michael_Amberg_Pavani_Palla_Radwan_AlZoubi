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


