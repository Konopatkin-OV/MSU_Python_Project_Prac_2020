class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.initial_x = x
        self.initial_y = y

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y


class Box:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.initial_x = x
        self.initial_y = y

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
