import pygame
import pygame.locals
from levels import Level


# the main application class which initialises pygame and rules over interfaces...
class Application(object):
    def __init__(self, app_name="Test application", screen_size=(1280, 720), max_fps=60):
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

        # something like the main application cycle but only switching interfaces like a stack
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


# the interface class which runs the main cycle
# can be inherited and used for menu or specific game modes
class GUI(object):
    def __init__(self, app, name='__main__'):
        self.application = app
        app.add_gui(self, name)

    # renders the GUI in the application
    def render(self):
        pygame.display.update()

    # events handler
    def process_event(self, event):
        return

    # time handler, delta_t - time from the last call
    def process_frame(self, delta_t):
        return

    # main application cycle for current GUI
    def run(self):
        running = True
        return_value = None
        self.application.clock.tick() # ignore previous loading time
        while running:
            # process all incoming events
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    running = False
                    return_value = -1
                else:
                    res = self.process_event(event)
                    # cannot close the whole application from anything other than QUIT
                    # but can go to another interface
                    if res == -1:
                        running = False
                        return_value = None
                    elif res is not None:
                        running = False
                        return_value = res

            # get time passed since last frame, 
            # plus wait until the whole frame time passed
            delta_t = self.application.clock.tick(self.application.max_fps)

            # if application is lagging, makes it slower to allow 
            # getting through all the computations required...
            delta_t = 1 / self.application.max_fps

            res = self.process_frame(delta_t)
            # maybe interface can close itself after some time?
            if res == -1:
                running = False
                return_value = None
            elif res is not None:
                running = False
                return_value = res

            self.render()

        return return_value




if __name__ == '__main__':
    app = Application()
    gui = GUI(app, '__main__')
    # lvl0 = Level(app, '0')
    app.start()

