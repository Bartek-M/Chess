import sys
import pygame

from game.drawing import Drawing, MenuDrawing, BoardDrawing
from game.events import handle_menu, handle_game
from public.board import Board

pygame.init()
FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption(f"Chess Game")

    drawing = Drawing()
    start, game = True, False
    event_handler = lambda: None

    while run:
        if start:
            drawing.screen = MenuDrawing(drawing.win)
            event_handler = lambda: handle_menu(event)
            start = False
        elif game:
            board = Board()
            drawing.screen = BoardDrawing(drawing.win, board)
            event_handler = lambda: handle_game(event, board)
            game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            event_handler()

        drawing.draw()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
