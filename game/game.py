import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (900, 900)
FPS = 60

GRID_SIZE = 8
TILE_SIZE = WIDTH / GRID_SIZE


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(GRID_SIZE, GRID_SIZE)
    drawing = Drawing(WIDTH, HEIGHT)
    pygame.display.set_caption(f"Chess")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
