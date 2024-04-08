from Connector import Message


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



