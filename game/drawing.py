import pygame

from public.utils import format_time


class Drawing:
    LIGHT = 226, 226, 226
    DARK = 130, 130, 129
    BACKGROUND = 1, 0, 25
    COLOR = 200, 200, 200

    def __init__(self, width, height, padding, board):
        self.width = width
        self.height = height
        self.pad_x, self.pad_y = padding

        self.window = pygame.display.set_mode((width, height))
        self.board = board

        self.font_m = pygame.font.SysFont("consolas", 18)
        self.font_l = pygame.font.SysFont("consolas", 22)
        self.draw()

    def draw(self):
        self.window.fill(self.BACKGROUND)
        self.players()
        self.timers()
        self.board.draw_cords(self.window, self.font_m)
        self.board.draw(self.window)

        pygame.display.update()

    def players(self):
        player_1 = self.font_l.render(
            f"{'Black' if self.board.color == 'w' else 'White'}: Player 2",
            True,
            self.COLOR,
        )
        self.window.blit(player_1, (self.pad_x, 20))

        player_2 = self.font_l.render(
            f"{'White' if self.board.color == 'w' else 'Black'}: Player 1",
            True,
            self.COLOR,
        )
        self.window.blit(player_2, (self.pad_x, self.height - 40))

    def timers(self):
        time_1 = self.font_l.render(format_time(self.board.timers[0]), True, self.COLOR)
        self.window.blit(time_1, (self.width - self.pad_x - 70, 20))

        time_2 = self.font_l.render(format_time(self.board.timers[1]), True, self.COLOR)
        self.window.blit(time_2, (self.width - self.pad_x - 70, self.height - 40))

        self.board.timer()
