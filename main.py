import sys
import pygame

pygame.init()

from game.drawing import Drawing
from game.events import click, drag
from public.board import Board

FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(FPS)
    drawing = Drawing(board)

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

        drawing.draw()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
