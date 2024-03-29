import os
import sys

import pygame

from game.drawing import Drawing, MenuDrawing, BoardDrawing
from game.events import MenuHandler, BoardHandler
from public.board import Board

pygame.init()
FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Chess Game")

    drawing = Drawing()
    screen = "start"
    handler = None

    while run:
        match screen:
            case "start":
                screen = None
                drawing.screen = MenuDrawing(drawing.win)
                handler = MenuHandler(drawing.screen)
            case "game_1":
                screen = None
                board = Board()
                drawing.screen = BoardDrawing(drawing.win, board)
                handler = BoardHandler(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if handler:
                screen = handler.handle(event)

        drawing.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
