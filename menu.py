"""menu.py
===========
GUI class for menu page.
"""
import pygame
from gui import GUI
import button
import label

FRAME_WIDTH: int = 3


class Menu(GUI):
    def __init__(self, app, name: str):
        super().__init__(app, name)
        screen = self.application.screen

        # background
        bg_coord = screen.get_width() / 2 - button.BUTTON_SIZE[0], 2 * label.LABEL_SIZE[1]
        self.bg_rect = pygame.Rect(bg_coord, (2 * button.BUTTON_SIZE[0],
                                              screen.get_height() - 4 * label.LABEL_SIZE[1]))
        frame_coord = self.bg_rect.left + FRAME_WIDTH, self.bg_rect.top + FRAME_WIDTH
        frame_size = 2 * button.BUTTON_SIZE[0] - 2 * FRAME_WIDTH, \
            screen.get_height() - 4 * label.LABEL_SIZE[1] - 2 * FRAME_WIDTH
        self.frame_rect = pygame.Rect(frame_coord, frame_size)

        # button list for menu
        self.B = []
        w = screen.get_width() / 2 - button.BUTTON_SIZE[0] / 2
        button_num = 5
        num_buttons_per_screen = screen.get_height() / 2 / button.BUTTON_SIZE[1]
        offset = (num_buttons_per_screen - button_num) / 2

        h = offset * 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame'})
        self.B.append(button.Button(_('START'), screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application,
                                                  'name': 'ChooseLevel0'})
        self.B.append(button.Button(_('LEVELS'), screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'NewLevel'})
        self.B.append(button.Button(_('NEW LEVEL'), screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'Settings'})
        self.B.append(button.Button(_('SETTINGS'), screen, e, (w, h)))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button(_('EXIT'), screen, e, (w, h)))

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

    def render(self):
        """Button rendering."""

        screen = self.application.screen
        screen.fill((0, 0, 0))
#        walls_w = screen.get_width() / WALL_IMAGE.get_width()
#        walls_h = screen.get_height() / WALL_IMAGE.get_height()
#        for i in range(int(walls_w)):
#            for j in range(int(walls_h+1)):
#                screen.blit(WALL_IMAGE, (i * WALL_IMAGE.get_width(),
#                                         j * WALL_IMAGE.get_height()))
#        screen.fill(pygame.Color(255, 190, 192, 255), self.bg_rect)

        screen.fill(pygame.Color(100, 80, 100), self.bg_rect)
        screen.fill(pygame.Color(0, 0, 0), self.frame_rect)

#        screen.fill(pygame.Color(130, 130, 130), self.frame_rect)
        for b in self.B:
            b.render()
        self.label.render(_('MENU'))
        pygame.display.update()

    def process_event(self, e: pygame.event.EventType):
        """Button event handler."""

        # press a button
        for b in self.B:
            b.process_event(e)

        if e.type == pygame.USEREVENT:
            return e.name
