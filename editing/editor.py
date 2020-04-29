from gui import GUI
import pygame
from pygame.event import Event
from pygame import Surface, Rect, SRCALPHA
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
from pygame.transform import smoothscale
from editing.customlevel import CustomLevel
from button import Button, BUTTON_SIZE
from textbox import TextBox, TEXTBOX_SIZE
from image import WALL_IMAGE, FREE_CELL_IMAGE, \
    BOX_CELL_IMAGE, PLAYER_IMAGE, BOX_IMAGE


class LevelEditor(GUI):
    def __init__(self, app, name: str):
        super().__init__(app, name)
        self.custom_level = CustomLevel()

        self.images = {'free_cell': Surface((128, 128), SRCALPHA),
                       'wall': Surface((128, 128), SRCALPHA),
                       'box_cell': Surface((128, 128), SRCALPHA),
                       'player': Surface((128, 128), SRCALPHA),
                       'box': Surface((128, 128), SRCALPHA)}

        self.images['free_cell'].blit(FREE_CELL_IMAGE, (0, 0))
        self.images['wall'].blit(WALL_IMAGE, (0, 0))
        self.images['box_cell'].blit(BOX_CELL_IMAGE, (0, 0))
        self.images['player'].blit(PLAYER_IMAGE, (0, 0))
        self.images['box'].blit(BOX_IMAGE, (0, 0))

        self.dragged_picture = None
        self.still_pictures = [StillPicture(' '),
                               StillPicture('b'),
                               StillPicture('p'),
                               StillPicture('x')]

        self.cell_size = None
        self.offset_x, self.offset_y = None, None
        self.symbols_to_images = {}
        self.calculate_cell_size()

        self.level_name_box = TextBox(
                                  self.application.screen, 
                                  (self.application.screen.get_width()/2 - TEXTBOX_SIZE[0]/2, 10))

        self.buttons = [
            Button(
                'MENU', self.application.screen,
                Event(pygame.USEREVENT,
                      {'app': self.application, 'name': '__main__'}), (0, 0)),
            Button(
                'SAVE',
                self.application.screen,
                Event(pygame.USEREVENT, {'app': self.application, 'name': 'save'}),
                (self.application.screen.get_width() - BUTTON_SIZE[0], 0)),
            Button(
                'OK',
                self.application.screen,
                Event(pygame.USEREVENT, {'app': self.application, 'name': 'ok'}),
                (self.level_name_box.rect_box.right + 10, self.level_name_box.rect.top),
                button_size = (40, 30))
        ]

    def clear(self):
        self.custom_level = CustomLevel()
        self.dragged_picture = None
        self.calculate_cell_size()

    def calculate_cell_size(self):
        reduction_x, reduction_y = 200, 20
        screen_width, screen_height = self.application.screen.get_size()
        screen_width -= 2 * reduction_x
        screen_height -= 2 * reduction_y

        # compute cell size and offset to render the field fully in the center of screen
        width, height = self.custom_level.width, self.custom_level.height
        space = 0.25
        height_for_pictures = len(self.still_pictures) * (1 + space) - space
        self.cell_size = int(
            min(screen_width / (width + 4),
                screen_height / max(height, height_for_pictures)))
        self.offset_x = int(
            reduction_x + (screen_width - self.cell_size * width) / 2)
        self.offset_y = int(
            reduction_y + (screen_height - self.cell_size * height) / 2)

        for i, still_picture in enumerate(self.still_pictures):
            still_picture.move(
                self.offset_x - 2 * self.cell_size,
                self.offset_y + ((height - height_for_pictures) / 2 +
                                 (1 + space) * i) * self.cell_size,
                self.cell_size)

        size = (self.cell_size, self.cell_size)
        self.symbols_to_images = {' ': smoothscale(self.images['free_cell'], size),
                                  'w': smoothscale(self.images['wall'], size),
                                  'p': smoothscale(self.images['player'], size),
                                  'b': smoothscale(self.images['box'], size),
                                  'x': smoothscale(self.images['box_cell'], size)}

    def render(self):
        screen = self.application.screen
        screen.fill((0, 0, 0))

        # render cells
        for x in range(self.custom_level.width):
            for y in range(self.custom_level.height):
                cell = self.custom_level.field[x][y]
                for symbol in cell:
                    screen.blit(self.symbols_to_images[symbol],
                                (self.offset_x + x * self.cell_size,
                                 self.offset_y + y * self.cell_size))
                if not cell:
                    screen.blit(self.symbols_to_images['w'],
                                (self.offset_x + x * self.cell_size,
                                 self.offset_y + y * self.cell_size))

        # render still pictures
        for still_picture in self.still_pictures:
            screen.blit(self.symbols_to_images[still_picture.symbol],
                        (still_picture.rect.x, still_picture.rect.y))

        # render a moving picture
        if self.dragged_picture is not None:
            screen.blit(self.symbols_to_images[self.dragged_picture.symbol],
                        (self.dragged_picture.x, self.dragged_picture.y))

        # render buttons
        for button in self.buttons:
            button.render()
        
        # render textbox
        self.level_name_box.render()

        pygame.display.update()

    def process_event(self, event: Event):
        # entering level name
        if self.level_name_box.start_writing:
            self.level_name_box.process_event(event)

        # press a button
        for button in self.buttons:
            button.process_event(event)
    
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.level_name_box.rect.collidepoint(event.pos):
                    self.level_name_box.start()
                    return

                if self.dragged_picture is None:
                    x, y = event.pos

                    for still_picture in self.still_pictures:
                        if still_picture.rect.collidepoint(*event.pos):
                            offset_x = x - still_picture.rect.x
                            offset_y = y - still_picture.rect.y
                            self.dragged_picture = DraggedPicture(
                                still_picture.symbol,
                                *still_picture.rect.topleft,
                                offset_x, offset_y)
                            return

                    field_x = int((x - self.offset_x) // self.cell_size)
                    field_y = int((y - self.offset_y) // self.cell_size)
                    symbol = self.custom_level.remove(field_x, field_y)
                    if symbol:
                        actual_x = field_x * self.cell_size + self.offset_x
                        actual_y = field_y * self.cell_size + self.offset_y
                        offset_x = x - actual_x
                        offset_y = y - actual_y
                        self.dragged_picture = DraggedPicture(
                            symbol, actual_x, actual_y, offset_x, offset_y)

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
                # user didn't save the name
                if self.level_name_box.str[-1] == '|':
                    self.level_name_box.str = 'my level'
                try:
                    level_name = self.application.GUIs["NewLevel"].level_name_box.str
                    name = self.custom_level.save(level_name)
                    # self.application.GUIs['moveBoxesGame'].add_level(name)
                    number_list = list(map(lambda s: s.replace('ChooseLevel', ''),
                                           list(filter(lambda s: s.startswith('ChooseLevel'), self.application.GUIs.keys()))))
                    max_number = max(list(map(int, number_list)))
                    self.application.GUIs[f'ChooseLevel{max_number}'].add_level(name)
                    self.clear()
                    self.level_name_box.str = 'my level'
                except IOError:
                    print('The level is not completed!')
                

class StillPicture:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.rect = Rect(0, 0, 0, 0)

    def move(self, x: int, y: int, cell_size: int):
        self.rect.width = cell_size
        self.rect.height = cell_size
        self.rect.topleft = x, y


class DraggedPicture:
    def __init__(self, symbol, x, y,
                 offset_x: int, offset_y: int):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y

    def move(self, x, y):
        self.x = x - self.offset_x
        self.y = y - self.offset_y
