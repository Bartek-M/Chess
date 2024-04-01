import sys

import pygame
import dotenv

from game.drawing import Drawing, MenuDrawing, BoardDrawing
from game.events import MenuHandler, BoardHandler
from game.client import Client
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

        if screen == "start":
            drawing.screen = MenuDrawing(drawing.win)
            handler = MenuHandler(drawing.screen)
        elif screen == "game-1":
            board = Board()
        elif screen == "game-2":
            print(drawing.screen.get_input("name-inpt"))
            print(drawing.screen.get_input("code-inpt"))
            board = Board(client=Client())

        if screen in ["game-1", "game-2"]:
            drawing.screen = BoardDrawing(drawing.win, FPS, board)
            handler = BoardHandler(board)

        drawing.draw()
        clock.tick(FPS)
        screen = None

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
