import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (720, 800)
PAD_X, PAD_Y = 40, 80

TILE_SIZE = (WIDTH - PAD_X * 2) // 8
FPS = 30


def click(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos

    if not (
        PAD_X <= mouse_x <= (WIDTH - PAD_X) and PAD_Y <= mouse_y <= (HEIGHT - PAD_Y)
    ):
        return

    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE
    piece = board.board[y][x]

    if (x, y) in board.valid_moves and board.current:
        board.move(board.current, (x, y))
    elif piece:
        board.select(piece)
    else:
        board.reset_selected()


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(TILE_SIZE, (PAD_X, PAD_Y))
    drawing = Drawing(WIDTH, HEIGHT, board)

    pygame.display.set_caption(f"Chess Game")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button != 1:
                    continue

                click(pygame.mouse.get_pos(), board)

        drawing.draw()

    pygame.quit()
