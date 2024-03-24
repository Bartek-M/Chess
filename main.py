import sys
import pygame

from game.drawing import Drawing
from game.events import click, drag
from public.board import Board


pygame.init()

PAD_X, PAD_Y = (60, 80)  # Dynamic, but suggested (40, 80) as minimum
WIDTH, HEIGHT = (640 + PAD_X * 2, 640 + PAD_Y * 2 + 20)

TILE_SIZE = (WIDTH - PAD_X * 2) // 8
FPS = 60


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
                click(pygame.mouse.get_pos(), board, (PAD_X, PAD_Y), TILE_SIZE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag(pygame.mouse.get_pos(), board, (PAD_X, PAD_Y), TILE_SIZE)

        drawing.update()

        if board.current and board.current.dragged:
            drawing.draw()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
