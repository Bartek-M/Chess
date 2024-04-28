import pygame


class Piece:
    """
    Chess piece representation
    """

    CYAN = 56, 220, 255
    RED = 255, 50, 50

    def __init__(self, board: object, row: int, col: int, color: str, img: int) -> None:
        self.board = board

        self.row = row
        self.col = col

        self.color = color  # w | b
        self.img = img

        self.selected = False
        self.first_select = False
        self.dragged = False
        self.valid_moves = [None]

        self.king = False
        self.rook = False
        self.pawn = False

    def draw(
        self, win: pygame.Surface, assets: tuple[list], tile_size: int, padding: int
    ) -> None:
        x = self.col * tile_size + padding[0]
        y = self.row * tile_size + padding[1]

        color = self.CYAN if self.color == "w" else self.RED

        if self.selected:
            pygame.draw.rect(win, color, (x, y, tile_size, tile_size), 4)

        if self.dragged:
            x, y = pygame.mouse.get_pos()
            bx, by = (x - padding[0]) // tile_size, (y - padding[1]) // tile_size

            if 0 <= bx < 8 and 0 <= by < 8:
                bx = bx * tile_size + padding[0]
                by = by * tile_size + padding[1]
                pygame.draw.rect(win, color, (bx, by, tile_size, tile_size), 4)

            x -= tile_size // 2
            y -= tile_size // 2

        win.blit(assets[self.img], (x, y))

    def set_pos(self, pos: list[int]) -> list[int]:
        self.col, self.row = pos
        return pos


class King(Piece):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.king = True
        self.moved = False

    def get_moves(self) -> None:
        moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx, dy) == (0, 0):
                    continue

                x = self.col + dx
                y = self.row + dy
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])

        if not self.moved:
            moves += self.check_castle()

        self.valid_moves = moves if moves else [None]

    def check_castle(self) -> list[list[int]]:
        moves = []

        for d in [-1, 1]:
            dx = 1

            while True:
                x = self.col + dx * d

                if not 0 <= x < 8:
                    break

                piece = self.board.board[self.row][x]

                if piece is None:
                    dx += 1
                    continue

                if piece.color == self.color and piece.rook and not piece.moved:
                    moves.append([piece.col, self.row])

                break

        return moves

    def is_attacked(self, board: list[list] = None, t_pos: list[int] = None) -> bool:
        board = board if board else self.board.board

        direction = 1 if self.board.color == self.color else -1
        row, col = t_pos if t_pos else (self.row, self.col)

        # X / Y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for d in range(1, 8):
                x = col + dx * d
                y = row + dy * d
                avail = self.board.is_avail((x, y), self, board)

                if type(avail) in [Queen, Rook]:
                    return True
                elif avail is None:
                    break

        # DIAGONALS
        for dx, dy in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for d in range(1, 8):
                x = col + dx * d
                y = row + dy * d
                avail = self.board.is_avail((x, y), self, board)

                if (
                    type(avail) == Pawn
                    and x in [col - 1, col + 1]
                    and y == row - 1 * direction
                ):
                    return True
                elif type(avail) in [Queen, Bishop]:
                    return True
                elif avail is None:
                    break

        # KNIGHT
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if abs(dx) == abs(dy):
                    continue

                x = col + dx
                y = row + dy
                avail = self.board.is_avail((x, y), self, board)

                if type(avail) == Knight:
                    return True
                elif avail is None:
                    break

        return False

    def __repr__(self) -> str:
        return f"king {self.color} at [{self.row}; {self.col}]"


class Queen(Piece):
    def get_moves(self) -> None:
        moves = []

        # X / Y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])
                else:
                    break

                if avail:
                    break

        # DIAGONALS
        for dx, dy in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])
                else:
                    break

                if avail:
                    break

        self.valid_moves = moves if moves else [None]

    def __repr__(self) -> str:
        return f"queen {self.color} at [{self.row}; {self.col}]"


class Bishop(Piece):
    def get_moves(self) -> None:
        moves = []

        for dx, dy in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])
                else:
                    break

                if avail:
                    break

        self.valid_moves = moves if moves else [None]

    def __repr__(self) -> str:
        return f"bishop {self.color} at [{self.row}; {self.col}]"


class Knight(Piece):
    def get_moves(self) -> None:
        moves = []

        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if abs(dx) == abs(dy):
                    continue

                x = self.col + dx
                y = self.row + dy
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])

        self.valid_moves = moves if moves else [None]

    def __repr__(self) -> str:
        return f"knight {self.color} at [{self.row}; {self.col}]"


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rook = True
        self.moved = False

    def get_moves(self) -> None:
        moves = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for d in range(1, 8):
                x = self.col + dx * d
                y = self.row + dy * d
                avail = self.board.is_avail((x, y), self)

                if avail == "king":
                    continue

                if avail is not None:
                    moves.append([x, y])
                else:
                    break

                if avail:
                    break

        self.valid_moves = moves if moves else [None]

    def __repr__(self) -> str:
        return f"rook {self.color} at [{self.row}; {self.col}]"


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pawn = True

    def get_moves(self) -> None:
        moves = []
        passed_pawn = self.board.passed_pawn
        d = 1 if self.board.color == self.color else -1

        if self.board.is_avail((self.col, self.row - 1 * d), self) == False:
            moves.append([self.col, self.row - 1 * d])

            if (
                self.row == (6 if self.board.color == self.color else 1)
                and self.board.is_avail((self.col, self.row - 2 * d), self) == False
            ):
                moves.append([self.col, self.row - 2 * d])

        if self.board.is_avail((self.col - 1, self.row - 1 * d), self) not in [
            None,
            False,
            "king",
        ]:
            moves.append([self.col - 1, self.row - 1 * d])

        if self.board.is_avail((self.col + 1, self.row - 1 * d), self) not in [
            None,
            False,
            "king",
        ]:
            moves.append([self.col + 1, self.row - 1 * d])

        if passed_pawn:
            if self.board.is_avail([self.col - 1, self.row], self) == passed_pawn:
                moves.append([self.col - 1, self.row - 1 * d])
            elif self.board.is_avail([self.col + 1, self.row], self) == passed_pawn:
                moves.append([self.col + 1, self.row - 1 * d])

        self.valid_moves = moves if moves else [None]

    def __repr__(self) -> str:
        return f"pawn {self.color} at [{self.row}; {self.col}]"
