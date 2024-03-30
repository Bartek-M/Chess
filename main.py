import sys

import pygame
import dotenv

from game.drawing import Drawing, MenuDrawing, BoardDrawing
from game.events import MenuHandler, BoardHandler
from public.board import Board

dotenv.load_dotenv()
pygame.init()

FPS = 60
TITLE = "Chess Game"


def main():
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption(TITLE)

    drawing = Drawing()
    screen = "start"
    handler = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if handler:
                screen = handler.handle(event)

        match screen:
            case "start":
                screen = None
                drawing.screen = MenuDrawing(drawing.win)
                handler = MenuHandler(drawing.screen)
            case "game_1":
                screen = None
                board = Board()
                drawing.screen = BoardDrawing(drawing.win, FPS, board)
                handler = BoardHandler(board)
            case "game_2":
                screen = None

        drawing.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
