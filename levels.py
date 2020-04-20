from typing import Optional
from objects import Player, Box


class Level:
    def __init__(self, file_name: str):
        self.dimensions = None
        self.player = None
        self.field = []
        self.boxes = []
        self.places_for_boxes = []
        self.name = file_name

        file = open(f'lvls/{file_name}.lvl', 'r')
        for x, string in enumerate(file):
            line = []
            for y, symbol in enumerate(string):
                if symbol == '\n':
                    continue
                if symbol == 'w':
                    line.append(False)
                else:
                    line.append(True)
                    if symbol == 'p':
                        if self.player:
                            raise IOError
                        else:
                            self.player = Player(y, x)
                    elif symbol == 'b':
                        self.boxes.append(Box(y, x))
                    elif symbol == 'x':
                        self.places_for_boxes.append((y, x))
                    elif symbol == ' ':
                        continue
                    else:
                        raise IOError
            self.field.append(line)

        # Check that each box has a place
        if len(self.boxes) != len(self.places_for_boxes):
            raise IOError

        # Check that all the lines in a file have the same length
        if not all(len(elem) == len(self.field[0]) for elem in self.field):
            raise IOError

        # Transpose the matrix
        self.field = list(map(list, zip(*self.field)))
        self.dimensions = len(self.field), len(self.field[0])

    """Indicates that the level is complete."""
    def is_complete(self) -> bool:
        return set(self.places_for_boxes) ==\
               set(map(lambda box: box.position, self.boxes))

    """Returns a box from the given cell or None if there is no box."""
    def get_box(self, x: int, y: int) -> Optional[Box]:
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None

    """Indicates that the cell is available and has no boxes on it."""
    def is_empty(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.dimensions[0] or\
           y < 0 or y >= self.dimensions[1]:
            return False
        return self.field[x][y] and not self.get_box(x, y)

    """Start over."""
    def reset(self):
        self.player.reset()
        for box in self.boxes:
            box.reset()



