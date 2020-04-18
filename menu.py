import pygame
from gui import GUI
import button
import choose_level
import moveBoxesGame

class Menu(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)

        #button list for menu
        self.B = []
    
    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        h =  screen.get_height()/2-button.BUTTON_SIZE[1]/2
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button('EXIT', screen, e, (w, h)))
     
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 
                               'name': 'ChooseLevel'})
        h -= 2*button.BUTTON_SIZE[1] 
        self.B.append(button.Button('LEVELS', screen, e, (w, h))) 

        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 
                               'name': 'moveBoxesGame'})
        h -= 2*button.BUTTON_SIZE[1] 
        self.B.append(button.Button('START', screen, e, (w, h))) 
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
                moveBoxesGame.MoveBoxesGame(e.app, e.name)
                return e.name
            else:
                choose_level.ChooseLevel(e.app, e.name)
                return e.name

