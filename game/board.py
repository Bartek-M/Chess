import pygame

from pieces import King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    LIGHT_COLOR = 238, 238, 238
    DARK_COLOR = 116, 116, 116

    GRAY_COLOR = 200, 200, 200
    RED_COLOR = 255, 50, 50

    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.load_assets()

        self.color = "b"
        self.board = [[None for _ in range(8)] for _ in range(8)]

        for row in [0, 7]:
            color = "b" if row == 0 else "w"
            assets = self.black_assets if row == 0 else self.white_assets
            pawn_row = row + (-1 if row == 7 else 1)

            self.board[row][0] = Rook(row, 0, color, assets[4])
            self.board[row][1] = Knight(row, 1, color, assets[3])
            self.board[row][2] = Bishop(row, 2, color, assets[2])
            self.board[row][3] = Queen(row, 3, color, assets[1])
            self.board[row][4] = King(row, 4, color, assets[0])
            self.board[row][5] = Bishop(row, 5, color, assets[2])
            self.board[row][6] = Knight(row, 6, color, assets[3])
            self.board[row][7] = Rook(row, 7, color, assets[4])

            for col in range(8):
                self.board[pawn_row][col] = Pawn(pawn_row, col, color, assets[5])

        self.current = None
        self.valid_moves = []

    def draw(self, win):
        for i in range(8):
            for j in range(8):
                color = self.LIGHT_COLOR if (i + j) % 2 == 0 else self.DARK_COLOR
                x = j * self.tile_size
                y = i * self.tile_size

                pygame.draw.rect(win, color, (x, y, self.tile_size, self.tile_size))
                piece = self.board[i][j]

                if (i, j) in self.valid_moves:
                    color, radius, border = (
                        (self.GRAY_COLOR, 12, 0)
                        if piece is None
                        else (self.RED_COLOR, self.tile_size * 0.35, 5)
                    )

                    center_x = x + self.tile_size // 2
                    center_y = y + self.tile_size // 2

                    pygame.draw.circle(win, color, (center_x, center_y), radius, border)

                if piece is not None:
                    piece.draw(win, self.tile_size)

    def select(self, piece):
        if self.current:
            self.current.selected = False

        if self.current == piece:
            self.current = None
            self.valid_moves = []
            return

        piece.selected = True
        self.current = piece
        self.valid_moves = piece.valid_moves(self.board)

    def move(self):
        pass

    def load_assets(self):
        self.white_assets = list(
            map(
                lambda img: pygame.transform.smoothscale(
                    img, (self.tile_size, self.tile_size)
                ),
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
        self.black_assets = list(
            map(
                lambda img: pygame.transform.smoothscale(
                    img, (self.tile_size, self.tile_size)
                ),
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
