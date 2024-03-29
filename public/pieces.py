import pygame

from public.utils import is_avail


class Piece:
    """
    Chess piece representation
    """

    SELECT_COLOR = 56, 220, 255
    DRAGGED_COLOR = 255, 50, 50

    def __init__(self, row, col, color, img):
        self.row = row
        self.col = col

        self.color = color  # w | b
        self.img = img

        self.selected = False
        self.first_select = False
        self.dragged = False

        self.king = False
        self.rook = False
        self.pawn = False

    def draw(self, win, assets, tile_size, padding):
        x = self.col * tile_size + padding[0]
        y = self.row * tile_size + padding[1]

        if self.selected:
            pygame.draw.rect(win, self.SELECT_COLOR, (x, y, tile_size, tile_size), 5)

        if self.dragged:
            x, y = pygame.mouse.get_pos()

            bx = (x - padding[0]) // tile_size * tile_size + padding[0]
            by = (y - padding[1]) // tile_size * tile_size + padding[1]
            pygame.draw.rect(win, self.DRAGGED_COLOR, (bx, by, tile_size, tile_size), 5)

            x -= tile_size // 2
            y -= tile_size // 2

        win.blit(assets[self.img], (x, y))

    def set_pos(self, pos):
        self.col, self.row = pos


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.king = True
        self.moved = False

    def valid_moves(self, board):
        moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):
                    continue

                x = self.col + dx
                y = self.row + dy
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))

        if not self.moved:
            moves += self.check_castle(board)

        return moves

    def check_castle(self, board):
        moves = []

        for d in [-1, 1]:
            dx = 1

            while True:
                x = self.col + dx * d

                if not 0 <= x < 8:
                    break

                piece = board[self.row][x]

                if piece is None:
                    dx += 1
                    continue

                if piece.color == self.color and piece.rook and not piece.moved:
                    moves.append((piece.col, self.row))

                break

        return moves

    def __repr__(self):
        return f"king {self.color} at [{self.row}; {self.col}]"


class Queen(Piece):
    def valid_moves(self, board):
        moves = []

        # X / Y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))
                else:
                    break

                if avail:
                    break

        # DIAGONALS
        for dx, dy in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))
                else:
                    break

                if avail:
                    break

        return moves

    def __repr__(self):
        return f"queen {self.color} at [{self.row}; {self.col}]"


class Bishop(Piece):
    def valid_moves(self, board):
        moves = []

        for dx, dy in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))
                else:
                    break

                if avail:
                    break

        return moves

    def __repr__(self):
        return f"bishop {self.color} at [{self.row}; {self.col}]"


class Knight(Piece):
    def valid_moves(self, board):
        moves = []

        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if abs(dx) == abs(dy):
                    continue

                x = self.col + dx
                y = self.row + dy
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))

        return moves

    def __repr__(self):
        return f"knight {self.color} at [{self.row}; {self.col}]"


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rook = True
        self.moved = False

    def valid_moves(self, board):
        moves = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = is_avail(board, (x, y), self.color)

                if avail is not None:
                    moves.append((x, y))
                else:
                    break

                if avail:
                    break

        return moves

    def __repr__(self):
        return f"rook {self.color} at [{self.row}; {self.col}]"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pawn = True

    def valid_moves(self, board):
        moves = []
        d = 1 if board[-1] == self.color else -1

        if is_avail(board, (self.col, self.row - 1 * d), self.color) == False:
            moves.append((self.col, self.row - 1 * d))

            if (
                self.row == (6 if board[-1] == self.color else 1)
                and is_avail(board, (self.col, self.row - 2 * d), self.color) == False
            ):
                moves.append((self.col, self.row - 2 * d))

        if is_avail(board, (self.col - 1, self.row - 1 * d), self.color):
            moves.append((self.col - 1, self.row - 1 * d))

        if is_avail(board, (self.col + 1, self.row - 1 * d), self.color):
            moves.append((self.col + 1, self.row - 1 * d))

        return moves

    def __repr__(self):
        return f"pawn {self.color} at [{self.row}; {self.col}]"
