from unittest import TestCase
from editing.editor import StillPicture, DraggedPicture
from pygame import Rect


class TestStillPicture(TestCase):
    def test_move(self):
        x, y, size = 100, 200, 300
        rect = Rect(x, y, size, size)
        picture = StillPicture('p')

        picture.move(x, y, size)

        self.assertEqual(picture.rect, rect)


class TestDraggedPicture(TestCase):
    def test_move(self):
        x, y = 100, 200
        offset_x, offset_y = 10, 20
        picture = DraggedPicture('p', x, y, offset_x, offset_y)
        picture.move(offset_x, offset_y)
        self.assertEqual(picture.x, 0)
        self.assertEqual(picture.y, 0)
