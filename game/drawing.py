import pygame


class Drawing:
    LIGHT = 226, 226, 226
    DARK = 130, 130, 129
    BACKGROUND = 1, 0, 25

    def __init__(self, width, height):
        self.window = pygame.display.set_mode((width, height))
        self.draw_grid()

    def draw_grid(self):
        self.window.fill(self.BACKGROUND)
