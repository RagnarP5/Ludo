from piece import Piece


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []
        for i in range(0,4):
            self.pieces.append(Piece(self.color))
