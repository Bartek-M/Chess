import pygame

SCALE_SIZE = 96

white_assets = list(
    map(
        lambda img: pygame.transform.smoothscale(img, (SCALE_SIZE, SCALE_SIZE)),
        [
            pygame.image.load("./assets/wk.png"),
            pygame.image.load("./assets/wq.png"),
            pygame.image.load("./assets/wb.png"),
            pygame.image.load("./assets/wn.png"),
            pygame.image.load("./assets/wr.png"),
            pygame.image.load("./assets/wp.png"),
        ],
    )
)

black_assets = list(
    map(
        lambda img: pygame.transform.smoothscale(img, (SCALE_SIZE, SCALE_SIZE)),
        [
            pygame.image.load("./assets/bk.png"),
            pygame.image.load("./assets/bq.png"),
            pygame.image.load("./assets/bb.png"),
            pygame.image.load("./assets/bn.png"),
            pygame.image.load("./assets/br.png"),
            pygame.image.load("./assets/bp.png"),
        ],
    )
)


class Piece:
    """
    Chess piece representation
    """

    def __init__(self, row, col, color):
        self.row = row
        self.col = col

        self.color = color  # w | b
        self.selected = False

    def draw(self, win):
        x = SCALE_SIZE * self.col
        y = SCALE_SIZE * self.row

        win.blit(self.img, (x, y))

    def set_pos(self, pos):
        self.row, self.col = pos


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[0] if self.color == "w" else black_assets[0]

    def __repr__(self):
        return f"king {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Queen(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[1] if self.color == "w" else black_assets[1]

    def __repr__(self):
        return f"queen {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[2] if self.color == "w" else black_assets[2]

    def __repr__(self):
        return f"bishop {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[3] if self.color == "w" else black_assets[3]

    def __repr__(self):
        return f"knight {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[4] if self.color == "w" else black_assets[4]

    def __repr__(self):
        return f"rook {self.color} at [{self.row}; {self.col}]; {self.selected}"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = white_assets[5] if self.color == "w" else black_assets[5]

    def __repr__(self):
        return f"pawn {self.color} at [{self.row}; {self.col}]; {self.selected}"
