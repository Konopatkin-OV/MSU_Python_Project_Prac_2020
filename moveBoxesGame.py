from gui import GUI
from level import Level
import os
import pygame
import pygame.locals
import button
from label import Label, LABEL_SIZE
from image import WALL_IMAGE, FREE_CELL_IMAGE, \
    BOX_CELL_IMAGE, PLAYER_IMAGE, BOX_IMAGE


class MoveBoxesGame(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)

        self.levels = []

        root, dirs, files = next(os.walk('levels/', topdown=True))
#        for name in sorted(files, key=lambda x: os.path.getmtime(os.path.abspath(f'levels/{x}'))):
        for name in files:
            if name.endswith('.lvl'):
                name = name[:-4]
                try:
                    self.levels.append(Level(name))
                except Exception:
                    print(f'Level {name} is not valid.')
        self.levels.sort(key=lambda level: level.order)

        self.current_index = 1
        self.current_level = self.levels[self.current_index]

        # images for game objects
        # default monochrome colors
        self.images = {}
        self.images['background'] = pygame.Surface(self.application.screen.get_size())
        self.images['background'].fill((0, 0, 0))
        self.images['free_cell'] = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.images['free_cell'].blit(FREE_CELL_IMAGE, (0, 0))
        self.images['wall'] = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.images['wall'].blit(WALL_IMAGE, (0, 0))
        self.images['box_cell'] = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.images['box_cell'].blit(BOX_CELL_IMAGE, (0, 0))
        self.images['player'] = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.images['player'].blit(PLAYER_IMAGE, (0, 0))
        self.images['box'] = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.images['box'].blit(BOX_IMAGE, (0, 0))
        self.images['grab'] = pygame.Surface((64, 64), flags=pygame.locals.SRCALPHA)
        self.images['grab'].fill((0, 0, 0, 0))
        pygame.draw.circle(self.images['grab'], (50, 100, 200), (32, 32), 25, 4)

        # game variables
        self.moves_made = 0
        self.level_finished = False
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

        # time in seconds to complete one step animation
        self.move_duration = 0.5

        # animation parameters
        self.is_moving = False
        self.moving_time = 0.0
        self.moving_old_poses = {'player': None, 'box': None}

        # buttons
        self.buttons = {}
        screen = self.application.screen

        # button to menu
        button_event = pygame.event.Event(pygame.USEREVENT, {'name': '__main__'})
        self.buttons['menu'] = button.Button(_('MENU'), screen, button_event, (0, 0))

        # next level button
        w = screen.get_width() - button.BUTTON_SIZE[0]
        button_event = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame',
                                                             'lvl': 'next'})
        self.buttons['next_lvl'] = button.Button(_('NEXT'), screen, button_event, (w, 0))

        # previous level button
        h = 3 * button.BUTTON_SIZE[1] / 2
        button_event = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame',
                                                             'lvl': 'this'})
        self.buttons['reset'] = button.Button(_('RESET'), screen, button_event, (w, h))

        # restart button
        w -= 5 * button.BUTTON_SIZE[0] / 4
        button_event = pygame.event.Event(pygame.USEREVENT, {'name': 'moveBoxesGame',
                                                             'lvl': 'previous'})
        self.buttons['prev_lvl'] = button.Button(_('PREVIOUS'), screen, button_event, (w, 0))

        # control buttons
        button_size = 35, 35
        button_color = pygame.Color(50, 50, 50)
        font_size = 15

        w = screen.get_width() - 13 * button_size[0] / 4
        h = screen.get_height() - 6 * button_size[1]

        button_event = pygame.event.Event(pygame.locals.KEYDOWN)
        button_event.key = pygame.locals.K_UP
        b_up = button.Button(_('up'), screen, button_event, (w, h),
                             button_size, button_color, font_size)
        self.buttons[0] = b_up

        button_size_1 = 46, 30
        h += button_size[1] + button_size_1[1] / 2
        w -= button_size_1[0] / 2 - button_size[0] / 2
        button_event = pygame.event.Event(pygame.locals.KEYDOWN)
        button_event.key = pygame.locals.K_DOWN
        b_down = button.Button(_('down'), screen, button_event, (w, h),
                               button_size_1, button_color, font_size)
        self.buttons[1] = b_down

        w -= 5 * button_size[0] / 3
        h = screen.get_height() - 5 * button_size[1]
        button_event = pygame.event.Event(pygame.locals.KEYDOWN)
        button_event.key = pygame.locals.K_LEFT
        b_left = button.Button(_('left'), screen, button_event, (w, h),
                               button_size_1, button_color, font_size)
        self.buttons[2] = b_left

        w += 10 * button_size[0] / 3
        button_event = pygame.event.Event(pygame.locals.KEYDOWN)
        button_event.key = pygame.locals.K_RIGHT
        b_right = button.Button(_('right'), screen, button_event, (w, h),
                                button_size_1, button_color, font_size)
        self.buttons[3] = b_right

        button_size_2 = 100, 30
        w = screen.get_width() - 13 * button_size[0] / 4 - (button_size_2[0] / 2 -
                                                            button_size[0] / 2)
        h += 2 * button_size[1]
        button_event = pygame.event.Event(pygame.locals.KEYDOWN)
        button_event.key = pygame.locals.K_e
        b_grab = button.Button(_('grab'), screen, button_event, (w, h),
                               button_size_2, button_color, font_size)
        self.buttons['grab'] = b_grab

        # labels
        self.labels = []

        # current level label
        w = screen.get_width() / 2 - LABEL_SIZE[0] / 2
        self.labels.append(Label(screen, (w, 0)))

        # current moves amount
        h = screen.get_height() - LABEL_SIZE[1]
        self.labels.append(Label(screen, (0, h)))

        # success label
        w = screen.get_width() - LABEL_SIZE[0]
        h = screen.get_height() / 2 - LABEL_SIZE[1] / 2
        self.labels.append(Label(screen, (w, h), font_size=25))
        self.success_str = ''

    def set_image(self, name, image):
        self.images[name] = image

    def process_frame(self, delta_t):
        if self.is_moving:
            self.moving_time += delta_t
            if self.moving_time >= self.move_duration:
                self.is_moving = False
                self.moving_time = 0.0

    def start_move(self, player_goal, box_goal=None):
        if not self.is_moving:
            if self.move_duration > 0.0:
                self.is_moving = True
                self.moving_time = 0.0
                self.moving_old_poses['player'] = self.current_level.player.get_pos()
                if self.grabbed_box is not None:
                    self.moving_old_poses['box'] = self.grabbed_box.get_pos()

            self.current_level.player.move(*player_goal)
            if self.grabbed_box is not None and box_goal is not None:
                self.grabbed_box.move(*box_goal)
            self.moves_made += 1

    # renders one square object, maybe moving
    # because copypasting is evil!
    def render_sq_object(self, image, size, offset, cell_size, pos, old_move_pos=None):
        x, y = pos
        image = pygame.transform.smoothscale(image, (size, size))
        if old_move_pos is not None:
            old_x, old_y = old_move_pos
            progress = (1.0 - self.moving_time / self.move_duration)
            move_off_x = (old_x - x) * progress
            move_off_y = (old_y - y) * progress
            self.application.screen.blit(image,
                                         (int(offset[0] + (x + move_off_x + 0.5) *
                                              cell_size - size / 2),
                                          int(offset[1] + (y + move_off_y + 0.5) *
                                              cell_size - size / 2)))
        else:
            self.application.screen.blit(image,
                                         (int(offset[0] + (x + 0.5) * cell_size - size / 2),
                                          int(offset[1] + (y + 0.5) * cell_size - size / 2)))

    def check_level_finish(self):
        if self.current_level.is_complete():
            self.level_finished = True
            self.success_str = _("SUCCESS!")

    def render(self):
        screen = self.application.screen

        screen.fill((0, 0, 0))
        screen.blit(self.images['background'], (0, 0))

        # allocate center part of screen to the game field and borders to menu elements
        game_field_offset = (200, LABEL_SIZE[1])
        gf_off_x, gf_off_y = game_field_offset
        s_w, s_h = screen.get_size()
        s_w -= 2 * gf_off_x
        s_h -= 2 * gf_off_y

        # rendering the game field
        # compute cell size and offset to render the field fully in the center of screen
        c_w, c_h = self.current_level.width, self.current_level.height
        cell_size = int(min(s_w / c_w, s_h / c_h))
        off_x, off_y = (gf_off_x + (s_w - cell_size * c_w) / 2,
                        gf_off_y + (s_h - cell_size * c_h) / 2)
        offset = off_x, off_y

        cur_img_free = pygame.transform.smoothscale(self.images['free_cell'],
                                                    (cell_size, cell_size))
        cur_img_wall = pygame.transform.smoothscale(self.images['wall'],
                                                    (cell_size, cell_size))
        # render cells
        for x in range(c_w):
            for y in range(c_h):
                if self.current_level.field[x][y]:
                    cur_img = cur_img_free
                else:
                    cur_img = cur_img_wall
                screen.blit(cur_img, (off_x + x * cell_size, off_y + y * cell_size))

        # render objects
        cur_img = pygame.transform.smoothscale(self.images['box_cell'], (cell_size, cell_size))
        for x, y in self.current_level.box_cells:
            screen.blit(cur_img, (off_x + x * cell_size, off_y + y * cell_size))

        cur_img = pygame.transform.smoothscale(self.images['box'], (cell_size, cell_size))
        for box in self.current_level.boxes:
            if self.is_moving and self.grabbed_box is not None and box is self.grabbed_box:
                old_pos = self.moving_old_poses['box']
            else:
                old_pos = None
            self.render_sq_object(self.images['box'], cell_size, offset,
                                  cell_size, box.get_pos(), old_pos)

        self.render_sq_object(self.images['player'], cell_size, offset, cell_size,
                              self.current_level.player.get_pos(),
                              self.moving_old_poses['player'] if self.is_moving else None)

        # magic grabbing circle on player trying to grab or on the grabbed box
        if self.grabbed_box is not None or self.attempting_grabbing:
            if self.grabbed_box is not None:
                pos = self.grabbed_box.get_pos()
            else:
                pos = self.current_level.player.get_pos()
            self.render_sq_object(self.images['grab'], cell_size, offset, cell_size, pos,
                                  self.moving_old_poses['box'] if self.is_moving else None)

        # render menu elements (TODO)
        for k, b in self.buttons.items():
            b.render()

        # render labels
        if self.current_level.name.isdigit() and len(self.current_level.name) < 4:
            level_name = _('LEVEL ') + str(self.current_level.name)
        else:
            level_name = self.current_level.name
        self.labels[0].render(level_name, True)
        self.labels[1].render(_('Moves: ') + str(self.moves_made), True)
        self.labels[2].render(self.success_str, True)

        pygame.display.update()

    def process_event(self, event):
        # press a button
        for k, b in self.buttons.items():
            b.process_event(event)

        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                return -1
            elif event.key == self.keys["reset"]:
                self.reset()
            elif event.key == self.keys["grab"]:
                if not self.is_moving:
                    if self.grabbed_box is not None:
                        self.grabbed_box = None
                    else:
                        self.attempting_grabbing = not self.attempting_grabbing
            elif event.key == self.keys["next_lvl"]:
                if self.level_finished:
                    self.reset()
                    if self.current_index < len(self.levels) - 1:
                        self.select_level(self.current_index + 1)
                    else:
                        return '__main__'
                else:
                    self.success_str = _('Level is not comlete')
                    print(f'Level {self.current_level.name} is not complete.')
            elif event.key == self.keys["prev_lvl"]:
                self.reset()
                if self.current_index > 0:
                    self.select_level(self.current_index - 1)
                else:
                    return '__main__'
            elif event.key in self.keys["move"]:
                # try moving, still no collision checking
                # get direction of moving
                cur_dir = self.move_dirs[self.keys["move"][event.key]]
                dx, dy = cur_dir

                x, y = self.current_level.player.get_pos()
                g_x, g_y = x + dx, y + dy  # goal cell

                if self.attempting_grabbing:
                    box = self.current_level.get_box(g_x, g_y)
                    if box is not None:
                        self.grabbed_box = box
                        self.attempting_grabbing = False
                elif self.grabbed_box is not None:
                    b_x, b_y = self.grabbed_box.get_pos()
                    # dir to grabbed box and goal cell of grabbed box
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
                            if self.current_level.is_empty(g_x, g_y) and \
                                    self.current_level.is_empty(bg_x, bg_y):
                                good_move = True
                    if good_move:
                        self.start_move((g_x, g_y), (bg_x, bg_y))
                        self.check_level_finish()
                else:
                    if self.current_level.is_empty(g_x, g_y):
                        self.start_move((g_x, g_y))
                        self.check_level_finish()

        elif event.type == pygame.locals.USEREVENT:
            if event.name == '__main__':
                self.reset()
                return event.name
            elif event.name == 'moveBoxesGame':
                if event.lvl == 'next':
                    if self.level_finished:
                        self.reset()
                        if self.current_index < len(self.levels) - 1:
                            self.select_level(self.current_index + 1)
                        else:
                            self.reset()
                            return '__main__'
                    else:
                        self.success_str = _('Level is not comlete')
                        print(f'Level {self.current_level.name} is not complete.')
                elif event.lvl == 'this':
                    self.reset()
                elif event.lvl == 'previous':
                    self.reset()
                    if self.current_index > 0:
                        self.select_level(self.current_index - 1)
                    else:
                        return '__main__'

    def add_level(self, level: Level) -> int:
        index = len(self.levels)
        self.levels.append(level)
        return index

    def reset(self):
        self.current_level.reset()
        self.moves_made = 0
        self.level_finished = False
        self.attempting_grabbing = False
        self.grabbed_box = None
        self.success_str = ''

        self.is_moving = False
        self.moving_time = 0.0

    def select_level(self, index: int):
        self.current_index = index
        self.current_level = self.levels[index]


if __name__ == '__main__':
    from BaseApp import Application

    app = Application()
    gui = MoveBoxesGame(app, '__main__')
    app.start()
