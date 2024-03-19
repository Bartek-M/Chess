import pygame


class Drawing:
    LIGHT = 226, 226, 226
    DARK = 130, 130, 129
    BACKGROUND = 1, 0, 25

    def __init__(self, width, height, board):
        self.window = pygame.display.set_mode((width, height))
        self.board = board

        self.draw()

    def draw(self):
        self.window.fill(self.BACKGROUND)
        self.board.draw(self.window)

        pygame.display.update()