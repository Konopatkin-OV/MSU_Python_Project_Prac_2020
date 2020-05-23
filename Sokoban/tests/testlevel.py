from unittest import TestCase
from Sokoban.level import Level


class TestLevel(TestCase):
    def setUp(self):
        self.level = Level('0')

    def test_is_complete_false(self):
        self.assertFalse(self.level.is_complete())

    def test_is_complete_true(self):
        for box, cell in zip(self.level.boxes, self.level.box_cells):
            box.move(*cell)

        self.assertTrue(self.level.is_complete())

    def test_get_box_none(self):
        self.assertIsNone(self.level.get_box(0, 0))

    def test_get_box_not_none(self):
        box_pos = self.level.boxes[0].get_pos()
        self.assertIsNotNone(self.level.get_box(*box_pos))

    def test_is_empty_wall(self):
        self.assertFalse(self.level.is_empty(0, 0))

    def test_is_empty_box(self):
        box_pos = self.level.boxes[0].get_pos()

        self.assertFalse(self.level.is_empty(*box_pos))

    def test_is_empty_player(self):
        player_pos = self.level.player.get_pos()

        self.assertTrue(self.level.is_empty(*player_pos))

    def test_is_empty_unoccupied_box_cell(self):
        cell_pos = self.level.box_cells[0]

        self.assertTrue(self.level.is_empty(*cell_pos))

    def test_is_empty_occupied_box_cell(self):
        cell_pos = self.level.box_cells[0]
        self.level.boxes[0].move(*cell_pos)

        self.assertFalse(self.level.is_empty(*cell_pos))

    def test_reset(self):
        self.level.boxes[0].move(0, 0)
        self.level.player.move(1, 1)

        self.level.reset()

        new_level = Level('0')
        self.assertEqual(self.level.player.get_pos(), new_level.player.get_pos())
        self.assertEqual(set(box.get_pos() for box in self.level.boxes),
                         set(box.get_pos() for box in new_level.boxes))

    def test_check_for_validity_raises_exception(self):
        field = [['w', 'w', 'w', 'w'],
                 ['w', 'b', ' ', 'w'],
                 ['w', 'b', 'p', 'w'],
                 ['w', 'w', 'w', 'w']]

        self.assertRaises(IOError, lambda: Level.check_for_validity(field))

    def test_check_for_validity_does_not_raise_exception(self):
        field = [['w', 'w', 'w', 'w'],
                 ['w', 'x', ' ', 'w'],
                 ['w', 'b', 'p', 'w'],
                 ['w', 'w', 'w', 'w']]

        Level.check_for_validity(field)
