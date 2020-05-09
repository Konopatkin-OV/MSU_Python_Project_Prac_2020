import pygame
from gui import GUI
import label
import button
import controls

FRAME_WIDTH = 3

class Settings(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        screen = self.application.screen

        # buttons list
        self.B = []
     
        # labels list
        self.L = []

        w_l = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w_l, 0), color=pygame.Color(70, 50, 70)))

        w = screen.get_width() / 2 - button.BUTTON_SIZE[0] / 2 
        h = screen.get_height() / 2 - 3 * button.BUTTON_SIZE[1] 
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'Controls'})
        self.B.append(button.Button(_('CONTROLS'), screen, e, (w, h)))

        controls.Controls(app, 'Controls')

        w -= 3 * button.BUTTON_SIZE[0] / 4
        h += 3 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'Mode'})
        self.B.append(button.Button(_('MODE'), screen, e, (w, h)))  

        self.set_mode = False

        w +=  3 * button.BUTTON_SIZE[0] / 2
        h -=  button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'Classic'})
        self.B.append(button.Button(_('CLASSIC'), screen, e, (w, h)))
        
        classic_coord = w - 3 * FRAME_WIDTH, h - 3 * FRAME_WIDTH
        size = button.BUTTON_SIZE[0] + 6 * FRAME_WIDTH, button.BUTTON_SIZE[1] + 7 * FRAME_WIDTH
        self.classic_rect = pygame.Rect(classic_coord, size)
        frame_coord = self.classic_rect.left + FRAME_WIDTH, self.classic_rect.top + FRAME_WIDTH
        frame_size = size[0] - 2 * FRAME_WIDTH,  size[1] - 2 * FRAME_WIDTH
        self.frame_cl_rect = pygame.Rect(frame_coord, frame_size)

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'Easy'})
        self.B.append(button.Button(_('EASY'), screen, e, (w, h)))

        easy_coord = w - 3 * FRAME_WIDTH, h - 3 * FRAME_WIDTH
        self.easy_rect = pygame.Rect(easy_coord, size)
        frame_coord = self.easy_rect.left + FRAME_WIDTH, self.easy_rect.top + FRAME_WIDTH
        self.frame_ea_rect = pygame.Rect(frame_coord, frame_size)

        # button to menu
        w -=  3 * button.BUTTON_SIZE[0] / 2 
        w +=  3 * button.BUTTON_SIZE[0] / 4
        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': '__main__'})
        self.B.append(button.Button(_('BACK'), screen, e, (w, h)))

        # background
        bg_coord = screen.get_width() / 2 - 3 * button.BUTTON_SIZE[0]/2, h - 15 * button.BUTTON_SIZE[1] / 2
        self.bg_rect = pygame.Rect(bg_coord, (3 * button.BUTTON_SIZE[0],  19 * button.BUTTON_SIZE[1] / 2))
        frame_coord = self.bg_rect.left + FRAME_WIDTH, self.bg_rect.top + FRAME_WIDTH
        frame_size = 3 * button.BUTTON_SIZE[0] - 2 * FRAME_WIDTH,  19 * button.BUTTON_SIZE[1] / 2 - 2 * FRAME_WIDTH
        self.frame_rect = pygame.Rect(frame_coord, frame_size)


    """Button rendering."""

    def render(self):
        screen = self.application.screen
        screen.fill((0, 0, 0))

        screen.fill(pygame.Color(100, 80, 100), self.bg_rect)
        screen.fill(pygame.Color(0, 0, 0), self.frame_rect)

        if self.application.GUIs['moveBoxesGame'].allow_all_box_moves:
            screen.fill(pygame.Color(100, 80, 100), self.easy_rect)
            screen.fill(pygame.Color(0, 0, 0), self.frame_ea_rect)
        else:
            screen.fill(pygame.Color(100, 80, 100), self.classic_rect)
            screen.fill(pygame.Color(0, 0, 0), self.frame_cl_rect)

        for b in self.B:
            b.render()
        self.label.render(_('SETTINGS'))
        pygame.display.update()

    """Button event handler."""

    def process_event(self, e):
        if self.set_mode:
            self.B[2].process_event(e)
            self.B[3].process_event(e)
        else: 
            # press a button
            self.B[0].process_event(e)
            self.B[1].process_event(e)
            self.B[-1].process_event(e)        
        if e.type == pygame.USEREVENT:
            if e.name == 'Mode':
                self.set_mode = True
            elif e.name == 'Classic':
                self.application.GUIs['moveBoxesGame'].allow_all_box_moves = False
                self.set_mode = False
            elif e.name == 'Easy':
                self.application.GUIs['moveBoxesGame'].allow_all_box_moves = True
                self.set_mode = False
            else:
                return e.name
