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
        screen = self.application.screen
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        h = screen.get_height()/2+button.BUTTON_SIZE[1]/2
        
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'NewLevel'})
        self.B.append(button.Button('NEW LEVEL', screen, e, (w, h)))

        h += 4*button.BUTTON_SIZE[1]/2
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button('EXIT', screen, e, (w, h)))
     
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 
                               'name': 'ChooseLevel'})
        h -= 4*button.BUTTON_SIZE[1] 
        self.B.append(button.Button('LEVELS', screen, e, (w, h))) 

        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame'})
        h -= 2*button.BUTTON_SIZE[1] 
        self.B.append(button.Button('START', screen, e, (w, h))) 
         
        self.render()
        
    
    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        for b in self.B:
            b.render()
        pygame.display.update()
              

    """Button event handler."""
    def process_event(self, e):
        for b in self.B:
            # indicates if button was pressed, pressing animation 
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
                return e.name
            elif e.name == 'ChooseLevel':
                choose_level.ChooseLevel(e.app, e.name)
                return e.name


