import pygame
from gui import GUI
import button
import moveBoxesGame
import menu
import label

FRAME_WIDTH = 3


class Controls(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)
        screen = self.application.screen

        # background 
        bg_coord = screen.get_width() / 2 - 2 * button.BUTTON_SIZE[0], 2 * label.LABEL_SIZE[1]
        self.bg_rect = pygame.Rect(bg_coord, (4 * button.BUTTON_SIZE[0], screen.get_height() - 3 * label.LABEL_SIZE[1]))
        frame_coord = self.bg_rect.left + FRAME_WIDTH, self.bg_rect.top + FRAME_WIDTH
        frame_size = 4 * button.BUTTON_SIZE[0] - 2 * FRAME_WIDTH, screen.get_height() - 3 * label.LABEL_SIZE[
            1] - 2 * FRAME_WIDTH
        self.frame_rect = pygame.Rect(frame_coord, frame_size)

        # buttons list
        self.B = []
        # labels list
        self.L = []

        gui = self.application.GUIs['moveBoxesGame']

        w1 = screen.get_width() / 2 - 5 * button.BUTTON_SIZE[0] / 4
        w = screen.get_width() / 2 + button.BUTTON_SIZE[0] / 4
        button_num = 9
        num_buttons_per_screen = screen.get_height() / 2 / button.BUTTON_SIZE[1]
        offset = (num_buttons_per_screen - button_num) / 2

        w2 = screen.get_width() / 2 - label.LABEL_SIZE[0] / 2
        self.label = (label.Label(screen, (w2, 0), color=pygame.Color(70, 50, 70)))

        # control buttons and labels

        h = offset * 3 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': "grab"})
        self.B.append(button.Button('E', screen, e, (w, h)))

        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'grab'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 0})
        self.B.append(button.Button('UP', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'up'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 1})
        self.B.append(button.Button('DOWN', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'down'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 2})
        self.B.append(button.Button('LEFT', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'left'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 3})
        self.B.append(button.Button('RIGHT', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'right'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 'prev_lvl'})
        self.B.append(button.Button('PG DOWN', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'prev lvl'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 'next_lvl'})
        self.B.append(button.Button('PG UP', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'next lvl'))

        h += 2 * button.BUTTON_SIZE[1]
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame', 'move': 'reset'})
        self.B.append(button.Button('R', screen, e, (w, h)))
        self.L.append((label.Label(screen, (w1, h), label_size=(button.BUTTON_SIZE[0],
                                                                button.BUTTON_SIZE[1] + 3),
                                   color=pygame.Color(70, 50, 70)), 'reset'))

        # button to menu
        h += 2 * button.BUTTON_SIZE[1]
        w1 += 3 * button.BUTTON_SIZE[0] / 4
        e = pygame.event.Event(pygame.USEREVENT, {'name': 'Settings'})
        self.B.append(button.Button('BACK', screen, e, (w1, h)))

        self.move = -1

    """Button rendering."""

    def render(self):
        screen = self.application.screen
        screen.fill((0, 0, 0))
        screen.fill(pygame.Color(100, 80, 100), self.bg_rect)
        screen.fill(pygame.Color(0, 0, 0), self.frame_rect)

        for b in self.B:
            b.render()
        for l in self.L:
            l[0].render(l[1])
        self.label.render('CONTROLS')
        pygame.display.update()

    """Check key values collision."""

    def buttons_collision(self, name, value):
        gui = self.application.GUIs['moveBoxesGame']
        return value in gui.keys.values() or value in gui.keys['move'].keys()

    """Button event handler."""

    def process_event(self, e):
        gui = self.application.GUIs['moveBoxesGame']

        # press a button
        for b in self.B:
            b.process_event(e)
            if b.is_button_pressed:
                self.pressed_button = b
                return

        if e.type == pygame.USEREVENT:
            if e.name == 'moveBoxesGame':
                self.move = e.move
            elif e.name == 'Settings':
                return e.name
        elif e.type == pygame.KEYDOWN:
            if self.move != -1 and not self.buttons_collision(self.move, e.key):
                if isinstance(self.move, str):
                    gui.keys[self.move] = e.key
                    if self.move == 'grab':
                        gui.buttons[self.move].event.key = e.key
                else:
                    for key, value in gui.keys['move'].items():
                        if value == self.move:
                            gui.keys['move'].update({e.key: gui.keys['move'].pop(key)})
                            gui.buttons[self.move].event.key = e.key
                            break
                if e.unicode.isalpha():
                    self.pressed_button.name = e.unicode.upper()
                elif e.key == pygame.K_BACKSPACE:
                    self.pressed_button.name = '<--'
                elif e.key == pygame.K_UP:
                    self.pressed_button.name = 'UP'
                elif e.key == pygame.K_DOWN:
                    self.pressed_button.name = 'DOWN'
                elif e.key == pygame.K_LEFT:
                    self.pressed_button.name = 'LEFT'
                elif e.key == pygame.K_RIGHT:
                    self.pressed_button.name = 'RIGHT'
                elif e.key == pygame.K_SPACE:
                    self.pressed_button.name = 'SPACE'
                elif e.key == pygame.K_RETURN:
                    self.pressed_button.name = "ENTER"
                elif e.key == pygame.K_PAGEDOWN:
                    self.pressed_button.name = "PG DOWN"
                elif e.key == pygame.K_PAGEUP:
                    self.pressed_button.name = "PG UP"
                else:
                    self.pressed_button.name = e.unicode
                self.move = -1
