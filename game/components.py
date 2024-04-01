import pygame


class Button:
    BG_COLOR = 56, 73, 99
    FG_COLOR = 235, 235, 235

    def __init__(
        self,
        text,
        pos,
        width,
        height,
        font,
        action=lambda: None,
        colors=None,
        border=0,
        radius=5,
    ):
        self.colors = colors if colors else (self.BG_COLOR, self.FG_COLOR)
        self.text = font.render(str(text), True, self.colors[1])

        x, y = pos
        self.rect = pygame.Rect(x, y, width, height)
        self.text_pos = self.text.get_rect(center=(x + width // 2, y + height // 2))

        self.border = border
        self.radius = radius

        self.action = action

    def draw(self, win):
        pygame.draw.rect(win, self.colors[0], self.rect, self.border, self.radius)
        win.blit(self.text, self.text_pos)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class TextInput:
    BG_COLOR = 56, 73, 99
    ACTIVE_COLOR = 56, 173, 199
    FG_COLOR = 235, 235, 235

    def __init__(
        self, text, place_holder, pos, width, height, font, border=5, radius=5
    ):
        self.text = str(text)
        self.place_holder = str(place_holder)
        self.max_size = 25
        self.font = font

        x, y = pos
        self.rect = pygame.Rect(x, y, width, height)
        self.text_pos = (x + 12, y + height // 2 - 11)
        self.active = False

        self.border = border
        self.radius = radius

    def draw(self, win):
        color = self.ACTIVE_COLOR if self.active else self.BG_COLOR
        pygame.draw.rect(win, color, self.rect, self.border, self.radius)

        text = self.font.render(f"{self.place_holder} {self.text}", True, self.FG_COLOR)
        win.blit(text, self.text_pos)

    def clicked(self, pos):
        self.active = False
        return self.rect.collidepoint(pos)

    def action(self):
        self.active = not self.active

    def backspace(self):
        if len(self.text) <= 0:
            return

        self.text = self.text[:-1]
        