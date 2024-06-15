import pygame
import os
import sys
import game
from constants import *

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Level Selector")

font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

def draw_button(screen, text, rect, is_hovered):
    color = HIGHLIGHT_GRAY if is_hovered else GRAY
    pygame.draw.rect(screen, color, rect)
    lines = split_text_to_fit_height(button_font, text, rect.width, rect.height)
    for i, line in enumerate(lines):
        label = button_font.render(line, True, BLACK)
        screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                            rect.y + (i * button_font.get_height()) + (rect.height - len(lines) * button_font.get_height()) // 2))

def split_text_to_fit_height(font, text, max_width, max_height):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        if font.size(' '.join(current_line))[0] > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

        if (len(lines) + 1) * font.get_height() > max_height:
            lines.append("...")
            return lines

    lines.append(' '.join(current_line))

    return lines

def level_selector(main_menu_callback):
    clock = pygame.time.Clock()

    levels = []
    level_directory = 'levels'
    for file in os.listdir(level_directory):
        if file.endswith('.json'):
            level_name = os.path.splitext(file)[0]
            image_path = os.path.join(level_directory, f'{level_name}.png')
            if os.path.exists(image_path):
                levels.append((level_name, image_path))

    back_button = pygame.Rect(50, HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    level_buttons = []

    x_offset = 0
    y = (HEIGHT - LEVEL_BUTTON_HEIGHT) // 2

    for idx, (level_name, image_path) in enumerate(levels):
        x = x_offset + idx * (LEVEL_BUTTON_WIDTH + 20)
        rect = pygame.Rect(x, y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        level_buttons.append((rect, level_name, image_path))

    scroll_x = 0
    max_scroll_x = max(0, (LEVEL_BUTTON_WIDTH + 20) * len(levels) - WIDTH)
    dragging = False

    while True:
        screen.fill(WHITE)

        mouse_pos = pygame.mouse.get_pos()

        for rect, level_name, image_path in level_buttons:
            scrolled_rect = rect.move(-scroll_x, 0)
            is_hovered = scrolled_rect.collidepoint(mouse_pos)
            draw_button(screen, level_name, scrolled_rect, is_hovered)
            level_image = pygame.image.load(image_path)
            level_image = pygame.transform.scale(level_image, LEVEL_IMAGE_SIZE)
            screen.blit(level_image, (scrolled_rect.x, scrolled_rect.y - LEVEL_IMAGE_SIZE[1] - 10))

        draw_button(screen, "Back", back_button, back_button.collidepoint(mouse_pos))

        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 50, WIDTH, 50))
        scrollbar_rect = pygame.Rect(50, HEIGHT - 40, WIDTH - 100, 30)
        handle_width = max(30, scrollbar_rect.width * (WIDTH / (max_scroll_x + WIDTH)))
        handle_rect = pygame.Rect(scrollbar_rect.x + (scrollbar_rect.width - handle_width) * (scroll_x / max_scroll_x),
                                  scrollbar_rect.y, handle_width, scrollbar_rect.height)
        pygame.draw.rect(screen, DARK_GRAY, scrollbar_rect)
        pygame.draw.rect(screen, LIGHT_GRAY, handle_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    main_menu_callback()
                    return
                if handle_rect.collidepoint(event.pos):
                    dragging = True
                    drag_start_x = event.pos[0]
                    start_scroll_x = scroll_x
                for rect, level_name, image_path in level_buttons:
                    if rect.move(-scroll_x, 0).collidepoint(event.pos):
                        level_path = os.path.join(level_directory, f'{level_name}.json')
                        with open(level_path, 'r') as file:
                            level_json = file.read()
                        game.Game(main_menu_callback, level_json).run()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    delta_x = event.pos[0] - drag_start_x
                    scroll_x = start_scroll_x + (delta_x * max_scroll_x / (scrollbar_rect.width - handle_width))
                    scroll_x = max(0, min(scroll_x, max_scroll_x))

        pygame.display.flip()
        clock.tick(60)
