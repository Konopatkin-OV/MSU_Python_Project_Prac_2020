"""BaseApp.py - main application.
=================================
Initializes pygame and rules over interfaces.
"""
import pygame
import pygame.locals


class Application(object):
    def __init__(self, app_name="Test application",
                 screen_size=(1280, 720), max_fps=60):
        """Initialize pygame, display screen object and clock timer."""
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(app_name)
        self.GUIs = {}
        self.max_fps = max_fps

    def add_gui(self, gui, name):
        """Add interface to map, mainly used from initialised interfaces."""
        self.GUIs[name] = gui

    def start(self):
        """Run the application from the main interface."""
        if '__main__' in self.GUIs:
            cur_guis = [self.GUIs['__main__']]
        else:
            # maybe raise something nasty?
            return

        # the main application cycle but only switching interfaces like a stack
        running = True
        while running:
            res = cur_guis[-1].run()
            # if the application is closed
            if res == -1:
                running = False
            # if subinterface is called
            elif res is not None:
                cur_guis.append(self.GUIs[res])
            # if subinterface finished work
            else:
                cur_guis.pop()
                if not cur_guis:
                    # stop application if the main interface finished work
                    running = False
        pygame.quit()
