"""label.py
===========
Label class for creating text in a rectangle.
"""
import pygame
from typing import Tuple

TEXT_COLOR: Tuple[int, int, int] = (200, 200, 200)
LABEL_SIZE: Tuple[int, int] = (200, 50)


class Label():
    def __init__(self, screen: pygame.Surface, coord: Tuple[int, int],
                 label_size: Tuple[int, int] = LABEL_SIZE,
                 color: pygame.Color = pygame.Color(0, 0, 0),
                 font_size: int = 28):

        # create label rectangle
        self.rect = pygame.Rect(coord, label_size)
        self.screen = screen

        # create label text
        self.font = pygame.font.SysFont('freesansboldttf', font_size)

        self.color = color

    def render(self, text_name: str, TEXT_ONLY: bool = False):
        """Render a button."""

        if not TEXT_ONLY:
            self.screen.fill(self.color, self.rect)
        text = self.font.render(text_name, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)
