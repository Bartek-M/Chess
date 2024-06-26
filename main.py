import os
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


def main() -> None:
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
            client = None

        if screen == "game-1":
            board = Board()
        elif screen == "game-2":
            name = drawing.screen.get_input("name-inpt", "Player")
            code = drawing.screen.get_input("code-inpt", "").lower()
            os.environ["PLAYER_NAME"] = name

            try:
                client = Client(name, code)
                board = client.board
            except:
                info = "[ERROR] Couldn't connect to the server"
                screen = "start"

        if screen:
            del drawing.screen
        if screen == "start":
            drawing.screen = MenuDrawing(drawing.win, info)
            handler = MenuHandler(drawing.screen)
        elif screen in ["game-1", "game-2"]:
            drawing.screen = BoardDrawing(drawing.win, board)
            handler = BoardHandler(board)

        try:
            drawing.draw()
            clock.tick(FPS)
            screen = None
        except Exception as e:
            print(e)
            break

    if client:
        client.disconnect()
        client = None

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
