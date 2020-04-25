from gui import GUI
import pygame
from pygame.event import Event
from pygame import Surface, Rect
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
from pygame.transform import scale
from editing.customlevel import CustomLevel
from button import Button, BUTTON_SIZE
from image import WALL_IMAGE, PATH_IMAGE, SPACE_IMAGE, PLAYER_IMAGE, BOX_IMAGE


class LevelEditor(GUI):
    def __init__(self, app, name: str):
        super().__init__(app, name)
        self.custom_level = CustomLevel(app)

        self.images = {'free_cell': Surface((128, 128)),
                       'wall': Surface((128, 128)),
                       'box_cell': Surface((128, 128)),
                       'player': Surface((128, 128)),
                       'box': Surface((128, 128))}

        self.images['free_cell'].blit(PATH_IMAGE, (0, 0))
        self.images['wall'].blit(WALL_IMAGE, (0, 0))
        self.images['box_cell'].blit(SPACE_IMAGE, (0, 0))
        self.images['player'].blit(PLAYER_IMAGE, (0, 0))
        self.images['box'].blit(BOX_IMAGE, (0, 0))

        self.dragged_picture = None
        self.still_pictures = [StillPicture(' '),
                               StillPicture('w'),
                               StillPicture('b'),
                               StillPicture('p'),
                               StillPicture('x')]

        self.cell_size = None
        self.offset_x, self.offset_y = None, None
        self.calculate_cell_size()

        self.buttons = [
            Button(
                'MENU', self.application.screen,
                Event(pygame.USEREVENT, {'app': self.application, 'name': '__main__'}),
                (0, 0)),
            Button(
                'SAVE',
                self.application.screen,
                Event(pygame.USEREVENT, {'app': self.application, 'name': 'save'}),
                (self.application.screen.get_width() - BUTTON_SIZE[0], 0))
        ]

    def clear(self):
        pass

    def calculate_cell_size(self):
        reduction_x, reduction_y = 200, 20
        screen_width, screen_height = self.application.screen.get_size()
        screen_width -= 2 * reduction_x
        screen_height -= 2 * reduction_y

        # compute cell size and offset to render the field fully in the center of screen
        width, height = self.custom_level.width, self.custom_level.height
        height_for_pictures = 7
        self.cell_size = int(min(screen_width / (width + 4), screen_height / max(height, height_for_pictures)))
        self.offset_x = int(reduction_x + (screen_width - self.cell_size * width) / 2)
        self.offset_y = int(reduction_y + (screen_height - self.cell_size * height) / 2)

        for i, still_picture in enumerate(self.still_pictures):
            still_picture.move(int(self.offset_x - 2 * self.cell_size),
                               int(self.offset_y + ((height - 7) / 2 + 1.5 * i) * self.cell_size),
                               self.cell_size)

    def render(self):
        screen = self.application.screen
        screen.fill((0, 0, 0))

        path_image = scale(self.images['free_cell'], (self.cell_size, self.cell_size))
        wall_image = scale(self.images['wall'], (self.cell_size, self.cell_size))
        box_cell_image = scale(self.images['box_cell'], (self.cell_size, self.cell_size))
        player_image = scale(self.images['player'], (self.cell_size, self.cell_size))
        box_image = scale(self.images['box'], (self.cell_size, self.cell_size))

        symbols_to_images = {' ': path_image,
                             'w': wall_image,
                             'p': player_image,
                             'b': box_image,
                             'x': box_cell_image}
        # render cells
        for x in range(self.custom_level.width):
            for y in range(self.custom_level.height):
                symbol = self.custom_level.field[x][y]
                screen.blit(symbols_to_images[symbol],
                            (self.offset_x + x * self.cell_size,
                             self.offset_y + y * self.cell_size))

        # render still pictures
        for still_picture in self.still_pictures:
            screen.blit(symbols_to_images[still_picture.symbol],
                        (still_picture.rect.x, still_picture.rect.y))

        # render a moving picture
        if self.dragged_picture is not None:
            screen.blit(symbols_to_images[self.dragged_picture.symbol],
                        (self.dragged_picture.x, self.dragged_picture.y))

        # render buttons
        for button in self.buttons:
            button.render()

        pygame.display.update()

    def process_event(self, event: Event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.dragged_picture is None:
                    x, y = event.pos
                    for still_picture in self.still_pictures:
                        if still_picture.rect.collidepoint(*event.pos):
                            offset_x = x - still_picture.rect.x
                            offset_y = y - still_picture.rect.y
                            self.dragged_picture = DraggedPicture(
                                still_picture, offset_x, offset_y)
                            return

                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.press()
                            return

        elif event.type == MOUSEMOTION:
            if self.dragged_picture is not None:
                self.dragged_picture.move(*event.pos)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 and self.dragged_picture is not None:
                screen_x, screen_y = event.pos
                field_x = int((screen_x - self.offset_x) // self.cell_size)
                field_y = int((screen_y - self.offset_y) // self.cell_size)
                self.custom_level.put(
                    self.dragged_picture.symbol, field_x, field_y)
                self.calculate_cell_size()
                self.dragged_picture = None

        elif event.type == pygame.locals.USEREVENT:
            if event.name == '__main__':
                return event.name
            elif event.name == 'save':
                self.custom_level.save()
                self.buttons[-1].color, self.buttons[-1].new_color = \
                    self.buttons[-1].new_color, self.buttons[-1].color


class StillPicture:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.rect = Rect(0, 0, 0, 0)

    def move(self, x: int, y: int, cell_size: int):
        self.rect.topleft = x, y
        self.rect.width = cell_size
        self.rect.height = cell_size


class DraggedPicture:
    def __init__(self, still_picture: StillPicture, offset_x: int, offset_y: int):
        self.symbol = still_picture.symbol
        self.x = still_picture.rect.x
        self.y = still_picture.rect.y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def move(self, x, y):
        self.x = x - self.offset_x
        self.y = y - self.offset_y


if __name__ == '__main__':
    from BaseApp import Application
    app = Application()
    gui = LevelEditor(app, '__main__')
    app.start()
