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
        self.active_player = self.players[3]

    def play(self):

        while not self.winner_found:
            roll = self.board.roll()
            self.active_player.move(roll)
            self.board.update()
            time.sleep(0.001)
