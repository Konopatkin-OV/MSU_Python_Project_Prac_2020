import pygame

TEXT_COLOR = 200, 200, 200
TEXTBOX_SIZE = 200, 40
MAX_LENGTH = 9 #10
FRAME_WIDTH = 3

class TextBox():
    def __init__(self, screen, coord, box_size = TEXTBOX_SIZE, color = pygame.Color(100, 80, 100), font_size = 30):
       
        # create textbox rectangle
        self.rect_box = pygame.Rect(coord, box_size)
        text_box_size = box_size[0] - 2*FRAME_WIDTH, box_size[1] - 2*FRAME_WIDTH
        text_box_coord = self.rect_box.left + FRAME_WIDTH, self.rect_box.top + FRAME_WIDTH
        self.rect = pygame.Rect(text_box_coord, text_box_size)
        self.screen = screen

        # create text font
        self.font = pygame.font.SysFont('freesansboldttf', font_size)
        self.str = 'my level'

        self.color = color     
        self.start_writing = 0

    """Start enter text."""
    def start(self):
        self.str = '|'
        self.start_writing = 1

    """Render a textbox."""
    def render(self):
        self.screen.fill(self.color, self.rect_box)
        self.screen.fill(pygame.Color(0, 0, 0), self.rect)        
        
        text = self.font.render(self.str, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)
  
    """Entering processing."""
    def process_event(self, e):
       if e.type is pygame.KEYDOWN: 
           if e.unicode.isalnum() or e.key is pygame.K_SPACE:
               if len(self.str) < MAX_LENGTH:
                   self.str = self.str[0:len(self.str)-1]
                   self.str += e.unicode + '|'
           elif len(self.str) > 0 and e.key is pygame.K_BACKSPACE:
               self.str = self.str[0:len(self.str)-2] + '|'
           elif e.key is pygame.K_RETURN: 
               self.str = self.str[0:len(self.str)-1]
               self.start_writing = 0
       elif e.type is pygame.USEREVENT:
           if e.name == 'ok':
               self.str = self.str[0:len(self.str)-1]
               self.start_writing = 0
       return 
