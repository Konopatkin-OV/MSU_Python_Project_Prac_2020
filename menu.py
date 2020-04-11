from gui import GUI
import button
import pygame
from levels import Level

class Menu(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        screen = self.application.screen
   
        #button list for menu
        self.B = []
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        h =  screen.get_height()/2-button.BUTTON_SIZE[1]/2
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button('EXIT', screen, e, (w, h)))

        lvl0 = '0'
        e = pygame.event.Event(pygame.USEREVENT, {'app': app, 'lv': lvl0})
        h -= 2*button.BUTTON_SIZE[1] 
        self.B.append(button.Button('START', screen, e, (w, h)))
             

    """Button event handler."""
    def process_event(self, e):
        for b in self.B:
            # indicates if button was pressed 
            if e.type is pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(e.pos):
                b.press()
                return
        if e.type == pygame.USEREVENT:
                Level(e.app, e.lv)


