import sys
import pygame

from drawing import Drawing
from board import Board


pygame.init()

PAD_X, PAD_Y = (60, 80)  # Dynamic, but suggested (40, 80) as minimum
WIDTH, HEIGHT = (640 + PAD_X * 2, 640 + PAD_Y * 2 + 20)

TILE_SIZE = (WIDTH - PAD_X * 2) // 8
FPS = 60


def click(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos
    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

    if not (0 <= x < 8 and 0 <= y < 8):
        return board.reset_selected()

    if board.current:
        if (x, y) in board.valid_moves:
            return board.move(board.current, (x, y))

        piece = board.board[y][x]
        board.current.dragged = False

        if board.current.first_select or piece != board.current:
            board.current.first_select = False
            return

    board.reset_selected()


def drag(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos
    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

    if not (0 <= x < 8 and 0 <= y < 8):
        return board.reset_selected()

    piece = board.board[y][x]

    if not piece or piece.dragged:
        return

    if piece != board.current:
        board.reset_selected()

    if not board.current:
        board.select(piece)
        piece.first_select = True

    piece.dragged = True


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(TILE_SIZE, (PAD_X, PAD_Y))
    drawing = Drawing(WIDTH, HEIGHT, (PAD_X, PAD_Y), board)

    pygame.display.set_caption(f"Chess Game")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                click(pygame.mouse.get_pos(), board)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag(pygame.mouse.get_pos(), board)

        drawing.update()

        if board.current and board.current.dragged:
            drawing.draw()

    pygame.quit()
    sys.exit(0)
