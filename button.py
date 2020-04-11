import pygame

BUTTON_SIZE = 100, 30

TEXT_COLOR = 200, 200, 200


class Button():
    def __init__(self, name, screen, event, coord):
        self.name = name
        self.event = event

        # create button rectangle

        color = pygame.Color(100, 80, 100)
        self.rect = pygame.Rect(coord, BUTTON_SIZE)
        self.screen = screen
        self.screen.fill(color, self.rect)
 
        # create button text

        font = pygame.font.Font(pygame.font.get_default_font(), 30)        
        text = font.render(name, True, TEXT_COLOR) 
        place = text.get_rect(center=self.rect.center)
        screen.blit(text, place)      
        
    """Post event to events queue."""
    def press(self):
        pygame.event.post(self.event) 
