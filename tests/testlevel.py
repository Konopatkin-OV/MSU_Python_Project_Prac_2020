from unittest import TestCase
from level import Level


class TestLevel(TestCase):
    def setUp(self):
        self.level = Level('0')

    def test_is_complete(self):
        self.assertFalse(self.level.is_complete())

        for box, cell in zip(self.level.boxes, self.level.box_cells):
            box.move(*cell)

        self.assertTrue(self.level.is_complete())

    def test_get_box(self):
        self.assertIsNone(self.level.get_box(0, 0))

        box_pos = self.level.boxes[0].get_pos()
        self.assertIsNotNone(self.level.get_box(*box_pos))

    def test_is_empty(self):
        self.assertFalse(self.level.is_empty(0, 0))

        box_pos = self.level.boxes[0].get_pos()
        self.assertFalse(self.level.is_empty(*box_pos))

        cell = 0, 0
        for cell in self.level.box_cells:
            if all(cell != box.get_pos() for box in self.level.boxes):
                break
        self.assertTrue(self.level.is_empty(*cell))

    def test_reset(self):
        self.level.boxes[0].move(0, 0)
        self.level.reset()

        self.assertEqual(set(box.get_pos() for box in self.level.boxes),
                         set(box.get_pos() for box in Level('0').boxes))

    def test_check_for_validity(self):
        field = [['w', 'w', 'w', 'w'],
                 ['w', 'x', ' ', 'w'],
                 ['w', 'b', 'p', 'w'],
                 ['w', 'w', 'w', 'w']]

        # Does not raise an exception
        Level.check_for_validity(field)

        field[1][1] = 'b'
        self.assertRaises(IOError, lambda: Level.check_for_validity(field))
