class PlayerManager:
    def __init__(self, blackboard):
        self.blackboard = blackboard
        # Initialize players. 'human' for real players, 'ai' for computer players. Default is two human players.
        self.player_types = {1: 'human', 2: 'human'}
        # Initialize player tokens. Player 1 is red, Player 2 is yellow.
        self.player_tokens = {1: 'red', 2: 'yellow'}

    def switch_turns(self):
        self.blackboard.current_player = 1 if self.current_player == 2 else 2


