import pygame
from gui import GUI
import button
import moveBoxesGame
import os
from level import Level
import menu


class ChooseLevel(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        # button list for levels
        self.B = []
   
    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        h =  screen.get_height()/4

        # level buttons        
        root, dirs, files = next(os.walk('lvls/', topdown=True))
        for name in sorted(files):
            if name.endswith('.lvl'):
                name = name[:-4]
                try:
                    e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'moveBoxesGame', 'lvl': name})
                    self.B.append(button.Button(f'LEVEL {name}', screen, e, (w, h))) 
                    h += 2*button.BUTTON_SIZE[1]
                except IOError:
                    print(f'Level {name} is not valid.')
        
        # button to menu
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': '__main__'})
        self.B.append(button.Button('BACK', screen, e, (w,h)))        
        
        pygame.display.update()

    """Button event handler."""
    def process_event(self, e):
        for b in self.B:
            # indicates if button was pressed 
            if e.type is pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(e.pos):
                b.press()
                return
        if e.type == pygame.USEREVENT:
            if e.name == 'moveBoxesGame':
                M = moveBoxesGame.MoveBoxesGame(e.app, e.name)
                M.current_level =  M.levels[e.lvl]
                return e.name
            else:
                menu.Menu(e.app, e.name)
                return e.name

