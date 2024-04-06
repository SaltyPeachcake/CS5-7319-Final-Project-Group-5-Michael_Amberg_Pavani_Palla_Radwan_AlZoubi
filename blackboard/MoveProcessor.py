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

        #self.blackboard.switch_player()
        return True
