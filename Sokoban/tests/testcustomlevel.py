from unittest import TestCase
from Sokoban.editing.customlevel import CustomLevel


class TestCustomLevel(TestCase):
    def setUp(self):
        self.custom_level = CustomLevel()

    def test_add_left_column(self):
        field = self.custom_level.field
        field[0][1], field[-2][1] = ' ', ' '

        self.custom_level._add_left_column()

        self.assertTrue(self.custom_level.width == CustomLevel.min_width + 1)
        self.assertEqual(field[0], [''] * CustomLevel.min_height)

    def test_add_right_column(self):
        field = self.custom_level.field
        field[-1][1], field[-2][1] = ' ', ' '

        self.custom_level._add_right_column()

        self.assertTrue(self.custom_level.width == CustomLevel.min_width + 1)
        self.assertEqual(field[-1], [''] * CustomLevel.min_height)

    def test_add_top_row(self):
        field = self.custom_level.field
        field[1][0], field[1][-2] = ' ', ' '

        self.custom_level._add_top_row()

        self.assertTrue(self.custom_level.height == CustomLevel.min_height + 1)
        self.assertEqual([column[0] for column in field], [''] * CustomLevel.min_width)

    def test_add_bottom_row(self):
        field = self.custom_level.field
        field[1][-1], field[1][-2] = ' ', ' '

        self.custom_level._add_bottom_row()

        self.assertTrue(self.custom_level.height == CustomLevel.min_height + 1)
        self.assertEqual([column[-1] for column in field], [''] * CustomLevel.min_width)

    def test_check_column(self):
        field = self.custom_level.field
        field[1][1] = ' '

        self.assertTrue(self.custom_level._check_column(0))
        self.assertFalse(self.custom_level._check_column(1))

    def test_check_row(self):
        field = self.custom_level.field
        field[1][1] = ' '

        self.assertTrue(self.custom_level._check_row(0))
        self.assertFalse(self.custom_level._check_row(1))

    def test_remove_column(self):
        field = self.custom_level.field
        field[1][1] = ' '
        field.append([''] * CustomLevel.min_height)
        self.custom_level.width = len(field)

        self.custom_level._remove_column(-2)
        self.assertEqual(self.custom_level.width, CustomLevel.min_width)

    def test_remove_row(self):
        field = self.custom_level.field
        field[1][1] = ' '
        for column in field:
            column.append('')
        self.custom_level.height = len(field[0])

        self.custom_level._remove_row(-2)
        self.assertEqual(self.custom_level.height, CustomLevel.min_height)

    def test_add_extra_walls(self):
        field = self.custom_level.field
        field[0][1], field[1][1] = ' ', ' '

        self.custom_level._add_extra_walls()
        self.assertEqual(self.custom_level.width, CustomLevel.min_width + 1)

    def test_remove_extra_walls(self):
        field = self.custom_level.field
        field[1][1] = ' '
        field.append([''] * CustomLevel.min_height)
        self.custom_level.width = len(field)

        self.custom_level._remove_extra_walls()
        self.assertEqual(self.custom_level.width, CustomLevel.min_width)

    def test_put_free_cell(self):
        x, y = 1, 1
        self.custom_level.put(' ', x, y)

        field = self.custom_level.field
        self.assertEqual(field[x][y], ' ')
        self.assertEqual(self.custom_level.width, CustomLevel.min_width)
        self.assertEqual(self.custom_level.height, CustomLevel.min_height)

    def test_remove(self):
        x, y = 1, 1
        field = self.custom_level.field
        field[x][y] = ' p'

        self.custom_level.remove(x, y)
        self.assertEqual(field[x][y], ' ')
        self.assertEqual(self.custom_level.width, CustomLevel.min_width)
        self.assertEqual(self.custom_level.height, CustomLevel.min_height)
