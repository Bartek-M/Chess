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

        if self.board.current:
            if (x, y) in self.board.valid_moves:
                return self.board.move(self.board.current, (x, y))

            piece = self.board.board[y][x]
            if not (piece or self.board.current.dragged):
                return self.board.reset_selected()

            self.board.current.dragged = False

            if self.board.current.first_select:
                self.board.current.first_select = False
                return
            elif piece != self.board.current:
                return

        self.board.reset_selected()

    def drag(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

        if not (0 <= x < 8 and 0 <= y < 8):
            return

        piece = self.board.board[y][x]

        if not piece or piece.dragged:
            return

        if self.board.current and (x, y) in self.board.valid_moves:
            return self.board.move(self.board.current, (x, y))

        if piece != self.board.current:
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
