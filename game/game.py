import sys
import pygame

from drawing import Drawing
from board import Board


pygame.init()

WIDTH, HEIGHT = (720, 800)
PAD_X, PAD_Y = (40, 80)  # Dynamic, but suggested (40, 80) as minimum

TILE_SIZE = (WIDTH - PAD_X * 2) // 8
FPS = 60


def click(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos

    if not (PAD_X <= mouse_x < (WIDTH - PAD_X) and PAD_Y <= mouse_y < (HEIGHT - PAD_Y)):
        return

    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE
    piece = board.board[y][x]

    if (x, y) in board.valid_moves and board.current:
        return board.move(board.current, (x, y))
    
    if piece:        
        if not piece.dragged:
            return board.select(piece)

        piece.dragged = False
        return
        
    board.reset_selected()


def drag(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos

    if not (PAD_X <= mouse_x < (WIDTH - PAD_X) and PAD_Y <= mouse_y < (HEIGHT - PAD_Y)):
        return

    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE
    piece = board.board[y][x]

    if not piece or piece.dragged:
        return

    if piece != board.current:
        board.reset_selected()

    if not len(board.valid_moves):
        board.select(piece)

    piece.dragged = True


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(TILE_SIZE, (PAD_X, PAD_Y))
    drawing = Drawing(WIDTH, HEIGHT, board)

    pygame.display.set_caption(f"Chess Game")

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                drag(pygame.mouse.get_pos(), board)

            if event.type == pygame.MOUSEBUTTONUP:
                click(pygame.mouse.get_pos(), board)

        drawing.update()

        if board.current and board.current.dragged:
            drawing.draw()

    pygame.quit()
    sys.exit(0)
