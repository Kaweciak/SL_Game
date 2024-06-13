import pygame
from entities import Player, Platform, Obstacle, FinishPoint, State

class Game:
    def __init__(self, main_menu_callback):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.platforms = [Platform(100, 500, 200, 10), Platform(400, 400, 200, 10)]
        self.obstacles = [Obstacle(300, 300, 50, 50)]
        self.start_point = (100, 100)
        self.finish_point = FinishPoint(700, 500, 50, 50)
        self.game_state = State.PLAYING
        self.main_menu_callback = main_menu_callback

    def reset_level(self):
        self.player.set_spawn_point(*self.start_point)
        self.player.respawn()

    def run(self):
        self.reset_level()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.game_state == State.PLAYING:
                self.update()
                self.render()
            elif self.game_state == State.DEAD:
                self.show_message("You died!", ["Retry", "Quit"], self.handle_death_choice)
            elif self.game_state == State.COMPLETE:
                self.show_message("Level Complete!", ["Retry", "Quit"], self.handle_complete_choice)
            
            self.clock.tick(60)

    def update(self):
        self.game_state = self.player.update(self.platforms, self.obstacles)
        if self.player.rect.colliderect(self.finish_point.rect):
            self.game_state = State.COMPLETE

    def render(self):
        self.screen.fill((255, 255, 255))
        for platform in self.platforms:
            platform.render(self.screen)
        for obstacle in self.obstacles:
            obstacle.render(self.screen)
        self.finish_point.render(self.screen)
        self.player.render(self.screen)
        pygame.display.flip()

    def show_message(self, message, options, callback):
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))

        self.screen.fill((255, 255, 255))
        self.screen.blit(text, text_rect)

        button_font = pygame.font.Font(None, 50)
        button_texts = [button_font.render(opt, True, (0, 0, 0)) for opt in options]
        button_rects = [text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50 * (i + 1))) for i, text in enumerate(button_texts)]

        for button_text, button_rect in zip(button_texts, button_rects):
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect.inflate(20, 10), 2)
            self.screen.blit(button_text, button_rect)

        pygame.display.flip()

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, button_rect in enumerate(button_rects):
                        if button_rect.collidepoint(pos):
                            callback(i)
                            choosing = False

    def handle_death_choice(self, choice):
        if choice == 0:  # Retry
            self.reset_level()
            self.game_state = State.PLAYING
        elif choice == 1:  # Quit
            self.main_menu_callback()

    def handle_complete_choice(self, choice):
        if choice == 0:  # Retry
            self.reset_level()
            self.game_state = State.PLAYING
        elif choice == 1:  # Quit
            self.main_menu_callback()

if __name__ == '__main__':
    from MainMenu import main_menu
    Game(main_menu).run()
