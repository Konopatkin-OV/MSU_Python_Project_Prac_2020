"""__init__.py
==================================
Initializes game application and starts initialized game application.
"""
from Sokoban.BaseApp import Application
from Sokoban.moveBoxesGame import MoveBoxesGame
from Sokoban.menu import Menu
from Sokoban.editing.editor import LevelEditor
from Sokoban.choose_level import ChooseLevel
from Sokoban.settings import Settings

import sys
import os.path
import gettext


def init():
    '''Initializes game application.'''
    datapath = os.path.dirname(sys.argv[0])
    gettext.install('BaseApp', datapath)
    global app
    app = Application()
    MoveBoxesGame(app, 'moveBoxesGame')
    LevelEditor(app, "NewLevel")
    ChooseLevel(app, 'ChooseLevel0')
    Settings(app, 'Settings')
    Menu(app, '__main__')


def run():
    '''Starts initialized game application.'''
    app.start()


if __name__ == '__main__':
    init()
    run()
