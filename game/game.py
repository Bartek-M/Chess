import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (896, 896)
TILE_SIZE = WIDTH // 8

FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(TILE_SIZE)
    drawing = Drawing(WIDTH, HEIGHT, board)
    pygame.display.set_caption(f"Chess Game")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        drawing.draw()

    pygame.quit()
