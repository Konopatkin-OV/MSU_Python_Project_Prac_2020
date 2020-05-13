import pygame
from typing import Tuple

TEXT_COLOR: Tuple[int, int, int] = (200, 200, 200)
TEXTBOX_SIZE: Tuple[int, int] = (200, 40)
MAX_LENGTH: int = 9
FRAME_WIDTH: int = 3


class TextBox():
    def __init__(self, screen: pygame.Surface, coord: Tuple[int, int],
                 box_size: Tuple[int, int] = TEXTBOX_SIZE,
                 color: pygame.Color = pygame.Color(100, 80, 100),
                 font_size: int = 30):
        # create textbox rectangle
        self.rect_box = pygame.Rect(coord, box_size)
        text_box_size = box_size[0] - 2*FRAME_WIDTH, box_size[1] - 2*FRAME_WIDTH
        text_box_coord = self.rect_box.left + FRAME_WIDTH, self.rect_box.top + FRAME_WIDTH
        self.rect = pygame.Rect(text_box_coord, text_box_size)
        self.screen = screen

        # create text font
        self.font = pygame.font.SysFont('freesansboldttf', font_size)
        self.str = ''

        self.color = color
        self.start_writing = 0

    def start(self):
        """Start enter text."""

        self.str = '|'
        self.start_writing = 1

    def render(self):
        """Render a textbox."""

        self.screen.fill(self.color, self.rect_box)
        self.screen.fill(pygame.Color(0, 0, 0), self.rect)

        text = self.font.render(self.str, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)

    def process_event(self, e: pygame.event.EventType):
        """Entering processing."""

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
