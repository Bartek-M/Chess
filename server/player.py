class Player:
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return f"Player({self.addr}, {self.name})"
