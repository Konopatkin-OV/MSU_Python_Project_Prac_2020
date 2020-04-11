from gui import GUI
from levels import Level
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
        self.images['background'] = pygame.image.Surface(self.application.screen.get_size()).fill((0, 0, 0))
        self.images['free_cell'] = pygame.image.Surface((64, 64)).fill((150, 150, 150))
        self.images['wall'] = pygame.image.Surface((64, 64)).fill((200, 100, 100))
        self.images['box_cell'] = pygame.image.Surface((64, 64)).fill((100, 100, 200))
        self.images['player'] = pygame.image.Surface((64, 64)).fill((50, 200, 50))
        self.images['box'] = pygame.image.Surface((64, 64)).fill((100, 50, 0))

    def set_image(self, name, image):
        self.images[name] = image

    def render(self):
        screen = self.application.screen

        screen.blit(self.images['background'], (0, 0))

        # compute cell size and offset to render the field fully in the center of screen
        c_w, c_h = self.current_level.dimensions
        s_w, s_h = screen.get_size()
        cell_size = min(s_w / c_w, s_h / c_h)
        off_x, off_y = ((s_w - cell_size * c_w) / 2, (s_h - cell_size * c_h) / 2)

        # render cells
        for x in range(c_w):
            for y in range(c_h):
                if self.current_level.field[x][y]:
                    cur_img = self.images['free_cell']
                else:
                    cur_img = self.images['wall']
                screen.blit(cur_img, (off_x + x * cell_size, off_y + y * cell_size))

        # render objects
        for x, y in self.current_level.places_for_boxes:
            screen.blit(self.images['box_cell'], (off_x + x * cell_size, off_y + y * cell_size))

        for box in self.current_level.boxes:
            x, y = box.x, box.y
            screen.blit(self.images['box'], (off_x + x * cell_size, off_y + y * cell_size))

        x, y = self.current_level.player.x, self.current_level.player.y
        screen.blit(self.images['player'], (off_x + x * cell_size, off_y + y * cell_size))

        pygame.screen.update()


if __name__ == '__main__':
    app = Application()
    gui = MoveBoxesGame(app, '__main__')
    app.start()
