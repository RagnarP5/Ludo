from piece import Piece


class Player:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.pieces = []
        for i in range(0, 4):
            self.pieces.append(Piece(self.color))

