from typing import Optional
from objects import Player, Box
from BaseApp import GUI, Application


class Level(GUI):
    def __init__(self, app: Application, file_name: str):
        super().__init__(app, name=file_name)

        self.dimensions = None
        self.player = None
        self.field = []
        self.boxes = []
        self.places_for_boxes = []

        f = open(f'levels/{file_name}.lvl', 'r')
        for x, string in enumerate(f):
            line = []
            for y, symbol in enumerate(string):
                if symbol == '\n':
                    continue
                if symbol == 'w':
                    line.append(False)
                else:
                    line.append(True)
                    if symbol == 'p':
                        self.player = Player(y, x)
                    elif symbol == 'b':
                        self.boxes.append(Box(y, x))
                    elif symbol == 'x':
                        self.places_for_boxes.append((y, x))
            self.field.append(line)
        # Transpose the matrix
        self.field = list(map(list, zip(*self.field)))
        self.dimensions = len(self.field[0]), len(self.field)

    """Indicates that the level is finished."""
    def is_finished(self) -> bool:
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
        return self.field[x][y] and not self.get_box(x, y)



