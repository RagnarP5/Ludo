from board import Board
import pygame
from pygame.locals import *
import time
from player import Player
import random


class Game:
    winner_found = False

    def __init__(self):
        pygame.init()
        self.players = [Player("Ragnar", "RED"),
                        Player("Tómas", "GREEN"),
                        Player("Hagalín", "GOLD"),
                        Player("Logi", "SKYBLUE")]
        self.board = Board(self.players)
        self.active_player_id = random.randint(0, 3)
        self.active_player = self.players[self.active_player_id]
        self.active_player.is_active_player = True
        self.board.update()

    def next_player(self):
        self.active_player.is_active_player = False
        self.active_player_id = (self.active_player_id + 1) % 4
        self.active_player = self.players[self.active_player_id]
        self.active_player.is_active_player = True

    def _all_pieces_in_base(self):
        return all([piece.is_in_base() for piece in self.active_player.pieces])

    def roll_and_move(self):
        n_turns = 0
        while n_turns < 3:
            roll = self.board.roll()
            if roll != 6 and self._all_pieces_in_base():
                break
            for _ in range(1, roll + 1):
                self.active_player.move(1)
                time.sleep(0.25)
                self.board.update()
            self.knock_off()
            self.board.update()
            if roll != 6:
                break
            else:
                if not self._all_pieces_in_base():
                    self.active_player.next_active_piece()
            n_turns += 1

    def play(self):
        # If a player rolls a 6 they have another turn (maximum of 3)
        self.roll_and_move()
        self.next_player()

    def knock_off(self):

        def _is_multiple_same_position_pieces(other_player: Player, position):
            piece_positions = [x.position for x in other_player.pieces]
            return sum([x == position for x in piece_positions]) > 1

        active_piece = self.active_player.active_piece()

        for player in self.players:
            if player != self.active_player:
                for piece in player.pieces:
                    if piece.get_relative_position() == active_piece.get_relative_position():
                        if not _is_multiple_same_position_pieces(player, piece.get_relative_position()):
                            piece.return_to_base()

    def run(self):

        while not self.winner_found:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.winner_found = True
                    if event.key == K_RETURN:
                        self.play()
            self.play()


if __name__ == '__main__':
    game = Game()
    game.run()
