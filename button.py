
import pygame
import gradients


TEXT_COLOR = 200, 200, 200
BUTTON_SIZE = 130, 30


class Button():
    def __init__(self, name, screen, event, coord, button_size = BUTTON_SIZE, color = pygame.Color(70, 50, 70), font_size = 30):
        self.name = name
        self.event = event

        # create button rectangle
        self.rect = pygame.Rect(coord, button_size)
        self.screen = screen

        bot_size = button_size[0], 3  
        self.rect_bot = pygame.Rect(self.rect.bottomleft, bot_size)     
        self.color_bot = color.r-15, color.g-15, color.b-15, color.a
 
        # create button text
        self.font = pygame.font.SysFont('freesansboldttf', font_size)
       
#        self.font = pygame.font.SysFont('SegoeUISymbolttf', font_size)
        self.new_color = color     
        self.color = color.r+62, color.g+62, color.b+62, color.a

    """Render a button."""
    def render(self):
#        self.screen.fill(self.color, self.rect)
        self.screen.blit(gradients.vertical(self.rect.size, self.color, self.new_color), self.rect)
        self.screen.fill(self.color_bot, self.rect_bot)        

        text = self.font.render(self.name, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)
  
    """Post event to events queue."""
    def press(self): 
        self.color, self.new_color = self.new_color, self.color
        self.render() 
        pygame.event.post(self.event)
