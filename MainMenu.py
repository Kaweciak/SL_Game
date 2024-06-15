import pygame
import sys
import LevelSelector
from constants import *
from LevelEditor import LevelEditor

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")


def main_menu():
    clock = pygame.time.Clock()
    
    play_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 3, BUTTON_WIDTH, BUTTON_HEIGHT)
    editor_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT * 2 // 3, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    while True:
        screen.fill(WHITE)
        
        mouse_pos = pygame.mouse.get_pos()
        
        draw_button(screen, "Play", play_button, play_button.collidepoint(mouse_pos))
        draw_button(screen, "Level Editor", editor_button, editor_button.collidepoint(mouse_pos))
        draw_button(screen, "Quit", quit_button, quit_button.collidepoint(mouse_pos))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    LevelSelector.level_selector(main_menu)
                elif editor_button.collidepoint(event.pos):
                    LevelEditor(main_menu).run()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

main_menu()
