import pygame
import sys
import level_selector
from constants import *
from level_editor import LevelEditor

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")


def main():
    clock = pygame.time.Clock()
    
    play_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 3, BUTTON_WIDTH, BUTTON_HEIGHT)
    editor_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT * 2 // 3, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    while True:
        screen.fill(GRAY)
        
        mouse_pos = pygame.mouse.get_pos()
        
        draw_button(screen, "Play", play_button, play_button.collidepoint(mouse_pos))
        draw_button(screen, "Level Creator", editor_button, editor_button.collidepoint(mouse_pos))
        draw_button(screen, "Quit", quit_button, quit_button.collidepoint(mouse_pos))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    level_selector.level_selector(main)
                elif editor_button.collidepoint(event.pos):
                    LevelEditor(main).run()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()