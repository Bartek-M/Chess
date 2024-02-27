import os
import pygame

pygame.init()

WIDTH, HEIGHT = (900, 900)
FPS = 60

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


def main():
    run = True
    clock = pygame.time.Clock()

    drawing = Drawing()
    pygame.display.set_caption(f"Chess")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
