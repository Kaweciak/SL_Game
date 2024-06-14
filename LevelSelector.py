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
    label = button_font.render(text, True, BLACK)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))

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

    for idx, (level_name, image_path) in enumerate(levels):
        x = (WIDTH - LEVEL_BUTTON_WIDTH) // 2
        y = (HEIGHT // 3) + idx * (LEVEL_BUTTON_HEIGHT + 20)
        rect = pygame.Rect(x, y, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
        level_buttons.append((rect, level_name, image_path))

    while True:
        screen.fill(WHITE)

        mouse_pos = pygame.mouse.get_pos()
        
        for rect, level_name, image_path in level_buttons:
            is_hovered = rect.collidepoint(mouse_pos)
            draw_button(screen, level_name, rect, is_hovered)
            level_image = pygame.image.load(image_path)
            level_image = pygame.transform.scale(level_image, LEVEL_IMAGE_SIZE)
            screen.blit(level_image, (rect.x, rect.y - LEVEL_IMAGE_SIZE[1] - 10))

        draw_button(screen, "Back", back_button, back_button.collidepoint(mouse_pos))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    main_menu_callback()
                    return
                for rect, level_name, image_path in level_buttons:
                    if rect.collidepoint(event.pos):
                        level_path = os.path.join(level_directory, f'{level_name}.json')
                        with open(level_path, 'r') as file:
                            level_json = file.read()
                        game.Game(main_menu_callback, level_json).run()
        
        pygame.display.flip()
        clock.tick(60)
