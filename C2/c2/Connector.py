class Connector:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, component):
        self.subscribers.append(component)

    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)


class Message:
    def __init__(self, sender, type, data=None):
        self.sender = sender
        self.type = type
        self.data = data
