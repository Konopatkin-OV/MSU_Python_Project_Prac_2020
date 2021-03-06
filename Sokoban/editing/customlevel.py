"""customlevel.py
=================
CustomLevel class for editing level.
"""
import os
from Sokoban.level import Level


class CustomLevel:
    min_width = 3
    min_height = 3

    def __init__(self):
        self.width = self.min_width
        self.height = self.min_height
        self.field = [[''] * self.height for i in range(self.width)]

    def _add_left_column(self):
        """Adds a new column to the left of the field."""
        self.field.insert(0, [''] * self.height)
        self.width = self.width + 1

        if self._check_column(-2):
            self._remove_column(-2)

    def _add_right_column(self):
        """Adds a new column to the right of the field."""
        self.field.append([''] * self.height)
        self.width = self.width + 1

        if self._check_column(1):
            self._remove_column(1)

    def _add_top_row(self):
        """Adds a new row to the top of the field."""
        for column in self.field:
            column.insert(0, '')
        self.height = self.height + 1

        if self._check_row(-2):
            self._remove_row(-2)

    def _add_bottom_row(self):
        """Adds a new row to the bottom of the field."""
        for column in self.field:
            column.append('')
        self.height = self.height + 1

        if self._check_row(1):
            self._remove_row(1)

    def _check_column(self, index: int) -> bool:
        """Checks that the column consists entirely of walls."""
        return all(not item for item in self.field[index])

    def _check_row(self, index: int) -> bool:
        """Checks that the row consists entirely of walls."""
        return all(not column[index] for column in self.field)

    def _remove_column(self, index: int):
        """Removes a column from the field."""
        self.field.pop(index)
        self.width = self.width - 1

    def _remove_row(self, index: int):
        """Removes a row from the field."""
        for column in self.field:
            column.pop(index)
        self.height = self.height - 1

    def _add_extra_walls(self):
        """Adds a wall boarder if necessary."""
        if not self._check_column(0):
            self._add_left_column()
        if not self._check_column(-1):
            self._add_right_column()
        if not self._check_row(0):
            self._add_top_row()
        if not self._check_row(-1):
            self._add_bottom_row()

    def _remove_extra_walls(self):
        """Removes a wall boarder if necessary."""
        while self.width > self.min_width:
            if self._check_column(1):
                self._remove_column(1)
            else:
                break
        while self.width > self.min_width:
            if self._check_column(-2):
                self._remove_column(-2)
            else:
                break
        while self.height > self.min_height:
            if self._check_row(1):
                self._remove_row(1)
            else:
                break
        while self.height > self.min_height:
            if self._check_row(-2):
                self._remove_row(-2)
            else:
                break

    def put(self, symbol: str, x: int, y: int):
        """Puts something on the field."""
        if 0 <= x < self.width and 0 <= y < self.height and \
                (symbol == ' ' and self.field[x][y] == '' or
                 symbol == 'x' and self.field[x][y] == ' ' or
                 symbol in 'pb' and self.field[x][y] in (' ', ' x')):
            self.field[x][y] = self.field[x][y] + symbol
            self._add_extra_walls()
        self._remove_extra_walls()

    def remove(self, x: int, y: int) -> str:
        """Removes something from the field."""
        if 0 <= x < self.width and 0 <= y < self.height and \
                self.field[x][y]:
            symbol = self.field[x][y][-1]
            self.field[x][y] = self.field[x][y][:-1]
            return symbol
        else:
            return ''

    def save(self, level_name, max_order) -> str:
        """Saves the level to a file."""
        field = []
        for column in self.field:
            actual_column = []
            for cell in column:
                if not cell:
                    actual_column.append('w')
                elif cell == ' ':
                    actual_column.append(cell)
                elif cell in (' x', ' p', ' b'):
                    actual_column.append(cell[-1])
                elif cell == ' xp':
                    actual_column.append('P')
                elif cell == ' xb':
                    actual_column.append('B')
            field.append(actual_column)
        Level.check_for_validity(field)

        dirname = os.path.dirname(__file__)

        order = 1
        while os.path.exists(os.path.join(dirname, '..', 'levels', f'my level {order}.lvl')):
            order = order + 1

        # default name for level
        if level_name == 'my level':
            name = f'my level {order}'
        else:
            name = level_name

        file = open(os.path.join(dirname, '..', 'levels', f'{name}.lvl'), 'w')
        file.write(f'{max_order + 1}\n')
        for line in zip(*field):
            for symbol in line:
                file.write(symbol)
            file.write('\n')
        file.close()
        return name
