import pygame
from gui import GUI
import button
import moveBoxesGame
import os
from level import Level
import menu
import label

BUTTONS_NUM_PER_COL = 6
COLUMNS = 2

class ChooseLevel(GUI):
    def __init__(self, app, name, levels = [], num_added_buttons = 0):
        super().__init__(app, name)
        # button list for levels
        self.B = []
        self.gui_B = []
        screen = self.application.screen
        
        button_num_per_col = BUTTONS_NUM_PER_COL
        col = COLUMNS
        num_buttons_per_screen =  screen.get_height()/2/button.BUTTON_SIZE[1]       
        offset_h = (num_buttons_per_screen - button_num_per_col)/2
        h = offset_h*2*button.BUTTON_SIZE[1]

        num_columns_per_screen = screen.get_width()/3/button.BUTTON_SIZE[0]*2
        offset_w = (num_columns_per_screen - col)/2 
        w = offset_w*3*button.BUTTON_SIZE[0]/2 + button.BUTTON_SIZE[0]/4
        
        self.levels = []
        for name in sorted(app.GUIs['moveBoxesGame'].levels.keys()):
            self.levels.append(name)

        buttons_per_page = col*button_num_per_col + num_added_buttons
        number_of_buttons = len(app.GUIs['moveBoxesGame'].levels)

        # level buttons

        i = num_added_buttons
        while i < buttons_per_page:
            name = self.levels[i]
            e = pygame.event.Event(pygame.USEREVENT, {'app': self.application, 'name': 'moveBoxesGame', 'lvl': name})
            self.B.append(button.Button(f'LEVEL {name}', screen, e, (w, h)))
            button_num_per_col -= 1
            number_of_buttons -= 1
            i += 1 
            if button_num_per_col:       
                h += 2*button.BUTTON_SIZE[1]
            else:
                w += 3*button.BUTTON_SIZE[0]/2
                button_num_per_col = BUTTONS_NUM_PER_COL 
                h = offset_h*2*button.BUTTON_SIZE[1]

        if i < number_of_buttons:
            w_next = screen.get_width()/2+button.BUTTON_SIZE[0]/4
            h_next = (offset_h + button_num_per_col)*2*button.BUTTON_SIZE[1]
            # button to next page
            e = pygame.event.Event(pygame.USEREVENT, {'name': f'ChooseLevel{i}', 'lvl': self.levels, 'index': i})
            self.gui_B.append(button.Button('NEXT', screen, e, (w_menu, h_menu)))
            w_menu = screen.get_width()/2-button.BUTTON_SIZE[0]/2 - button.BUTTON_SIZE[0]/4
        else:
            w_menu = screen.get_width()/2-button.BUTTON_SIZE[0]/2
      
        h_menu = (offset_h + button_num_per_col)*2*button.BUTTON_SIZE[1]
        # button to menu
        e = pygame.event.Event(pygame.USEREVENT, {'name': '__main__'})
        self.gui_B.append(button.Button('BACK', screen, e, (w_menu, h_menu)))

        self.current_w = w
        self.current_h = h

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

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
            # indicates if button was pressed 
            if e.type is pygame.MOUSEBUTTONDOWN and b.rect.collidepoint(e.pos):
                b.color, b.new_color = b.new_color, b.color
                b.render()
                return
            # indicates if button was released
            elif e.type is pygame.MOUSEBUTTONUP and b.rect.collidepoint(e.pos):
                b.press()
                return
        for b in self.gui_B:
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
                self.application.GUIs[e.name].current_level = self.application.GUIs[e.name].levels[e.lvl]
            return e.name

