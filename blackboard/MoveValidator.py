class MoveValidator:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def is_move_valid(self, column, row):
        # Check if the column or row is within the valid range
        if column < 0 or column >= len(self.blackboard.board[0]):
            return False
        if row < 0 or row >= len(self.blackboard.board[1]):
            return False
        # Check if the position is 0 and thus open
        return self.blackboard.board[row][column] == 0

