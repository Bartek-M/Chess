import os
import pygame


def generate_board(player_color):
    from .pieces import King, Queen, Bishop, Knight, Rook, Pawn

    board = [[None for _ in range(8)] for _ in range(8)]

    for row in [0, 7]:
        if player_color == "w":
            color = "b" if row == 0 else "w"
            king_col, queen_col = 4, 3
        else:
            color = "b" if row == 7 else "w"
            king_col, queen_col = 3, 4

        pawn_row = row + (-1 if row == 7 else 1)

        board[row][0] = Rook(row, 0, color, 4)
        board[row][1] = Knight(row, 1, color, 3)
        board[row][2] = Bishop(row, 2, color, 2)
        board[row][queen_col] = Queen(row, queen_col, color, 1)
        board[row][king_col] = King(row, king_col, color, 0)
        board[row][5] = Bishop(row, 5, color, 2)
        board[row][6] = Knight(row, 6, color, 3)
        board[row][7] = Rook(row, 7, color, 4)

        for col in range(8):
            board[pawn_row][col] = Pawn(pawn_row, col, color, 5)

    board.append(player_color)
    return board


def is_avail(board, pos, color):
    x, y = pos

    if not (0 <= x < 8 and 0 <= y < 8):
        return None

    piece = board[y][x]

    if piece is None:
        return False

    if piece.color == color:
        return None

    return piece


def format_time(time):
    time = int(time)

    minute = str(time // 60)
    second = str(time % 60)

    while len(minute) < 2:
        minute = "0" + minute

    while len(second) < 2:
        second = "0" + second

    return f"{minute}:{second}"


def load_assets(tile_size):
    white_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
            [
                pygame.image.load(os.path.join("assets", "white", "wk.png")),
                pygame.image.load(os.path.join("assets", "white", "wq.png")),
                pygame.image.load(os.path.join("assets", "white", "wb.png")),
                pygame.image.load(os.path.join("assets", "white", "wn.png")),
                pygame.image.load(os.path.join("assets", "white", "wr.png")),
                pygame.image.load(os.path.join("assets", "white", "wp.png")),
            ],
        )
    )
    black_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
            [
                pygame.image.load(os.path.join("assets", "black", "bk.png")),
                pygame.image.load(os.path.join("assets", "black", "bq.png")),
                pygame.image.load(os.path.join("assets", "black", "bb.png")),
                pygame.image.load(os.path.join("assets", "black", "bn.png")),
                pygame.image.load(os.path.join("assets", "black", "br.png")),
                pygame.image.load(os.path.join("assets", "black", "bp.png")),
            ],
        )
    )

    return (white_assets, black_assets)
