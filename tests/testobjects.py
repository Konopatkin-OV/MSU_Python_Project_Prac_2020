from unittest import TestCase
from objects import GameEntity


class TestGameEntity(TestCase):
    def setUp(self):
        self.game_entity = GameEntity(0, 0)

    def test_move(self):
        x, y = 100, 200

        self.game_entity.move(x, y)
        self.assertEqual(self.game_entity.get_pos(), (x, y))

    def test_reset(self):
        self.game_entity.x, self.game_entity.y = 100, 200

        self.game_entity.reset()
        self.assertEqual(self.game_entity.get_pos(), (0, 0))
