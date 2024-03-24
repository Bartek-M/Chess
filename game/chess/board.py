import os
import random

import pygame

from chess.pieces import Queen
from utils import generate_board, load_assets


class Board:
    LIGHT_COLOR = 238, 238, 238
    DARK_COLOR = 116, 116, 116

    GRAY_COLOR = 200, 200, 200
    GREEN_COLOR = 56, 220, 255
    RED_COLOR = 255, 50, 50

    def __init__(self, tile_size, padding):
        self.tile_size = tile_size
        self.pad_x, self.pad_y = padding

        self.white_assets, self.black_assets = load_assets(self.tile_size)

        self.color = random.choice(("w", "b"))
        self.board = generate_board(self.color)

        self.current = None
        self.valid_moves = []

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
                        else (
                            (
                                self.RED_COLOR
                                if piece.color != self.current.color
                                else self.GREEN_COLOR
                            ),
                            self.tile_size * 0.4,
                            5,
                        )
                    )

                    center_x = x + self.tile_size // 2
                    center_y = y + self.tile_size // 2

                    pygame.draw.circle(win, color, (center_x, center_y), radius, border)

                if piece is None or piece.dragged:
                    continue

                assets = self.black_assets if piece.color == "b" else self.white_assets
                piece.draw(win, assets, self.tile_size, (self.pad_x, self.pad_y))

        if self.current and self.current.dragged:
            assets = (
                self.black_assets if self.current.color == "b" else self.white_assets
            )
            self.current.draw(win, assets, self.tile_size, (self.pad_x, self.pad_y))

    def select(self, piece):
        if self.current:
            self.current.selected = False

        if self.current == piece:
            return self.reset_selected()

        piece.selected = True
        self.current = piece
        self.valid_moves = piece.valid_moves(self.board)

    def reset_selected(self):
        if not self.current:
            return

        self.current.selected = False
        self.current.first_select = False
        self.current.dragged = False

        self.current = None
        self.valid_moves = []

    def move(self, piece, pos):
        x, y = pos

        self.board[piece.row][piece.col] = None
        self.reset_selected()

        if y == 0 and piece.pawn:
            self.board[y][x] = Queen(y, x, piece.color, 1)
            del piece
            return

        if piece.king or piece.rook:
            piece.moved = True

        if piece.king and (new := self.board[y][x]) and new.rook:
            self.board[y][x] = None

            if x > piece.col:
                new_x = x - (3 if piece.col == 3 else 2)
                x = piece.col + 2
            else:
                new_x = x + (2 if piece.col == 3 else 3)
                x = piece.col - 2

            self.board[y][new_x] = new
            new.set_pos((new_x, y))

        self.board[y][x] = piece
        piece.set_pos((x, y))

    def draw_cords(self, win, font):
        nums = ["8", "7", "6", "5", "4", "3", "2", "1"]
        alph = ["a", "b", "c", "d", "e", "f", "g", "h"]

        if self.color == "b":
            nums = nums[::-1]
            alph = alph[::-1]

        for i in range(8):
            text = font.render(str(nums[i]), True, self.GRAY_COLOR)
            win.blit(
                text,
                (
                    self.pad_x - 20,
                    i * self.tile_size + (self.pad_y + self.tile_size // 2 - 10),
                ),
            )

        for i, l in enumerate(alph):
            text = font.render(l, True, self.GRAY_COLOR)
            win.blit(
                text,
                (
                    i * self.tile_size + (self.pad_x + self.tile_size // 2 - 5),
                    8 * self.tile_size + self.pad_y + 5,
                ),
            )
