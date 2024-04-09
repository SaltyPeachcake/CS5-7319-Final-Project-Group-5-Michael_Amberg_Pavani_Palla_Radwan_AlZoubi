from Connector import Message, Connector


class PlayerManagerComponent:
    def __init__(self, connector):
        self.connector = connector
        self.player_types = {1: 'human', 2: 'human'}
        self.player_tokens = {1: 'red', 2: 'yellow'}
        connector.subscribe(self)

    def receive(self, message):
        if message.type == "SwitchPlayer":
            self.switch_turns(message.data)

    def switch_turns(self, player):
        player = 3 - player
        self.connector.publish(Message(self, "PlayerSwitched", player))
