import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (592, 592)
PADDING = 40
TILE_SIZE = (WIDTH - PADDING * 2) // 8


FPS = 30


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(TILE_SIZE, PADDING)
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

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if not (PADDING <= mouse_x <= (WIDTH - PADDING)):
                    continue

                if not (PADDING <= mouse_y <= (HEIGHT - PADDING)):
                    continue

                x, y = (mouse_x - PADDING) // TILE_SIZE, (mouse_y - PADDING) // TILE_SIZE
                board.select(board.board[y][x])

        drawing.draw()

    pygame.quit()
