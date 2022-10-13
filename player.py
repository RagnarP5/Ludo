from piece import Piece


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = [Piece(self.color)]*4
