import pygame

from public.utils import format_time, load_assets

PAD_X, PAD_Y = 60, 80
WIDTH, HEIGHT = 640 + PAD_X * 2, 640 + PAD_Y * 2 + 20
TILE_SIZE = (WIDTH - PAD_X * 2) // 8

pygame.font.init()
FONT_M = pygame.font.SysFont("consolas", 18)
FONT_L = pygame.font.SysFont("consolas", 22)
FONT_XL = pygame.font.SysFont("arialblack", 50)


class Drawing:
    BACKGROUND = 1, 0, 25
    COLOR = 200, 200, 200

    def __init__(self, screen=None):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = screen
        self.draw()

    def draw(self):
        self.win.fill(self.BACKGROUND)

        if self.screen:
            self.screen.draw()

        pygame.display.update()

    @staticmethod
    def draw_text(win, font, text, pos, color=None, center=False):
        text = font.render(str(text), True, color if color else Drawing.COLOR)
        if center:
            pos = text.get_rect(center=pos)

        win.blit(text, pos)


class MenuDrawing:
    COLOR = 235, 235, 235
    BUTTON_COLOR = 100, 150, 150

    def __init__(self, win):
        self.win = win

    def draw(self):
        self.draw_title()
        self.draw_buttons()

    def draw_title(self):
        text = "Chess"
        Drawing.draw_text(self.win, FONT_XL, text, (WIDTH // 2, 80), self.COLOR, True)

    def draw_buttons(self):
        b_width, b_height = 125, 50
        x = WIDTH // 3 - 25
        y = HEIGHT // 2 + 100

        pygame.draw.rect(self.win, self.BUTTON_COLOR, (x, y, b_width, b_height), 5, 5)
        x = WIDTH - b_width - x
        pygame.draw.rect(self.win, self.BUTTON_COLOR, (x, y, b_width, b_height), 5, 5)


class BoardDrawing:
    LIGHT_COLOR = 238, 238, 238
    DARK_COLOR = 116, 116, 116

    GRAY_COLOR = 200, 200, 200
    GREEN_COLOR = 56, 220, 255
    RED_COLOR = 255, 50, 50

    def __init__(self, win, board):
        self.win = win
        self.board = board

        self.white_assets, self.black_assets = load_assets(TILE_SIZE)

    def draw(self):
        self.draw_cords()
        self.draw_players()
        self.draw_timers()
        self.draw_board()

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = self.LIGHT_COLOR if (i + j) % 2 == 0 else self.DARK_COLOR
                x = PAD_X + j * TILE_SIZE
                y = PAD_Y + i * TILE_SIZE

                pygame.draw.rect(self.win, color, (x, y, TILE_SIZE, TILE_SIZE))
                piece = self.board.board[i][j]

                if (j, i) in self.board.valid_moves:
                    self.draw_valid_moves(x, y, piece)

                if piece is None or piece.dragged:
                    continue

                self.draw_piece(piece)

        if self.board.current and self.board.current.dragged:
            self.draw_piece(self.board.current)

    def draw_piece(self, piece):
        assets = self.black_assets if piece.color == "b" else self.white_assets
        piece.draw(self.win, assets, TILE_SIZE, (PAD_X, PAD_Y))

    def draw_valid_moves(self, x, y, piece):
        if piece is None:
            color = self.GRAY_COLOR
            radius = 12
            border = 0
        else:
            color = (
                self.RED_COLOR
                if piece.color != self.board.current.color
                else self.GREEN_COLOR
            )
            radius = TILE_SIZE * 0.4
            border = 5

        cx = x + TILE_SIZE // 2
        cy = y + TILE_SIZE // 2
        pygame.draw.circle(self.win, color, (cx, cy), radius, border)

    def draw_players(self):
        player_1 = f"{'Black' if self.board.color == 'w' else 'White'}: Player 2"
        player_2 = f"{'White' if self.board.color == 'w' else 'Black'}: Player 1"
        Drawing.draw_text(self.win, FONT_L, player_1, (PAD_X, 20))
        Drawing.draw_text(self.win, FONT_L, player_2, (PAD_X, HEIGHT - 40))

    def draw_timers(self):
        timer_1 = format_time(self.board.timers[0])
        timer_2 = format_time(self.board.timers[1])
        Drawing.draw_text(self.win, FONT_L, timer_1, (WIDTH - PAD_X - 70, 20))
        Drawing.draw_text(self.win, FONT_L, timer_2, (WIDTH - PAD_X - 70, HEIGHT - 40))

    def draw_cords(self):
        nums = ["8", "7", "6", "5", "4", "3", "2", "1"]
        alph = ["a", "b", "c", "d", "e", "f", "g", "h"]

        if self.board.color == "b":
            nums = nums[::-1]
            alph = alph[::-1]

        for i in range(8):
            x = PAD_X - 20
            y = i * TILE_SIZE + (PAD_Y + TILE_SIZE // 2 - 10)
            Drawing.draw_text(self.win, FONT_M, str(nums[i]), (x, y))

        for i, l in enumerate(alph):
            x = i * TILE_SIZE + (PAD_X + TILE_SIZE // 2 - 5)
            y = 8 * TILE_SIZE + PAD_Y + 5
            Drawing.draw_text(self.win, FONT_M, l, (x, y))
