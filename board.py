import pygame
import os
import csv
from cell import Cell
from player import Player
from pygame.locals import *


class Board:
    cell_size = 50
    grid_size = 15
    border_size = 3

    def __init__(self):
        self.screen_width = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)
        self.screen_height = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)
        self.players = [Player("RED"), Player("GREEN"), Player("GOLD"), Player("SKYBLUE")]
        self.grid = None
        self.track = {}
        self.base_positions = {}

        pygame.display.set_caption("Ludo")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.update()

    def get_grid(self):
        # Make grid (start with grid_size x grid_size matrix with empty values)
        grid = [list([] for x in range(0, self.grid_size)) for y in range(0, self.grid_size)]

        colors = list(csv.reader(open(f"{os.getcwd()}\\data\\colors.csv")))
        track = list(csv.reader(open(f"{os.getcwd()}\\data\\track.csv")))

        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                grid[x][y] = Cell(x, y, colors[y][x])
                grid[x][y].draw(self.screen)
                print(f"x: {x}\ty:{y}\ttrack[y][x]: {track[y][x]}")

                if track[y][x] != '-':
                    self.track[track[y][x]] = grid[x][y]

        self.grid = grid

    def draw_board(self):
        self.get_grid()
        self.draw_board_middle()
        self.draw_out_cells()
        self.show_home_bases()
        self.draw_pieces()
        # self.draw_pieces_in_base()

    def update(self):
        self.draw_board()
        pygame.display.flip()

    def draw_board_middle(self):
        top_left = (self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 6
        top_right = (self.cell_size + self.border_size) * 9 - self.border_size - 1, (self.cell_size + self.border_size) * 6
        bot_left = (self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 9 - self.border_size - 1
        bot_right = (self.cell_size + self.border_size) * 9 - self.border_size - 1, (self.cell_size + self.border_size) * 9 - self.border_size - 1

        middle_top_left = (self.cell_size + self.border_size) * 7, (self.cell_size + self.border_size) * 7
        middle_top_right = (self.cell_size + self.border_size) * 8 - self.border_size - 1, (self.cell_size + self.border_size) * 7
        middle_bot_left = (self.cell_size + self.border_size) * 7, (self.cell_size + self.border_size) * 8 - self.border_size - 1
        middle_bot_right = (self.cell_size + self.border_size) * 8 - self.border_size - 1, (self.cell_size + self.border_size) * 8 - self.border_size - 1

        middle = (self.screen_width / 2, self.screen_height / 2)
        pygame.draw.polygon(self.screen, pygame.Color("red"), [top_left, middle_top_left, middle_bot_left, bot_left])
        pygame.draw.polygon(self.screen, pygame.Color("green"), [top_left, middle_top_left, middle_top_right, top_right])
        pygame.draw.polygon(self.screen, pygame.Color("gold"), [top_right, middle_top_right, middle_bot_right, bot_right])
        pygame.draw.polygon(self.screen, pygame.Color("skyblue"), [bot_left, middle_bot_left, middle_bot_right, bot_right])

    def draw_out_cells(self):
        # Draw squares where each color goes out of base to
        def draw_cell(out_pos, color_id):
            out_cell = self.grid[out_pos[0]][out_pos[1]]
            out_cell.color_id = color_id
            out_cell.draw(self.screen)

        red_out_pos = (1, 6)
        green_out_pos = (8, 1)
        yellow_out_pos = (13, 8)
        blue_out_pos = (6, 13)

        draw_cell(red_out_pos, 1)
        draw_cell(green_out_pos, 2)
        draw_cell(blue_out_pos, 3)
        draw_cell(yellow_out_pos, 4)

    def show_home_bases(self):
        for player in self.players:
            self.show_home_base(player)

    # noinspection PyListCreation
    def show_home_base(self, player):
        if player.color.upper() == "RED":
            position = (0, 0)
        elif player.color.upper() == "GREEN":
            position = ((self.cell_size + self.border_size) * 9, 0)
        elif player.color.upper() == "SKYBLUE":
            position = (0, (self.cell_size + self.border_size) * 9)
        elif player.color.upper() == "GOLD":
            position = ((self.cell_size + self.border_size) * 9, (self.cell_size + self.border_size) * 9)
        else:
            raise Exception("Color incorrect")

        base_size = self.cell_size * 6 + self.border_size * 5
        # Fill with white
        pygame.draw.rect(self.screen, pygame.Color("white"), pygame.Rect(position, (base_size, base_size)))
        # Make colored circles
        circle_center = position[0] + base_size/2, position[1] + base_size/2
        circle_radius = base_size/2*0.9
        # First draw a black circle under for border
        pygame.draw.circle(self.screen, pygame.Color("black"), circle_center, circle_radius + self.border_size)
        pygame.draw.circle(self.screen, pygame.Color(player.color), circle_center, circle_radius)
        # Make white squares for pieces to stand on
        white_square_pos = []
        # radius divider
        rv = 3
        white_square_pos.append((circle_center[0] - circle_radius/rv - self.cell_size/2, circle_center[1] - circle_radius/rv - self.cell_size/2))
        white_square_pos.append((circle_center[0] + circle_radius/rv - self.cell_size/2, circle_center[1] - circle_radius/rv - self.cell_size/2))
        white_square_pos.append((circle_center[0] - circle_radius/rv - self.cell_size/2, circle_center[1] + circle_radius/rv - self.cell_size/2))
        white_square_pos.append((circle_center[0] + circle_radius/rv - self.cell_size/2, circle_center[1] + circle_radius/rv - self.cell_size/2))

        for pos in white_square_pos:
            self._draw_white_square_with_border(pos)
            self.base_positions[player.color] = [(x[0] + self.cell_size / 2, x[1] + self.cell_size / 2) for x in white_square_pos]

    def draw_pieces(self):

        testing = True

        for player in self.players:
            for piece in player.pieces:
                if piece.is_in_base():
                    white_square_pos = self.base_positions[player.color.upper()]
                    for pos in white_square_pos:
                        piece.base_position = pos
                        self._draw_circle_with_border(pygame.Color(player.color), pos, piece.radius)

                if piece.is_on_track():
                    curr_cell = self.get_cell(piece.color, piece.position)
                    curr_cell.draw_piece(self.screen, piece.color)
                    self._draw_white_square_with_border(piece.base_position)

    def get_cell(self, color, position):
        offset = {"RED": 0,
                  "GREEN": 13,
                  "YELLOW": 26,
                  "BLUE": 39}
        if position > 51:
            if color == "RED":
                position = "1-" + str(position)
            elif color == "YELLOW":
                position = "2-" + str(position)
            elif color == "GREEN":
                position = "3-" + str(position)
            elif color == "BLUE":
                position = "4-" + str(position)
        else:
            position += offset[color]

        return self.track[str(position)]

    def _draw_circle_with_border(self, color, circle_center, circle_radius):
        pygame.draw.circle(self.screen, pygame.Color("black"), circle_center, circle_radius + self.border_size)
        pygame.draw.circle(self.screen, pygame.Color(color), circle_center, circle_radius)

    def _draw_white_square_with_border(self, pos):
        black_pos = (pos[0] - self.border_size, pos[1] - self.border_size)
        black_size = (self.cell_size + 2 * self.border_size, self.cell_size + 2 * self.border_size)
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(black_pos, black_size))
        pygame.draw.rect(self.screen, pygame.Color("white"), pygame.Rect(pos, (self.cell_size, self.cell_size)))

if __name__ == '__main__':
    board = Board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                # board.update()


