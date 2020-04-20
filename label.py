import pygame

TEXT_COLOR = 200, 200, 200
LABEL_SIZE = 160, 50

class Label():
    def __init__(self, screen, coord, label_size = LABEL_SIZE, color = pygame.Color(0, 0, 0), font_size = 30):
       
        # create label rectangle
        self.rect = pygame.Rect(coord, label_size)
        self.screen = screen
 
        # create label text
        self.font = pygame.font.SysFont('freesansboldttf', font_size)

        self.color = color     

    """Render a button."""
    def render(self, text_name):
        self.screen.fill(self.color, self.rect)
                
        text = self.font.render(text_name, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)
  

