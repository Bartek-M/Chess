import os
import pygame


def generate_board(player_color):
    from pieces import King, Queen, Bishop, Knight, Rook, Pawn
    board = [[None for _ in range(8)] for _ in range(8)]

    for row in [0, 7]:
        if player_color == "w":
            color = "b" if row == 0 else "w"
            k_pos, q_pos = 4, 3
        else:
            color = "b" if row == 7 else "w"
            k_pos, q_pos = 3, 4

        pawn_row = row + (-1 if row == 7 else 1)

        board[row][0] = Rook(row, 0, color, 4)
        board[row][1] = Knight(row, 1, color, 3)
        board[row][2] = Bishop(row, 2, color, 2)
        board[row][q_pos] = Queen(row, q_pos, color, 1)
        board[row][k_pos] = King(row, k_pos, color, 0)
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


def load_assets(tile_size):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    white_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
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
    black_assets = list(
        map(
            lambda img: pygame.transform.smoothscale(img, (tile_size, tile_size)),
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

    return (white_assets, black_assets)
