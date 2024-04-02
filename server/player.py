class Player:
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr

        self.name = None
        self.code = None

    def set_data(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"Player({self.addr}, {self.name})"
