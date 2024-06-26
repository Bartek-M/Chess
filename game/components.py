import pygame


class Button:
    BG_COLOR = 56, 73, 99
    FG_COLOR = 235, 235, 235

    def __init__(
        self,
        text: str,
        pos: list[int],
        dims: list[int],
        font: pygame.font,
        action=lambda: None,
        colors: list[tuple] = None,
    ) -> None:
        self.colors = colors if colors else (self.BG_COLOR, self.FG_COLOR)
        self.text = font.render(text, True, self.colors[1])

        x, y = pos
        width, height = dims
        self.rect = pygame.Rect(x, y, width, height)
        self.text_pos = self.text.get_rect(center=(x + width // 2, y + height // 2))

        self.border = 0
        self.radius = 5

        self.action = action

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(win, self.colors[0], self.rect, self.border, self.radius)
        win.blit(self.text, self.text_pos)

    def clicked(self, pos: list[int]) -> bool:
        return self.rect.collidepoint(pos)


class TextInput:
    BG_COLOR = 56, 73, 99
    ACTIVE_COLOR = 56, 173, 199
    FG_COLOR = 235, 235, 235

    def __init__(
        self,
        text: str,
        place_holder: str,
        pos: list[int],
        dims: list[int],
        font: pygame.font,
    ) -> None:
        self.text = text
        self.place_holder = place_holder
        self.max_size = 25
        self.font = font

        x, y = pos
        width, height = dims
        self.rect = pygame.Rect(x, y, width, height)
        self.text_pos = (x + 12, y + height // 2 - 11)
        self.active = False

        self.border = 5
        self.radius = 5

    def draw(self, win: pygame.Surface) -> None:
        color = self.ACTIVE_COLOR if self.active else self.BG_COLOR
        pygame.draw.rect(win, color, self.rect, self.border, self.radius)

        text = self.font.render(f"{self.place_holder} {self.text}", True, self.FG_COLOR)
        win.blit(text, self.text_pos)

    def clicked(self, pos: list[int]) -> bool:
        self.active = False
        return self.rect.collidepoint(pos)

    def action(self) -> None:
        self.active = not self.active

    def backspace(self) -> None:
        if len(self.text) <= 0:
            return

        self.text = self.text[:-1]
