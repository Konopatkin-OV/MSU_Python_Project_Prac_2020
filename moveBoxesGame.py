from gui import GUI
from levels import Level
import os
import pygame
import pygame.locals
import menu
import button

class MoveBoxesGame(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)

        self.levels = {}

        root, dirs, files = next(os.walk('lvls/', topdown=True))
        for name in files:
            if name.endswith('.lvl'):
                name = name[:-4]
                try:
                    self.levels[name] = Level(name)
                except IOError:
                    print(f'Level {name} is not valid.')

        self.current_level = self.levels['1']

        # images for game objects
        # default monochrome colors
        self.images = {}
        self.images['background'] = pygame.surface.Surface(self.application.screen.get_size())
        self.images['background'].fill((0, 0, 0))
        self.images['free_cell'] = pygame.surface.Surface((64, 64))
        self.images['free_cell'].fill((150, 150, 150))
        self.images['wall'] = pygame.surface.Surface((64, 64))
        self.images['wall'].fill((200, 100, 100))
        self.images['box_cell'] = pygame.surface.Surface((64, 64))
        self.images['box_cell'].fill((100, 100, 200))
        self.images['player'] = pygame.surface.Surface((64, 64))
        self.images['player'].fill((50, 150, 50))
        self.images['box'] = pygame.surface.Surface((64, 64))
        self.images['box'].fill((100, 50, 0))
        self.images['grab'] = pygame.surface.Surface((64, 64), flags=pygame.locals.SRCALPHA)
        self.images['grab'].fill((0, 0, 0, 0))
        pygame.draw.circle(self.images['grab'], (50, 100, 200), (32, 32), 25, 4)

        # game variables
        self.moves_made = 0
        self.attempting_grabbing = False
        self.grabbed_box = None

        self.keys = {"reset": pygame.locals.K_r,
                     "grab": pygame.locals.K_e,
                     "next_lvl": pygame.locals.K_PAGEUP,
                     "prev_lvl": pygame.locals.K_PAGEDOWN,
                     "move": {pygame.locals.K_UP: 0,
                              pygame.locals.K_DOWN: 1,
                              pygame.locals.K_LEFT: 2,
                              pygame.locals.K_RIGHT: 3}
                    }

        self.move_dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))

        # False if player can only push boxes
        self.allow_all_box_moves = True

    def set_image(self, name, image):
        self.images[name] = image

    def render(self):
        screen = self.application.screen

        screen.fill((0, 0, 0))
        screen.blit(self.images['background'], (0, 0))

        # allocate center part of screen to the game field and borders to menu elements
        game_field_offset = (200, 20)
        gf_off_x, gf_off_y = game_field_offset
        s_w, s_h = screen.get_size()
        s_w -= 2 * gf_off_x
        s_h -= 2 * gf_off_y

        # rendering the game field
        # compute cell size and offset to render the field fully in the center of screen
        c_w, c_h = self.current_level.dimensions
        cell_size = int(min(s_w / c_w, s_h / c_h))
        off_x, off_y = (gf_off_x + (s_w - cell_size * c_w) / 2, gf_off_y + (s_h - cell_size * c_h) / 2)

        cur_img_free = pygame.transform.scale(self.images['free_cell'], (cell_size, cell_size))
        cur_img_wall = pygame.transform.scale(self.images['wall'], (cell_size, cell_size))
        # render cells
        for x in range(c_w):
            for y in range(c_h):
                if self.current_level.field[x][y]:
                    cur_img = cur_img_free
                else:
                    cur_img = cur_img_wall
                screen.blit(cur_img, (off_x + x * cell_size, off_y + y * cell_size))

        # render objects
        cur_img = pygame.transform.scale(self.images['box_cell'], (cell_size, cell_size))
        for x, y in self.current_level.places_for_boxes:
            screen.blit(cur_img, (off_x + x * cell_size, off_y + y * cell_size))

        # moving objects should be a bit smaller than a whole cell?
        moving_coeff = 0.9
        delta_s = int((1.0 - moving_coeff) * cell_size)
        cur_img = pygame.transform.scale(self.images['box'], (cell_size - delta_s, cell_size - delta_s))
        for box in self.current_level.boxes:
            x, y = box.x, box.y
            screen.blit(cur_img, (off_x + x * cell_size + delta_s // 2, off_y + y * cell_size + delta_s // 2))

        x, y = self.current_level.player.x, self.current_level.player.y
        cur_img = pygame.transform.scale(self.images['player'], (cell_size - delta_s, cell_size - delta_s))
        screen.blit(cur_img, (off_x + x * cell_size + delta_s // 2, off_y + y * cell_size + delta_s // 2))

        # magic grabbing circle on player trying to grab or on the grabbed box
        if self.grabbed_box is not None or self.attempting_grabbing:
            if self.grabbed_box is not None:
                x, y = self.grabbed_box.x, self.grabbed_box.y
            else:
                x, y = self.current_level.player.x, self.current_level.player.y
            cur_img = pygame.transform.scale(self.images['grab'], (cell_size - delta_s, cell_size - delta_s))
            screen.blit(cur_img, (off_x + x * cell_size + delta_s // 2, off_y + y * cell_size + delta_s // 2))

        # render menu elements (TODO)
        # button to menu
        button_event = pygame.event.Event(pygame.USEREVENT, 
                              {'app': self.application, 'name': '__main__'})
        self.button = button.Button('MENU', screen, button_event, (0,0))        


        pygame.display.update()

    def process_event(self, event):
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                return -1
            elif event.key == self.keys["reset"]:
                self.reset()
            elif event.key == self.keys["grab"]:
                if self.grabbed_box is not None:
                    self.grabbed_box = None
                else:
                    self.attempting_grabbing = not self.attempting_grabbing
            elif event.key in self.keys["move"]:
                # try moving, still no collision checking
                # get direction of moving
                cur_dir = self.move_dirs[self.keys["move"][event.key]]
                dx, dy = cur_dir
                x, y = self.current_level.player.x, self.current_level.player.y
                c_w, c_h = self.current_level.dimensions
                g_x, g_y = x + dx, y + dy # goal cell

                if self.attempting_grabbing:
                    box = self.current_level.get_box(g_x, g_y)
                    if box is not None:
                        self.grabbed_box = box
                        self.attempting_grabbing = False
                elif self.grabbed_box is not None:
                    b_x, b_y = self.grabbed_box.x, self.grabbed_box.y
                    # dir to grabbed box and goal cell of grabbed box
                    bd_x, bd_y = b_x - x, b_y - y
                    bg_x, bg_y = b_x + dx, b_y + dy

                    good_move = False
                    if g_x == b_x and g_y == b_y:
                        if self.current_level.is_empty(bg_x, bg_y):
                            good_move = True
                    elif self.allow_all_box_moves:
                        if bg_x == x and bg_y == y:
                            if self.current_level.is_empty(g_x, g_y):
                                good_move = True
                        else:
                            if self.current_level.is_empty(g_x, g_y) and\
                               self.current_level.is_empty(bg_x, bg_y):
                                good_move = True
                    if good_move:
                        self.current_level.player.move(g_x, g_y)
                        self.grabbed_box.move(bg_x, bg_y)
                else:
                    if self.current_level.is_empty(g_x, g_y):
                        self.current_level.player.move(g_x, g_y)
        
        # press a button
        elif event.type == pygame.locals.MOUSEBUTTONDOWN and self.button.rect.collidepoint(event.pos):
            self.button.press()
        elif event.type == pygame.locals.USEREVENT:
            menu.Menu(event.app, event.name)
            return event.name
    
    def reset(self):
        self.current_level.reset()
        self.moves_made = 0
        self.attempting_grabbing = False
        self.grabbed_box = None


if __name__ == '__main__':
    from BaseApp import Application
    app = Application()
    gui = MoveBoxesGame(app, '__main__')
    app.start()
