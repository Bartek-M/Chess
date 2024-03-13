import pygame

from board import Drawing


pygame.init()
FPS = 60


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