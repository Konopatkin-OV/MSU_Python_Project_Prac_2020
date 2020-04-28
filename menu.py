import pygame
from gui import GUI
import button
import choose_level
import moveBoxesGame
import settings
import label

FRAME_WIDTH = 3


class Menu(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        screen = self.application.screen

        # background 
        bg_coord = screen.get_width() / 2 - button.BUTTON_SIZE[0], 2 * label.LABEL_SIZE[1]
        self.bg_rect = pygame.Rect(bg_coord, (2 * button.BUTTON_SIZE[0], screen.get_height() - 4 * label.LABEL_SIZE[1]))
        frame_coord = self.bg_rect.left + FRAME_WIDTH, self.bg_rect.top + FRAME_WIDTH
        frame_size = 2 * button.BUTTON_SIZE[0] - 2 * FRAME_WIDTH, screen.get_height() - 4 * label.LABEL_SIZE[
            1] - 2 * FRAME_WIDTH
        self.frame_rect = pygame.Rect(frame_coord, frame_size)

        # button list for menu
        self.B = []
        w = screen.get_width() / 2 - button.BUTTON_SIZE[0] / 2
        button_num = 5
        num_buttons_per_screen = screen.get_height() / 2 / button.BUTTON_SIZE[1]
        offset = (num_buttons_per_screen - button_num) / 2

        h = offset * 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame'})
        self.B.append(button.Button('START', screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application,
                                                  'name': 'ChooseLevel0'})
        self.B.append(button.Button('LEVELS', screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'NewLevel'})
        self.B.append(button.Button('NEW LEVEL', screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'Settings'})
        self.B.append(button.Button('SETTINGS', screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button('EXIT', screen, e, (w, h)))

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

        choose_level.ChooseLevel(app, 'ChooseLevel0')
        settings.Settings(app, 'Settings')

    """Button rendering."""

    def render(self):
        screen = self.application.screen
        screen.fill((0, 0, 0))

        screen.fill(pygame.Color(100, 80, 100), self.bg_rect)
        screen.fill(pygame.Color(0, 0, 0), self.frame_rect)
        for b in self.B:
            b.render()
        self.label.render('MENU')
        pygame.display.update()

    """Button event handler."""

    def process_event(self, e):
        # press a button
        for b in self.B:
            b.process_event(e)

        if e.type == pygame.USEREVENT:
            return e.name
