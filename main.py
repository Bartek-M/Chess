import sys
import pygame

from game.drawing import Drawing
from game.events import click, drag
from public.board import Board

pygame.init()
FPS = 60


def welcome():
    pass


def game(clock, fps):
    run = True
    board = Board()
    drawing = Drawing(board, fps)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    board.reset()

            if event.type == pygame.MOUSEBUTTONUP:
                click(pygame.mouse.get_pos(), board)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drag(pygame.mouse.get_pos(), board)

        drawing.draw()


def main():
    pygame.display.set_caption(f"Chess Game")
    clock = pygame.time.Clock()

    game(clock, FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
