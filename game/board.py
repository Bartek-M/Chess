import pygame

from pieces import King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    LIGHT_COLOR = 238, 238, 238
    DARK_COLOR = 136, 136, 136

    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.board = [[None for _ in range(8)] for _ in range(8)]

        for row in [0, 7]:
            color = "b" if row == 0 else "w"
            pawn_row = row + (-1 if row == 7 else 1)

            self.board[row][0] = Rook(row, 0, color)
            self.board[row][1] = Knight(row, 1, color)
            self.board[row][2] = Bishop(row, 2, color)
            self.board[row][3] = Queen(row, 3, color)
            self.board[row][4] = King(row, 4, color)
            self.board[row][5] = Bishop(row, 5, color)
            self.board[row][6] = Knight(row, 6, color)
            self.board[row][7] = Rook(row, 7, color)

            for col in range(8):
                self.board[pawn_row][col] = Pawn(pawn_row, col, color)

    def select(self):
        pass

    def move(self):
        pass

    def draw(self, win):
        for i in range(8):
            for j in range(8):
                color = self.LIGHT_COLOR if (i + j) % 2 == 0 else self.DARK_COLOR
                pygame.draw.rect(
                    win,
                    color,
                    (
                        j * self.tile_size,
                        i * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                )

        for row in self.board:
            for piece in row:
                if piece is None:
                    continue
                
                piece.draw(win)
