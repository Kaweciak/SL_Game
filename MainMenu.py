import pygame
import sys
import game

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT_GRAY = (170, 170, 170)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
BUTTON_WIDTH, BUTTON_HEIGHT = 400, 100

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

def draw_button(screen, text, rect, is_hovered):
    color = HIGHLIGHT_GRAY if is_hovered else GRAY
    pygame.draw.rect(screen, color, rect)
    label = button_font.render(text, True, BLACK)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                        rect.y + (rect.height - label.get_height()) // 2))


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
                    game.Game(main_menu).run()
                elif editor_button.collidepoint(event.pos):
                    print("Level Editor button pressed")
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

main_menu()