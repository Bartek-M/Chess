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
    client = None
    info = None
    screen, handler = "start", None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if handler:
                screen = handler.handle(event)

        if screen and client:
            client.disconnect()
            del client

        if screen == "game-1":
            board = Board()
        elif screen == "game-2":
            name = drawing.screen.get_input("name-inpt", "Player")
            code = drawing.screen.get_input("code-inpt")

            try:
                board = Board()
                client = Client(board, name, code)
            except:
                info = "[ERROR] Couldn't connect to the server"
                screen = "start"

        if screen:
            del drawing.screen
        if screen == "start":
            drawing.screen = MenuDrawing(drawing.win, info)
            handler = MenuHandler(drawing.screen)
        elif screen in ["game-1", "game-2"]:
            drawing.screen = BoardDrawing(drawing.win, FPS, board)
            handler = BoardHandler(board)

        drawing.draw()
        clock.tick(FPS)
        screen = None

    if client:
        client.disconnect()
        del client

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
