import pygame


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
        self.font_l = pygame.font.SysFont("consolas", 24)
        self.draw()

    def draw(self):
        self.window.fill(self.BACKGROUND)
        self.board.draw_cords(self.window, self.font_m)
        self.players()
        self.timers()

    def update(self):
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
        time_1 = self.font_l.render("10:00", True, self.COLOR)
        self.window.blit(time_1, (self.width - self.pad_x - 70, 20))

        time_2 = self.font_l.render("10:00", True, self.COLOR)
        self.window.blit(time_2, (self.width - self.pad_x - 70, self.height - 40))
