import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
LEVEL_BUTTON_WIDTH = 300
LEVEL_BUTTON_HEIGHT = 200

LEVEL_IMAGE_SIZE = (300, 150)

FONT_SIZE = 74
BUTTON_FONT_SIZE = 50


def draw_button(screen, text, rect, is_hovered):
    color = DARK_GRAY if is_hovered else LIGHT_GRAY
    pygame.draw.rect(screen, color, rect)
    label = pygame.font.Font(None, BUTTON_FONT_SIZE).render(text, True, BLACK)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))