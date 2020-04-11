from gui import GUI
from levels import Level
import os
import pygame
import pygame.locals


class MoveBoxesGame(GUI):
    def __init__(self, app, name):
        super().__init__(app, name)

        self.levels = {}

        root, dirs, files = next(os.walk('lvls/', topdown=True))
        for name in files:
            if name.endswith('.lvl'):
                name = name[:-4]
                self.levels[name] = Level(name)

        self.current_level = self.levels['0']

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
        self.images['player'].fill((50, 200, 50))
        self.images['box'] = pygame.surface.Surface((64, 64))
        self.images['box'].fill((100, 50, 0))

    def set_image(self, name, image):
        self.images[name] = image

    def render(self):
        screen = self.application.screen

        screen.fill((0, 0, 0))
        screen.blit(self.images['background'], (0, 0))

        # compute cell size and offset to render the field fully in the center of screen
        c_h, c_w = self.current_level.dimensions # why do transpose in level???
        s_w, s_h = screen.get_size()
        cell_size = int(min(s_w / c_w, s_h / c_h))
        off_x, off_y = ((s_w - cell_size * c_w) / 2, (s_h - cell_size * c_h) / 2)

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

        pygame.display.update()

    def process_event(self, event):
        if event.type == pygame.locals.KEYDOWN:
            pass


if __name__ == '__main__':
    from BaseApp import Application
    app = Application()
    gui = MoveBoxesGame(app, '__main__')
    app.start()
