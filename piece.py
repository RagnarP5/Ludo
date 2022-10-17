
class Piece:
    HOME_POSITION = 57

    offset = {"RED": 0,
              "GREEN": 13,
              "GOLD": 26,
              "SKYBLUE": 39}

    def __init__(self, color):
        self.position = 0
        self.color = color
        self.radius = 20
        # x and y coordinates for the home position of the piece
        self.base_position = None

    def move(self, places):
        if self.can_move(places):
            self.position += places

    def can_move(self, places):
        return self.position + places <= self.HOME_POSITION

    def is_in_base(self):
        return self.position == 0

    def is_on_track(self):
        return 0 < self.position < self.HOME_POSITION

    def is_home(self):
        return self.position == self.HOME_POSITION

    def return_to_base(self):
        if not self.is_home():
            self.position = 0

    def get_relative_position(self):
        return (self.position + self.offset[self.color]) % 52