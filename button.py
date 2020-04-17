import pygame

TEXT_COLOR = 200, 200, 200
BUTTON_SIZE = 130, 30

class Button():
    def __init__(self, name, screen, event, coord, button_size = BUTTON_SIZE,  color = pygame.Color(100, 80, 100), font_size = 30):
        self.name = name
        self.event = event

        # create button rectangle
        self.rect = pygame.Rect(coord, button_size)
        self.screen = screen
 
        # create button text
        self.font = pygame.font.Font(pygame.font.get_default_font(), font_size)        
        self.name = name    
        self.color = color     

    def render(self,):
        self.screen.fill(self.color, self.rect)
     
        text = self.font.render(self.name, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)
        
    """Post event to events queue."""
    def press(self): 
        pygame.event.post(self.event) 
        
