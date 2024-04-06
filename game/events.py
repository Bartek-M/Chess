import pygame

from game.components import Button, TextInput
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
            if [x, y] in current.valid_moves and current.color == self.board.turn:
                return self.board.move(self.board.current, [x, y])

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

        if current and [x, y] in current.valid_moves:
            return self.board.move(current, [x, y])

        if piece != current:
            self.board.reset_selected()

        if not self.board.current:
            self.board.select(piece)
            piece.first_select = True

        piece.dragged = True

    def handle(self, event):
        if event.type == pygame.KEYUP:
            if not (event.mod & pygame.KMOD_CTRL):
                return None

            if event.key == pygame.K_r:
                self.board.reset()
            elif event.key == pygame.K_p:
                self.board.pause()
            elif event.key == pygame.K_q:
                return "start"

        if event.type == pygame.MOUSEBUTTONUP:
            self.click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.drag(pygame.mouse.get_pos())

        return None


class MenuHandler:
    def __init__(self, drawing):
        self.drawing = drawing

    def click(self, mouse_pos):
        for item in self.drawing.components.values():
            if not item.clicked(mouse_pos):
                continue

            action = item.action()
            if type(item) is Button:
                return action

        return None

    def typing(self, text_input, key=None, backspace=False):
        if backspace:
            return text_input.backspace()

        if len(text_input.text) >= text_input.max_size:
            return

        if not key.isalnum() and key != " ":
            return

        text_input.text += key

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            return self.click(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            for item in self.drawing.components.values():
                if type(item) is not TextInput or not item.active:
                    continue

                if event.key == pygame.K_BACKSPACE:
                    self.typing(item, backspace=True)
                else:
                    self.typing(item, key=event.unicode)

        return None
