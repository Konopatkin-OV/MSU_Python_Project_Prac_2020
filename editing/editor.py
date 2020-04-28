from gui import GUI
import pygame
from pygame.event import Event
from pygame import Surface, Rect
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP
from pygame.transform import scale
from editing.customlevel import CustomLevel
from button import Button, BUTTON_SIZE
from textbox import TextBox, TEXTBOX_SIZE

class LevelEditor(GUI):
    def __init__(self, app, name: str):
        super().__init__(app, name)
        self.custom_level = CustomLevel(app)

        self.images = {'background': Surface(self.application.screen.get_size()),
                       'free_cell': Surface((64, 64)),
                       'wall': Surface((64, 64)),
                       'box_cell': Surface((64, 64)),
                       'player': Surface((64, 64)),
                       'box': Surface((64, 64))}

        self.images['background'].fill((0, 0, 0))
        self.images['free_cell'].fill((150, 150, 150))
        self.images['wall'].fill((200, 100, 100))
        self.images['box_cell'].fill((100, 100, 200))

        rect = Rect(3, 3, 58, 58)
        self.images['player'].fill((150, 150, 150))
        self.images['player'].fill((50, 150, 50), rect)
        self.images['box'].fill((150, 150, 150))
        self.images['box'].fill((100, 50, 0), rect)

        self.dragged_picture = None
        self.still_pictures = [StillPicture(' ', -2, -1),
                               StillPicture('w', -2, 0),
                               StillPicture('b', -2, 1),
                               StillPicture('p', -2, 2),
                               StillPicture('x', -2, 3)]

        self.cell_size = None
        self.offset_x, self.offset_y = None, None
        self.calculate_cell_size()

        self.level_name_box = TextBox(
                                  self.application.screen, 
                                  (self.application.screen.get_width()/2 - TEXTBOX_SIZE[0]/2, 10))

        self.buttons = [
            Button(
                'MENU', self.application.screen,
                Event(pygame.USEREVENT, {'app': self.application, 'name': '__main__'}),
                (0, 0)),
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
        pass

    def calculate_cell_size(self):
        reduction_x, reduction_y = 200, 20
        screen_width, screen_height = self.application.screen.get_size()
        screen_width -= 2 * reduction_x
        screen_height -= 2 * reduction_y

        # compute cell size and offset to render the field fully in the center of screen
        width, height = self.custom_level.width, self.custom_level.height
        height_for_pictures = len(self.still_pictures) + (height + 1) % 2
        self.cell_size = int(min(screen_width / (width + 4), screen_height / max(height, height_for_pictures)))
        self.offset_x = int(reduction_x + (screen_width - self.cell_size * width) / 2)
        self.offset_y = int(reduction_y + (screen_height - self.cell_size * height) / 2)

        for i, still_picture in enumerate(self.still_pictures):
            still_picture.y = i + \
                int((self.custom_level.height - len(self.still_pictures)) // 2)

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
                        (self.offset_x + still_picture.x * self.cell_size,
                         self.offset_y + still_picture.y * self.cell_size))

        # render a moving picture
        if self.dragged_picture is not None:
            screen.blit(symbols_to_images[self.dragged_picture.symbol],
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
                if self.dragged_picture is None:
                    screen_x, screen_y = event.pos
                    field_x = int((screen_x - self.offset_x) // self.cell_size)
                    field_y = int((screen_y - self.offset_y) // self.cell_size)
                    for still_picture in self.still_pictures:
                        if still_picture.x == field_x and still_picture.y == field_y:
                            x = still_picture.x * self.cell_size + self.offset_x
                            y = still_picture.y * self.cell_size + self.offset_y
                            offset_x = screen_x - x
                            offset_y = screen_y - y
                            self.dragged_picture = DraggedPicture(
                                still_picture.symbol, x, y, offset_x, offset_y)
                            return
 
            if self.level_name_box.rect.collidepoint(event.pos):
                self.level_name_box.start()
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
                self.custom_level.save()
                self.level_name_box.str = 'my level'
        
class StillPicture:
    def __init__(self, symbol: str, x: int, y: int):
        self.symbol = symbol
        self.x = x
        self.y = y


class DraggedPicture:
    def __init__(self, symbol: str, x: int, y: int, offset_x: int, offset_y: int):
        self.symbol = symbol
        self.x = x
        self.y = y
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
