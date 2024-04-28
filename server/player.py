class Player:
    def __init__(self, client: object, addr: object) -> None:
        self.client = client
        self.addr = addr

        self.name = None
        self.code = None

    def set_data(self, name: str, code: str) -> None:
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"Player({self.addr}, {self.name})"
