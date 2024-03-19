import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (768, 768)
TILE_SIZE = WIDTH // 8

FPS = 30


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

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button != 1:
                    continue

                mouse_x, mouse_y = pygame.mouse.get_pos()
                piece = board.board[mouse_y // TILE_SIZE][mouse_x // TILE_SIZE]

                if piece == None:
                    continue

                board.select(piece)

        drawing.draw()

    pygame.quit()
