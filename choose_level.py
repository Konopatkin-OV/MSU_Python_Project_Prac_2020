import pygame
from gui import GUI
import button
import moveBoxesGame
import os
from level import Level
import menu
import label


class ChooseLevel(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        # button list for levels
        self.B = []
        screen = self.application.screen
        screen.fill((0,0,0))
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        h = screen.get_height()/5

        # level buttons
        for index, level in enumerate(app.GUIs['moveBoxesGame'].levels):
            e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'moveBoxesGame', 'lvl': index})
            self.B.append(button.Button(f'LEVEL {level.name}', screen, e, (w, h)))
            h += 2*button.BUTTON_SIZE[1]

        # button to menu
        e = pygame.event.Event(pygame.USEREVENT, {'name': '__main__'})
        self.B.append(button.Button('BACK', screen, e, (w, h)))

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        for b in self.B:
            b.render() 
        self.label.render('LEVELS')
        pygame.display.update()

    """Button event handler."""
    def process_event(self, e):
        for b in self.B:
            # indicates if button was pressed 
            if e.type is pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(e.pos):
                b.color, b.new_color = b.new_color, b.color
                b.render()
                return
            # indicates if button was released
            elif e.type is pygame.MOUSEBUTTONUP and b.rect.collidepoint(e.pos):
                b.press()
                return
        if e.type == pygame.USEREVENT:
            if e.name == 'moveBoxesGame':
                self.application.GUIs[e.name].select_level(e.lvl)
            return e.name
