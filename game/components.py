import pygame


class Button:
    FG_COLOR = 235, 235, 235
    BG_COLOR = 91, 96, 104

    def __init__(self, text, pos, width, height, font, action=lambda: None, colors=None, border=0, radius=5):
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
