import pygame
from gui import GUI
import button
import choose_level
import moveBoxesGame
import settings
import label

class Menu(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)

        # button list for menu
        self.B = []
        screen = self.application.screen
        w = screen.get_width()/2-button.BUTTON_SIZE[0]/2
        button_num = 5
        num_buttons_per_screen =  screen.get_height()/2/button.BUTTON_SIZE[1]       
        offset = (num_buttons_per_screen - button_num)/2
    
        h = offset*2*button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame'})
        self.B.append(button.Button('START', screen, e, (w, h))) 

        h += 2* button.BUTTON_SIZE[1] 
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 
                               'name': 'ChooseLevel0'})
        self.B.append(button.Button('LEVELS', screen, e, (w, h))) 

        h += 2* button.BUTTON_SIZE[1] 
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'NewLevel'})
        self.B.append(button.Button('NEW LEVEL', screen, e, (w, h)))

        h += 2* button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'Settings'})
        self.B.append(button.Button('SETTINGS', screen, e, (w, h)))


        h += 2* button.BUTTON_SIZE[1] 
        e = pygame.event.Event(pygame.QUIT)
        self.B.append(button.Button('EXIT', screen, e, (w, h)))

        w2 = screen.get_width()/2 - label.LABEL_SIZE[0]/2
        self.label = (label.Label(screen, (w2,0), color = pygame.Color(70, 50, 70)))

        choose_level.ChooseLevel(app, 'ChooseLevel0')
        settings.Settings(app, 'Settings')        
    
    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        for b in self.B:
            b.render()
        self.label.render('MENU')
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
            return e.name

