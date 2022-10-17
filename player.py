from piece import Piece


class Player:
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.pieces = []
        for i in range(0, 4):
            self.pieces.append(Piece(self.color))
        self.active_piece_idx = 0

    def move(self, roll):
        self.active_piece().position += roll

    def next_active_piece(self):
        self.active_piece_idx = (self.active_piece_idx + 1) % 4

    def active_piece(self):
        return self.pieces[self.active_piece_idx]
