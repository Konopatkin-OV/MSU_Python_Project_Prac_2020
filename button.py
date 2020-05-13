"""button.py
============================
Class for creating a button with text.
"""
import pygame
import gradients
from typing import Tuple

TEXT_COLOR: Tuple[int, int, int] = (200, 200, 200)
BUTTON_SIZE: Tuple[int, int] = (130, 30)


class Button:
    def __init__(self, name: str, screen: pygame.Surface, event: pygame.event.EventType,
                 coord: Tuple[int, int],
                 button_size: Tuple[int, int] = BUTTON_SIZE,
                 color: pygame.Color = pygame.Color(70, 50, 70),
                 font_size: int = 25):
        self.name = name
        self.event = event

        # create button rectangle
        self.rect = pygame.Rect(coord, button_size)
        self.screen = screen

        bot_size = button_size[0], 3
        self.rect_bot = pygame.Rect(self.rect.bottomleft, bot_size)
        self.color_bot = color.r - 15, color.g - 15, color.b - 15, color.a

        # create button text
        self.font = pygame.font.SysFont('freesansboldttf', font_size)

        self.new_color = color
        self.color = color.r + 62, color.g + 62, color.b + 62, color.a

        self.is_button_pressed = 0

    def render(self):
        """Render a button."""

        self.screen.blit(gradients.vertical(self.rect.size,
                                            self.color,
                                            self.new_color),
                         self.rect)
        self.screen.fill(self.color_bot, self.rect_bot)

        text = self.font.render(self.name, True, TEXT_COLOR)
        place = text.get_rect(center=self.rect.center)
        self.screen.blit(text, place)

    def press(self):
        """Post event to events queue."""

        self.color, self.new_color = self.new_color, self.color
        self.render()
        pygame.event.post(self.event)

    def process_event(self, e: pygame.event.EventType):
        """Button event handler."""

        # indicates if button was pressed, pressing animation
        if e.type is pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
            self.color, self.new_color = self.new_color, self.color
            self.render()
            self.is_button_pressed = 1

        # indicates if button was released
        elif e.type is pygame.MOUSEBUTTONUP and self.is_button_pressed:
            self.press()
            self.is_button_pressed = 0
