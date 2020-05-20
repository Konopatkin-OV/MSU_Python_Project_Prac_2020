from typing import Optional
from Sokoban.objects import Player, Box
from typing import List
import os


class Level:
    min_width = 3
    min_height = 3

    def __init__(self, file_name: str):
        self.width = None
        self.height = None
        self.player = None
        self.field = []
        self.boxes = []
        self.box_cells = []
        self.name = file_name

        dirname = os.path.dirname(__file__)
        file = open(os.path.join(dirname, 'levels', f'{file_name}.lvl'), 'r')
        self.order = int(file.readline().split()[0])
        field = [[symbol for symbol in line if symbol != '\n']
                 for line in file if line != '\n']
        file.close()

        # Transpose the matrix
        field = list(map(list, zip(*field)))

        # If invalid, raise exception
        self.check_for_validity(field)

        for i, column in enumerate(field):
            actual_column = []
            for j, (symbol) in enumerate(column):
                actual_column.append(symbol != 'w')
                if symbol in 'pP':
                    self.player = Player(i, j)
                if symbol in 'bB':
                    self.boxes.append(Box(i, j))
                if symbol in 'xPB':
                    self.box_cells.append((i, j))
            self.field.append(actual_column)
        self.width = len(self.field)
        self.height = len(self.field[0])

    """Raises IOError if the level file is invalid."""

    @staticmethod
    def check_for_validity(field: List[List[str]]):
        # Check that the width is acceptable
        if len(field) < Level.min_width:
            raise IOError

        # Check that the height is acceptable
        if len(field[0]) < Level.min_height:
            raise IOError

        # Check that all the columns have the same length
        if not all(len(column) == len(field[0]) for column in field):
            raise IOError

        flat_field = [symbol for column in field for symbol in column]

        # Check that all the symbols are acceptable
        if len(list(filter(lambda symbol: symbol in ' wxpPbB', flat_field))) \
                != len(flat_field):
            raise IOError

        # Check that there is exactly one player
        player = len(list(filter(lambda symbol: symbol in 'pP', flat_field)))
        if player != 1:
            raise IOError

        # Check that there are boxes on the field and each box has its place
        # And that the level is not already completed
        boxes = len(list(filter(lambda symbol: symbol in 'b', flat_field)))
        box_cells = len(list(filter(lambda symbol: symbol in 'xP', flat_field)))
        if boxes == 0 or boxes != box_cells:
            raise IOError

        # Check that the field is surrounded by walls
        if not all(symbol == 'w' for symbol in field[0]) or \
                not all(symbol == 'w' for symbol in field[-1]) or \
                not all(column[0] == 'w' for column in field) or \
                not all(column[-1] == 'w' for column in field):
            raise IOError

    """Indicates that the level is complete."""

    def is_complete(self) -> bool:
        return set(self.box_cells) == \
               set(map(lambda box: box.get_pos(), self.boxes))

    """Returns a box from the given cell or None if there is no box."""

    def get_box(self, x: int, y: int) -> Optional[Box]:
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None

    """Indicates that the cell is available and has no boxes on it."""

    def is_empty(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or \
                y < 0 or y >= self.height:
            return False
        return self.field[x][y] and not self.get_box(x, y)

    """Start over."""

    def reset(self):
        self.player.reset()
        for box in self.boxes:
            box.reset()
