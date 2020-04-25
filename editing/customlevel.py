import os


class CustomLevel:
    min_width = 3
    min_height = 3

    def __init__(self, app):
        self.app = app
        self.width = self.min_width
        self.height = self.min_height
        self.field = [['w'] * self.width for i in range(self.height)]

    def _add_left_column(self):
        self.field.insert(0, ['w'] * self.height)
        self.width = self.width + 1

        if self._check_column(-2):
            self._remove_column(-2)

    def _add_right_column(self):
        self.field.append(['w'] * self.height)
        self.width = self.width + 1

        if self._check_column(1):
            self._remove_column(1)

    def _add_top_row(self):
        for column in self.field:
            column.insert(0, 'w')
        self.height = self.height + 1

        if self._check_row(-2):
            self._remove_row(-2)

    def _add_bottom_row(self):
        for column in self.field:
            column.append('w')
        self.height = self.height + 1

        if self._check_row(1):
            self._remove_row(1)

    def _check_column(self, index: int) -> bool:
        return all(item == 'w' for item in self.field[index])

    def _check_row(self, index: int) -> bool:
        return all(column[index] == 'w' for column in self.field)

    def _remove_column(self, index: int):
        self.field.pop(index)
        self.width = self.width - 1

    def _remove_row(self, index: int):
        for column in self.field:
            column.pop(index)
        self.height = self.height - 1

    """Puts something on the field."""

    def put(self, symbol: str, x: int, y: int):
        if x < 0 or x >= self.width or \
                y < 0 or y >= self.height:
            return

        self.field[x][y] = symbol

        if symbol == 'w':
            if x == 1:
                while self.width > self.min_width:
                    if self._check_column(1):
                        self._remove_column(1)
                    else:
                        break
            elif x == self.width - 2:
                while self.width > self.min_width:
                    if self._check_column(-2):
                        self._remove_column(-2)
                    else:
                        break
            if y == 1:
                while self.height > self.min_height:
                    if self._check_row(1):
                        self._remove_row(1)
                    else:
                        break
            elif y == self.height - 2:
                while self.height > self.min_height:
                    if self._check_row(-2):
                        self._remove_row(-2)
                    else:
                        break
        else:
            if x == 0:
                self._add_left_column()
            elif x == self.width - 1:
                self._add_right_column()
            if y == 0:
                self._add_top_row()
            elif y == self.height - 1:
                self._add_bottom_row()

    """Saves the level to a file."""

    def save(self):
        order = 1
        while os.path.exists(f'levels/my level {order}.lvl'):
            order = order + 1

        name = f'my level {order}'
        file = open(f'levels/{name}.lvl', 'w')
        # for row in map(lambda symbol: ''.join(symbol), zip(*self.field)):
        for line in zip(*self.field):
            for symbol in line:
                file.write(symbol)
            file.write('\n')
        file.close()
        self.app.GUIs['moveBoxesGame'].add_level(name)
