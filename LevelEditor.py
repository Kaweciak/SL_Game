import pygame
import pygame_gui
import json
import os
from entities import *
from constants import *

class LevelEditor:
    def __init__(self, main_menu_callback, level_json=None):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.Clock()
        self.main_menu_callback = main_menu_callback
        self.selected_object = None
        self.dragging = False
        self.resizing = False
        self.resize_edge = None

        self.manager = pygame_gui.UIManager(self.screen.get_size())
        self.setup_ui()

        if level_json:
            self.level = Level.from_json(level_json)
        else:
            self.level = Level(StartPoint(100, 100), [], [], [])

        self.hotbar_objects = [
            Platform(0, 0, 100, 20),
            Obstacle(0, 0, 50, 50),
            FinishPoint(0, 0, 50, 50),
            StartPoint(0, 0)
        ]
        self.hotbar_rects = []
        self.setup_hotbar()

        screen_width, screen_height = self.screen.get_size()
        self.save_button_rect = pygame.Rect((screen_width - 260, screen_height - 60), (250, 50))
        self.quit_button_rect = pygame.Rect((screen_width - 630, screen_height - 60), (350, 50))
        self.is_save_button_hovered = False
        self.is_quit_button_hovered = False

        # Load custom cursors
        self.cursors = {
            'default': pygame.SYSTEM_CURSOR_ARROW,
            'left': pygame.SYSTEM_CURSOR_SIZEWE,
            'right': pygame.SYSTEM_CURSOR_SIZEWE,
            'top': pygame.SYSTEM_CURSOR_SIZENS,
            'bottom': pygame.SYSTEM_CURSOR_SIZENS,
            'top-left': pygame.SYSTEM_CURSOR_SIZENWSE,
            'top-right': pygame.SYSTEM_CURSOR_SIZENESW,
            'bottom-left': pygame.SYSTEM_CURSOR_SIZENESW,
            'bottom-right': pygame.SYSTEM_CURSOR_SIZENWSE
        }

    def setup_ui(self):
        screen_width, screen_height = self.screen.get_size()
        self.text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((screen_width - 260, screen_height - 100), (250, 50)),
            manager=self.manager
        )

    def setup_hotbar(self):
        screen_height = self.screen.get_height()
        hotbar_y = screen_height - 110
        for i in range(len(self.hotbar_objects)):
            rect = pygame.Rect(i * 110 + 10, hotbar_y, 100, 100)
            self.hotbar_rects.append(rect)

    def run(self):
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.manager.update(time_delta)
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            self.manager.process_events(event)

            mouse_pos = pygame.mouse.get_pos()
            self.is_save_button_hovered = self.save_button_rect.collidepoint(mouse_pos)
            self.is_quit_button_hovered = self.quit_button_rect.collidepoint(mouse_pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_save_button_hovered:
                    self.save_and_quit()
                elif self.is_quit_button_hovered:
                    self.quit_without_saving()

    def handle_mouse_button_down(self, event):
        if event.button == 1:
            for rect in self.hotbar_rects:
                if rect.collidepoint(event.pos):
                    index = self.hotbar_rects.index(rect)
                    obj = self.hotbar_objects[index]
                    if isinstance(obj, Platform):
                        new_obj = Platform(event.pos[0], event.pos[1], obj.rect.width, obj.rect.height)
                    elif isinstance(obj, Obstacle):
                        new_obj = Obstacle(event.pos[0], event.pos[1], obj.rect.width, obj.rect.height)
                    elif isinstance(obj, FinishPoint):
                        new_obj = FinishPoint(event.pos[0], event.pos[1], obj.rect.width, obj.rect.height)
                    elif isinstance(obj, StartPoint):
                        new_obj = StartPoint(event.pos[0], event.pos[1])
                        self.level.start_point = new_obj
                    self.selected_object = new_obj
                    self.dragging = True
                    if isinstance(self.selected_object, Platform):
                        self.level.platforms.append(self.selected_object)
                    elif isinstance(self.selected_object, Obstacle):
                        self.level.obstacles.append(self.selected_object)
                    elif isinstance(self.selected_object, FinishPoint):
                        self.level.finish_points.append(self.selected_object)
                    return

            for obj in self.level.platforms + self.level.obstacles + self.level.finish_points + [self.level.start_point]:
                if obj.rect.collidepoint(event.pos):
                    self.selected_object = obj
                    self.resize_edge = self.get_resize_edge(event.pos, obj.rect)
                    if self.resize_edge:
                        self.resizing = True
                    else:
                        self.dragging = True
                    return
        elif event.button == 3:
            for obj in self.level.platforms + self.level.obstacles + self.level.finish_points:
                if obj.rect.collidepoint(event.pos):
                    if isinstance(obj, Platform):
                        self.level.platforms.remove(obj)
                    elif isinstance(obj, Obstacle):
                        self.level.obstacles.remove(obj)
                    elif isinstance(obj, FinishPoint):
                        self.level.finish_points.remove(obj)
                    return

    def handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            self.selected_object = None

    def handle_mouse_motion(self, event):
        if self.dragging and self.selected_object:
            self.selected_object.rect.x += event.rel[0]
            self.selected_object.rect.y += event.rel[1]
        elif self.resizing and self.selected_object:
            rect = self.selected_object.rect
            if 'left' in self.resize_edge:
                rect.width -= event.rel[0]
                rect.x += event.rel[0]
            if 'right' in self.resize_edge:
                rect.width += event.rel[0]
            if 'top' in self.resize_edge:
                rect.height -= event.rel[1]
                rect.y += event.rel[1]
            if 'bottom' in self.resize_edge:
                rect.height += event.rel[1]
        else:
            self.update_cursor(event.pos)

    def get_resize_edge(self, pos, rect):
        edge_margin = 10
        edges = []
        if rect.x <= pos[0] <= rect.x + edge_margin:
            edges.append('left')
        if rect.right - edge_margin <= pos[0] <= rect.right:
            edges.append('right')
        if rect.y <= pos[1] <= rect.y + edge_margin:
            edges.append('top')
        if rect.bottom - edge_margin <= pos[1] <= rect.bottom:
            edges.append('bottom')
        return edges if edges else None

    def update_cursor(self, pos):
        cursor_type = 'default'
        for obj in self.level.platforms + self.level.obstacles + self.level.finish_points + [self.level.start_point]:
            if obj.rect.collidepoint(pos):
                edges = self.get_resize_edge(pos, obj.rect)
                if edges:
                    if 'left' in edges and 'top' in edges:
                        cursor_type = 'top-left'
                    elif 'right' in edges and 'top' in edges:
                        cursor_type = 'top-right'
                    elif 'left' in edges and 'bottom' in edges:
                        cursor_type = 'bottom-left'
                    elif 'right' in edges and 'bottom' in edges:
                        cursor_type = 'bottom-right'
                    elif 'left' in edges:
                        cursor_type = 'left'
                    elif 'right' in edges:
                        cursor_type = 'right'
                    elif 'top' in edges:
                        cursor_type = 'top'
                    elif 'bottom' in edges:
                        cursor_type = 'bottom'
                    break
        pygame.mouse.set_cursor(self.cursors[cursor_type])

    def render(self):
        self.screen.fill(WHITE)
        for platform in self.level.platforms:
            platform.render(self.screen)
        for obstacle in self.level.obstacles:
            obstacle.render(self.screen)
        for finish_point in self.level.finish_points:
            finish_point.render(self.screen)
        self.level.start_point.render(self.screen)
        self.render_hotbar()
        self.manager.draw_ui(self.screen)
        draw_button(self.screen, 'Save and Quit', self.save_button_rect, self.is_save_button_hovered)
        draw_button(self.screen, 'Quit Without Saving', self.quit_button_rect, self.is_quit_button_hovered)
        pygame.display.flip()

    def render_hotbar(self):
        for i, rect in enumerate(self.hotbar_rects):
            pygame.draw.rect(self.screen, GRAY, rect)
            if isinstance(self.hotbar_objects[i], Platform):
                pygame.draw.rect(self.screen, (0, 255, 0), rect.inflate(-10, -10))
            elif isinstance(self.hotbar_objects[i], Obstacle):
                pygame.draw.rect(self.screen, (255, 0, 0), rect.inflate(-10, -10))
            elif isinstance(self.hotbar_objects[i], FinishPoint):
                pygame.draw.rect(self.screen, (0, 255, 255), rect.inflate(-10, -10))
            elif isinstance(self.hotbar_objects[i], StartPoint):
                pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(-10, -10))

    def save_and_quit(self):
        level_name = self.text_entry.get_text().strip()
        if not level_name:
            self.show_error_message("Please enter a name for the level before saving.")
            return

        level_dict = self.level.to_dict()
        levels_dir = 'Levels'
        os.makedirs(levels_dir, exist_ok=True)

        if self.level.start_point is None:
            self.show_error_message("The level must have exactly one starting point.")
            return
        if len(self.level.finish_points) == 0:
            self.show_error_message("The level must have at least one finish point.")
            return

        file_path = os.path.join(levels_dir, f'{level_name}.json')
        with open(file_path, 'w') as file:
            json.dump(level_dict, file, indent=4)

        layout_surface = pygame.Surface(self.screen.get_size())
        layout_surface.fill(WHITE)

        for platform in self.level.platforms:
            platform.render(layout_surface)
        for obstacle in self.level.obstacles:
            obstacle.render(layout_surface)
        for finish_point in self.level.finish_points:
            finish_point.render(layout_surface)
        self.level.start_point.render(layout_surface)

        screenshot_path = os.path.join(levels_dir, f'{level_name}.png')
        pygame.image.save(layout_surface, screenshot_path)

        self.main_menu_callback()

    def quit_without_saving(self):
        self.main_menu_callback()

    def show_error_message(self, message):
        error_dialog = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 75), (300, 150)),
            html_message=message,
            manager=self.manager
        )
