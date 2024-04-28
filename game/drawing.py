import os
import pygame

from game.components import Button, TextInput
from public.utils import format_time, load_assets

PAD_X, PAD_Y = 60, 90
WIDTH, HEIGHT = 640 + PAD_X * 2, 640 + PAD_Y * 2 + 20
TILE_SIZE = (WIDTH - PAD_X * 2) // 8

pygame.font.init()
FONT_M = pygame.font.SysFont("consolas", 18)
FONT_L = pygame.font.SysFont("consolas", 22)
FONT_XL = pygame.font.SysFont("consolas", 72, bold=True)


class Drawing:
    BACKGROUND = 1, 0, 25
    COLOR = 200, 200, 200

    def __init__(self, screen: object = None) -> None:
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = screen
        self.cards = []
        self.draw()

    def draw(self) -> None:
        self.win.fill(self.BACKGROUND)

        if self.screen:
            self.screen.draw()

        self.draw_cards()
        pygame.display.update()

    def draw_cards(self) -> None:
        for card in self.cards:
            card.draw()

    @staticmethod
    def draw_text(
        win: pygame.Surface,
        font: pygame.font,
        text: str,
        pos: list[int],
        color: tuple[int] = None,
        center: bool = False,
    ) -> None:
        color = color if color else Drawing.COLOR
        text = font.render(str(text), True, color)

        if center:
            pos = text.get_rect(center=pos)

        win.blit(text, pos)


class MenuDrawing:
    COLOR = 235, 235, 235
    RED = 235, 75, 75

    def __init__(self, win: pygame.Surface, info: str = None) -> None:
        self.win = win
        self.info = info
        self.components = self.setup_components()

    def draw(self) -> None:
        self.draw_title()
        self.draw_info()
        self.draw_components()

    def draw_title(self) -> None:
        text = "CHESS"
        Drawing.draw_text(self.win, FONT_XL, text, (WIDTH // 2, 100), self.COLOR, True)

    def draw_info(self) -> None:
        if not self.info:
            return

        pos = (WIDTH // 2, HEIGHT - 50)
        Drawing.draw_text(self.win, FONT_L, self.info, pos, self.RED, True)

    def draw_components(self) -> None:
        for item in self.components.values():
            item.draw(self.win)

    def setup_components(self) -> dict[str:object]:
        dims = 400, 50
        x, y = WIDTH // 2 - dims[0] // 2, HEIGHT // 2 - 100

        name = os.getenv("PLAYER_NAME", "Player")

        return {
            "name-inpt": TextInput(name, "Name:", (x, y), dims, FONT_L),
            "code-inpt": TextInput("", "Code:", (x, y := y + 75), dims, FONT_L),
            "local-btn": Button(
                "Local", (x, y := y + 200), dims, FONT_L, lambda: "game-1"
            ),
            "multiplayer-btn": Button(
                "Multiplayer", (x, y + 75), dims, FONT_L, lambda: "game-2"
            ),
        }

    def get_input(self, name: str, alt: str = None) -> str:
        inpt = self.components.get(name)
        return inpt.text if inpt else alt


class BoardDrawing:
    LIGHT = 238, 238, 238
    DARK = 116, 116, 116

    GRAY = 200, 200, 200
    CYAN = 56, 220, 255
    RED = 255, 50, 50

    def __init__(self, win: pygame.Surface, board: object) -> None:
        self.win = win
        self.board = board

        self.white_assets, self.black_assets = load_assets(TILE_SIZE)

    def draw(self) -> None:
        self.draw_cords()
        self.draw_players()
        self.draw_timers()
        self.draw_board()

    def draw_board(self) -> None:
        current = self.board.current

        for i in range(8):
            for j in range(8):
                color = self.LIGHT if (i + j) % 2 == 0 else self.DARK
                x = PAD_X + j * TILE_SIZE
                y = PAD_Y + i * TILE_SIZE

                pygame.draw.rect(self.win, color, (x, y, TILE_SIZE, TILE_SIZE))
                piece = self.board.board[i][j]

                if current and [j, i] in current.valid_moves:
                    self.draw_valid_moves(x, y, piece)

                if [j, i] in self.board.last_moves:
                    self.draw_last_moves(x, y)

                if piece is None or piece.dragged:
                    continue

                self.draw_piece(piece)

        if current and current.dragged:
            self.draw_piece(current)

    def draw_piece(self, piece: object) -> None:
        assets = self.black_assets if piece.color == "b" else self.white_assets
        piece.draw(self.win, assets, TILE_SIZE, (PAD_X, PAD_Y))

    def draw_last_moves(self, x: int, y: int) -> None:
        color = self.CYAN if self.board.turn == "b" else self.RED
        pygame.draw.rect(self.win, color, (x, y, TILE_SIZE, TILE_SIZE), 4)

    def draw_valid_moves(self, x: int, y: int, piece: object) -> None:
        if piece is None:
            color = self.GRAY
            radius = 12
            border = 0
        else:
            color = self.RED if piece.color != self.board.current.color else self.CYAN
            radius = TILE_SIZE * 0.4
            border = 5

        cx = x + TILE_SIZE // 2
        cy = y + TILE_SIZE // 2
        pygame.draw.circle(self.win, color, (cx, cy), radius, border)

    def draw_players(self) -> None:
        if self.board.client and self.board.paused and not self.board.win:
            name_1, name_2 = "-", self.board.client.name
            code = self.board.client.code
            info = f"Waiting... [code: {code}]"
        else:
            name_1, name_2 = self.board.players
            info = f"Turn: {'white' if self.board.turn == 'w' else 'black'}"

        if self.board.text:
            info = self.board.text

        if self.board.color == "w":
            player_1, player_2 = f"Black: {name_1}", f"White: {name_2}"
        else:
            player_1, player_2 = f"White: {name_1}", f"Black: {name_2}"

        Drawing.draw_text(self.win, FONT_L, info, (WIDTH // 2, 70), center=True)
        Drawing.draw_text(self.win, FONT_L, player_1, (PAD_X, 20))
        Drawing.draw_text(self.win, FONT_L, player_2, (PAD_X, HEIGHT - 40))

    def draw_timers(self) -> None:
        timer_1, timer_2 = self.board.timers
        if self.board.color == "w":
            timer_1, timer_2 = format_time(timer_1), format_time(timer_2)
        else:
            timer_1, timer_2 = format_time(timer_2), format_time(timer_1)

        Drawing.draw_text(self.win, FONT_L, timer_2, (WIDTH - PAD_X - 70, 20))
        Drawing.draw_text(self.win, FONT_L, timer_1, (WIDTH - PAD_X - 70, HEIGHT - 40))
        self.board.timer()

    def draw_cords(self) -> None:
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
