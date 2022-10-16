from board import Board
import pygame
from pygame.locals import *
import time
from player import Player
import random


class Game:
    winner_found = False
    current_player_id = random.randint(0, 3)
    def __init__(self):
        pygame.init()
        self.players = [Player("Ragnar", "RED"),
                        Player("Tómas", "GREEN"),
                        Player("Hagalín", "GOLD"),
                        Player("Logi", "SKYBLUE")]
        self.board = Board(self.players)

    def play(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        self.board.roll()

