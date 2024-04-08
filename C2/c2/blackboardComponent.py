from Connector import Message, Connector


class BlackboardComponent:
    def __init__(self, connector):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.connector = connector
        connector.subscribe(self)

