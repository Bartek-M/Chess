import os
import pygame

from pieces import King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    LIGHT_COLOR = 238, 238, 238
    DARK_COLOR = 116, 116, 116

    GRAY_COLOR = 200, 200, 200
    RED_COLOR = 255, 50, 50

    def __init__(self, tile_size, padding):
        self.tile_size = tile_size
        self.pad_x, self.pad_y = padding

        self.load_assets()

        self.color = "w"
        self.board = self.generate_board()

        self.current = None
        self.valid_moves = []

    @staticmethod
    def generate_board():
        board = [[None for _ in range(8)] for _ in range(8)]

        for row in [0, 7]:
            color = "b" if row == 0 else "w"
            pawn_row = row + (-1 if row == 7 else 1)

            board[row][0] = Rook(row, 0, color, 4)
            board[row][1] = Knight(row, 1, color, 3)
            board[row][2] = Bishop(row, 2, color, 2)
            board[row][3] = Queen(row, 3, color, 1)
            board[row][4] = King(row, 4, color, 0)
            board[row][5] = Bishop(row, 5, color, 2)
            board[row][6] = Knight(row, 6, color, 3)
            board[row][7] = Rook(row, 7, color, 4)

            for col in range(8):
                board[pawn_row][col] = Pawn(pawn_row, col, color, 5)

        return board

    def draw(self, win):
        for i in range(8):
            for j in range(8):
                color = self.LIGHT_COLOR if (i + j) % 2 == 0 else self.DARK_COLOR
                x = self.pad_x + j * self.tile_size
                y = self.pad_y + i * self.tile_size

                pygame.draw.rect(win, color, (x, y, self.tile_size, self.tile_size))
                piece = self.board[i][j]

                if (j, i) in self.valid_moves:
                    color, radius, border = (
                        (self.GRAY_COLOR, 12, 0)
                        if piece is None
                        else (self.RED_COLOR, self.tile_size * 0.35, 5)
                    )

                    center_x = x + self.tile_size // 2
                    center_y = y + self.tile_size // 2

                    pygame.draw.circle(win, color, (center_x, center_y), radius, border)

                if piece is None:
                    continue

                assets = self.black_assets if piece.color == "b" else self.white_assets
                piece.draw(win, assets, self.tile_size, (self.pad_x, self.pad_y))

    def select(self, piece):
        if self.current:
            self.current.selected = False

        if piece.color != self.color:
            return self.reset_selected()

        if self.current == piece:
            return self.reset_selected()

        piece.selected = True
        self.current = piece
        self.valid_moves = piece.valid_moves(self.board)

    def reset_selected(self):
        if not self.current:
            return

        self.current.selected = False
        self.current = None
        self.valid_moves = []

    def move(self, piece, pos):
        x, y = pos

        self.board[piece.row][piece.col] = None
        self.select(piece)

        if y == 0 and piece.pawn:
            self.board[y][x] = Queen(y, x, piece.color, 1)
            del piece
            return

        self.board[y][x] = piece
        piece.set_pos((x, y))


    def load_assets(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.white_assets = list(
            map(
                lambda img: pygame.transform.smoothscale(
                    img, (self.tile_size, self.tile_size)
                ),
                [
                    pygame.image.load(os.path.join(current_dir, "assets", "wk.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "wq.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "wb.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "wn.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "wr.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "wp.png")),
                ],
            )
        )
        self.black_assets = list(
            map(
                lambda img: pygame.transform.smoothscale(
                    img, (self.tile_size, self.tile_size)
                ),
                [
                    pygame.image.load(os.path.join(current_dir, "assets", "bk.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "bq.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "bb.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "bn.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "br.png")),
                    pygame.image.load(os.path.join(current_dir, "assets", "bp.png")),
                ],
            )
        )
