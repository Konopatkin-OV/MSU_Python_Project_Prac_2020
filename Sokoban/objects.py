"""objects.py
=============
Classes GameEntity, Player, Box.
"""


class GameEntity(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.initial_x = x
        self.initial_y = y

    def reset(self):
        """Reset."""
        self.x = self.initial_x
        self.y = self.initial_y

    def move(self, x: int, y: int):
        """Move."""
        self.x = x
        self.y = y

    def get_pos(self):
        "Return position."
        return self.x, self.y


class Player(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class Box(GameEntity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
