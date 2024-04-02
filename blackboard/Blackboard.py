class Blackboard:
    def __init__(self):
        # Initialize the board with a 6x7 grid filled with 0s.
        # 0 represents empty, 1 and 2 represent player 1 and 2's tokens.
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        # Initialize the current player. Player 1 will be yellow, and starts.
        self.current_player = 1
        # Initialize the opponent type. Can be 'monte_carlo', 'abp', or 'player2'.
        self.opponent_type = 'ABP'

    def set_opponent_type(self, opponent_type):
        assert opponent_type in ['monte_carlo', 'abp', 'player2']
        self.opponent_type = opponent_type

    def switch_player(self):
        # Switches the current player
        self.current_player = 1 if self.current_player == 2 else 2
