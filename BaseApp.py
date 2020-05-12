import pygame
import pygame.locals
from moveBoxesGame import MoveBoxesGame
from menu import Menu
from editing.editor import LevelEditor

import sys
import os.path
import gettext


# the main application class which initialises pygame and rules over interfaces
class Application(object):
    def __init__(self, app_name="Test application",
                 screen_size=(1280, 720), max_fps=60):
        # initialise pygame, display screen object and clock timer
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(app_name)
        self.GUIs = {}
        self.max_fps = max_fps

    # add interface to map, mainly used from initialised interfaces
    def add_gui(self, gui, name):
        self.GUIs[name] = gui

    # run the application from the main interface
    def start(self):
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


if __name__ == '__main__':
    datapath = os.path.dirname(sys.argv[0])
    gettext.install('BaseApp', datapath)
    app = Application()
    gui = MoveBoxesGame(app, 'moveBoxesGame')
    levelEditor = LevelEditor(app, "NewLevel")
    menu = Menu(app, '__main__')
    app.start()
