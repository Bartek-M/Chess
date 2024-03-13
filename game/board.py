import pygame

WIDTH, HEIGHT = (900, 900)

GRID_SIZE = 8
TILE_SIZE = WIDTH / GRID_SIZE


class Drawing:
    LIGHT = 226, 226, 226
    DARK = 130, 130, 129
    BACKGROUND = 1, 0, 25

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.draw_grid()

    def draw_grid(self):
        self.window.fill(self.BACKGROUND)