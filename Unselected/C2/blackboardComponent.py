from Connector import Message, Connector


class BlackboardComponent:
    def __init__(self, connector):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.connector = connector
        connector.subscribe(self)

    def receive(self, message):
        if message.type == "MoveMade":
            self.process_move(message.data)


    def process_move(self, column):
        # Logic to process the move based on the message data
        pass  # Implement move processing logic here

    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2
        self.connector.publish(Message(self, "PlayerSwitched"))
