import pygame

from game.drawing import PAD_X, PAD_Y, TILE_SIZE


class BoardHandler:
    def __init__(self, board):
        self.board = board

    def click(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

        if not (0 <= x < 8 and 0 <= y < 8):
            return self.board.reset_selected()

        current = self.board.current
        if current:
            if (x, y) in current.valid_moves and current.color == self.board.turn:
                return self.board.move(self.board.current, (x, y))

            piece = self.board.board[y][x]
            if not (piece or current.dragged):
                return self.board.reset_selected()

            current.dragged = False

            if current.first_select:
                current.first_select = False
                return
            elif piece != current:
                return

        self.board.reset_selected()

    def drag(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        current = self.board.current
        piece = self.board.board[y][x]

        if not piece or piece.dragged:
            return

        if current and (x, y) in current.valid_moves:
            return self.board.move(current, (x, y))

        if piece != current:
            self.board.reset_selected()

        if not self.board.current:
            self.board.select(piece)
            piece.first_select = True

        piece.dragged = True

    def handle(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.board.reset()

        if event.type == pygame.MOUSEBUTTONUP:
            self.click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.drag(pygame.mouse.get_pos())

        return None


class MenuHandler:
    def __init__(self, drawing):
        self.drawing = drawing

    def click(self, mouse_pos):
        for btn in self.drawing.buttons:
            if not btn.clicked(mouse_pos):
                continue

            return btn.action()

        return None

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            return self.click(pygame.mouse.get_pos())

        return None
