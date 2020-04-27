import pygame
from gui import GUI
import button
import moveBoxesGame
import os
from level import Level
import menu
import label

BUTTONS_NUM_PER_COL = 5
COLUMNS = 3
class ChooseLevel(GUI):
    def __init__(self, app, name, levels = [], num_added_buttons = 0):
        super().__init__(app, name)

        # button list for levels
        self.B = []
        self.gui_B = []
        screen = self.application.screen
        
        self.button_num_per_col = BUTTONS_NUM_PER_COL
        col = COLUMNS
        num_buttons_per_screen =  screen.get_height()/2/button.BUTTON_SIZE[1]       
        offset_h = (num_buttons_per_screen - self.button_num_per_col)/2
        h = offset_h*2*button.BUTTON_SIZE[1]

        num_columns_per_screen = screen.get_width()/3/button.BUTTON_SIZE[0]*2
        offset_w = (num_columns_per_screen - col)/2 
        w = offset_w*3*button.BUTTON_SIZE[0]/2 + button.BUTTON_SIZE[0]/4
        
        if len(levels) == 0:
            self.levels = []
            for name in sorted(app.GUIs['moveBoxesGame'].levels.keys()):
                self.levels.append(name)
        else:
            self.levels = levels
        self.num_added_buttons = num_added_buttons
        buttons_per_page = col*self.button_num_per_col + num_added_buttons
        number_of_buttons = len(self.levels)

        # level buttons
        i = num_added_buttons
        while i < buttons_per_page and i < number_of_buttons:
            name = self.levels[i]
            e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'moveBoxesGame', 'lvl': name})
            self.B.append(button.Button(f'LEVEL {name}', screen, e, (w, h)))
            self.button_num_per_col -= 1
            i += 1 
            if self.button_num_per_col:       
                h += 2*button.BUTTON_SIZE[1]
            else:
                w += 3*button.BUTTON_SIZE[0]/2
                self.button_num_per_col = BUTTONS_NUM_PER_COL 
                h = offset_h*2*button.BUTTON_SIZE[1]

        # if number of buttons is too big for one paage create a new one 
        if i < number_of_buttons:
            w_next = screen.get_width()/2+button.BUTTON_SIZE[0]/4
            h_next = (offset_h + BUTTONS_NUM_PER_COL)*2*button.BUTTON_SIZE[1]
            # button to next page
            e = pygame.event.Event(pygame.USEREVENT, {'name': f'ChooseLevel{i}', 'next': 1})
            self.gui_B.append(button.Button('NEXT', screen, e, (w_next, h_next)))
            ChooseLevel(app, f'ChooseLevel{i}', self.levels, i)
            w_back = screen.get_width()/2-button.BUTTON_SIZE[0] - button.BUTTON_SIZE[0]/4
        else:
            w_back = screen.get_width()/2-button.BUTTON_SIZE[0]/2

        h_back = (offset_h + BUTTONS_NUM_PER_COL)*2*button.BUTTON_SIZE[1]
       
        # if it is first page back to menu
        if num_added_buttons:
            e = pygame.event.Event(pygame.USEREVENT, {'name': f'ChooseLevel{self.num_added_buttons-COLUMNS*BUTTONS_NUM_PER_COL}', 'next': 0})
        else:
            e = pygame.event.Event(pygame.USEREVENT, {'name': '__main__', 'next': 0})
      
        # button to previous page
        self.gui_B.append(button.Button('BACK', screen, e, (w_back, h_back)))

        self.current_w = w
        self.current_h = h
        self.offset_h = offset_h
        if i ==  buttons_per_page:
            self.current_w = 0
            self.current_h = 0

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

    def add_level(self, name):
         screen = self.application.screen
         self.levels.append(name)
         if self.current_w and self.current_h:
            
             e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'moveBoxesGame', 'lvl': name})
             self.B.append(button.Button(f'LEVEL {name}', screen, e, (self.current_w, self.current_h)))
             self.button_num_per_col -= 1

             if len(self.levels)-self.num_added_buttons < BUTTONS_NUM_PER_COL*COLUMNS:
                 if self.button_num_per_col:
                     self.current_h += 2*button.BUTTON_SIZE[1]
                 else:
                     self.current_w += 3*button.BUTTON_SIZE[0]/2
                     self.button_num_per_col = BUTTONS_NUM_PER_COL
                     self.current_h = self.offset_h*2*button.BUTTON_SIZE[1]
             else:
                 self.current_w = 0
                 self.current_h = 0
         else:
             e = self.gui_B.pop(-1).event
             w_back = screen.get_width()/2-5*button.BUTTON_SIZE[0]/4
             h_next = (self.offset_h + BUTTONS_NUM_PER_COL)*2*button.BUTTON_SIZE[1]
             self.gui_B.append(button.Button('BACK', screen, e, (w_back, h_next)))
             w_next = screen.get_width()/2+button.BUTTON_SIZE[0]/4
             # button to next page
             i = len(self.levels) - 1
             e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': f'ChooseLevel{i}', 'next': 1, 'lvls': self.levels, 'index': i})
             self.gui_B.append(button.Button('NEXT', screen, e, (w_next, h_next)))
             ChooseLevel(self.application, f'ChooseLevel{i}', self.levels, i)
 

    """Button rendering."""
    def render(self):
        screen = self.application.screen
        screen.fill((0,0,0))
        for b in self.B:
            b.render() 
        for b in self.gui_B:
            b.render() 
        self.label.render('LEVELS')
        pygame.display.update()

    """Button event handler."""
    def process_event(self, e):
        for b in self.B:
            # indicates if level button was pressed 
            if e.type is pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(e.pos):
                b.color, b.new_color = b.new_color, b.color
                b.render()
                return
            # indicates if button was released
            elif e.type is pygame.MOUSEBUTTONUP and b.rect.collidepoint(e.pos):
                b.press()
                return
        for b in self.gui_B:
            # indicates if gui button was pressed
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
                self.application.GUIs[e.name].current_level = self.application.GUIs[e.name].levels[e.lvl]
            return e.name

