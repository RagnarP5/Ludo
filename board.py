import pygame
import os
import csv
from cell import Cell
import random
import time


class Board:
    cell_size = 50
    grid_size = 15
    border_size = 3
    die_border = 20

    def __init__(self, players):
        self.screen_width = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)
        self.screen_height = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)
        self.players = players
        self.grid = None
        self.track = {}
        self.die_position = None
        self.roll_val = 6

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

                if track[y][x] != '-':
                    self.track[track[y][x]] = grid[x][y]

        self.grid = grid

    def draw_board(self):
        self.get_grid()
        self.draw_board_middle()
        self.draw_out_cells()
        self.show_home_bases()
        self.draw_pieces()
        self.draw_die()
        self.show_names()

    def update(self):
        self.draw_board()
        pygame.display.flip()

    def draw_board_middle(self):
        top_left = (self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 6
        top_right = (self.cell_size + self.border_size) * 9 - self.border_size - 1, (
                self.cell_size + self.border_size) * 6
        bot_left = (self.cell_size + self.border_size) * 6, (
                self.cell_size + self.border_size) * 9 - self.border_size - 1
        bot_right = (self.cell_size + self.border_size) * 9 - self.border_size - 1, (
                self.cell_size + self.border_size) * 9 - self.border_size - 1

        middle_top_left = (self.cell_size + self.border_size) * 7, (self.cell_size + self.border_size) * 7
        middle_top_right = (self.cell_size + self.border_size) * 8 - self.border_size - 1, (
                self.cell_size + self.border_size) * 7
        middle_bot_left = (self.cell_size + self.border_size) * 7, (
                self.cell_size + self.border_size) * 8 - self.border_size - 1
        middle_bot_right = (self.cell_size + self.border_size) * 8 - self.border_size - 1, (
                self.cell_size + self.border_size) * 8 - self.border_size - 1

        # # Save the middle position to draw the die
        self.die_position = {"top_left": middle_top_left,
                             "top_right": middle_top_right,
                             "bot_right": middle_bot_right,
                             "bot_left": middle_bot_left}
        # self.die_position = [middle_top_left,middle_top_right, middle_bot_right, middle_bot_left]

        middle = (self.screen_width / 2, self.screen_height / 2)
        pygame.draw.polygon(self.screen, pygame.Color("red"), [top_left, middle_top_left, middle_bot_left, bot_left])
        pygame.draw.polygon(self.screen, pygame.Color("green"),
                            [top_left, middle_top_left, middle_top_right, top_right])
        pygame.draw.polygon(self.screen, pygame.Color("gold"),
                            [top_right, middle_top_right, middle_bot_right, bot_right])
        pygame.draw.polygon(self.screen, pygame.Color("skyblue"),
                            [bot_left, middle_bot_left, middle_bot_right, bot_right])

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
        circle_center = position[0] + base_size / 2, position[1] + base_size / 2
        circle_radius = base_size / 2 * 0.9
        # First draw a black circle under for border
        pygame.draw.circle(self.screen, pygame.Color("black"), circle_center, circle_radius + self.border_size)
        pygame.draw.circle(self.screen, pygame.Color(player.color), circle_center, circle_radius)
        # Make white squares for pieces to stand on
        white_square_pos = []
        # radius divider
        rv = 3
        white_square_pos.append((circle_center[0] - circle_radius / rv - self.cell_size / 2,
                                 circle_center[1] - circle_radius / rv - self.cell_size / 2))
        white_square_pos.append((circle_center[0] + circle_radius / rv - self.cell_size / 2,
                                 circle_center[1] - circle_radius / rv - self.cell_size / 2))
        white_square_pos.append((circle_center[0] - circle_radius / rv - self.cell_size / 2,
                                 circle_center[1] + circle_radius / rv - self.cell_size / 2))
        white_square_pos.append((circle_center[0] + circle_radius / rv - self.cell_size / 2,
                                 circle_center[1] + circle_radius / rv - self.cell_size / 2))

        # Save base_positions for each piece
        for idx, pos in enumerate(white_square_pos):
            self._draw_white_square_with_border(pos)
            base_positions = [(x[0] + self.cell_size / 2, x[1] + self.cell_size / 2) for x in white_square_pos]
            player.pieces[idx].base_position = base_positions[idx]

    def show_names(self):

        def _get_font(size=20):
            return pygame.font.Font('freesansbold.ttf', size)

        name_padding = 10
        top_left = (name_padding, name_padding)
        top_right = ((self.cell_size + self.border_size) * 9 + name_padding, name_padding)
        bot_left = (name_padding, (self.cell_size + self.border_size) * 9 + name_padding)
        bot_right = (
            (self.cell_size + self.border_size) * 9 + name_padding,
            (self.cell_size + self.border_size) * 9 + name_padding)

        for player in self.players:

            font = _get_font()

            if player.color.upper() == "RED":
                pos = top_left
            elif player.color.upper() == "GREEN":
                pos = top_right
            elif player.color.upper() == "GOLD":
                pos = bot_right
            elif player.color.upper() == "SKYBLUE":
                pos = bot_left
            else:
                raise Exception("Incorrect color")

            text = font.render(player.name, True, player.color)
            self.screen.blit(text, pos)

    def draw_pieces(self):
        for player in self.players:
            for piece in player.pieces:
                if piece.is_in_base():
                    self._draw_circle_with_border(pygame.Color(player.color), piece.base_position, piece.radius)

                if piece.is_on_track():
                    piece_positions = [x.position for x in player.pieces]
                    n_pieces = sum([x == piece.position for x in piece_positions])
                    curr_cell = self.get_cell(piece)
                    curr_cell.draw_piece(self.screen, piece.color, n_pieces)

    def _offset_position(self, position, offset):
        return position[0] + offset, position[1] + offset

    def get_cell(self, piece):
        offset = piece.offset
        position = piece.position
        if position > 51:
            if piece.color == "RED":
                position = "1-" + str(piece.position)
            elif piece.color == "GOLD":
                position = "2-" + str(piece.position)
            elif piece.color == "GREEN":
                position = "3-" + str(piece.position)
            elif piece.color == "SKYBLUE":
                position = "4-" + str(piece.position)
        else:
            position = (position + offset[piece.color]) % 52

        return self.track[str(position)]

    def _draw_circle_with_border(self, color, circle_center, circle_radius):
        pygame.draw.circle(self.screen, pygame.Color("black"), circle_center, circle_radius + self.border_size)
        pygame.draw.circle(self.screen, pygame.Color(color), circle_center, circle_radius)

    def _draw_white_square_with_border(self, pos):
        black_pos = (pos[0] - self.border_size, pos[1] - self.border_size)
        black_size = (self.cell_size + 2 * self.border_size, self.cell_size + 2 * self.border_size)
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect(black_pos, black_size))
        pygame.draw.rect(self.screen, pygame.Color("white"), pygame.Rect(pos, (self.cell_size, self.cell_size)))

    def draw_die(self):
        roll = self.roll_val
        die_pos = (
            self.die_position["top_left"][0] + self.die_border / 2,
            self.die_position["top_left"][1] + self.die_border / 2)
        die_size = abs(self.die_position["top_left"][0] - self.die_position["top_right"][0]) - self.die_border
        pygame.draw.rect(self.screen, pygame.Color("white"), pygame.Rect(die_pos, (die_size, die_size)),
                         border_radius=2)
        pip_size = 3
        if roll in [1, 3, 5]:
            pip_center = (die_pos[0] + die_size / 2, die_pos[1] + die_size / 2)

            pygame.draw.circle(self.screen, pygame.Color("black"), pip_center, pip_size)
        if roll in [2, 3]:
            corner_pos = self._get_corner_pip_positions(die_pos, die_size)
            for index, pos in enumerate(corner_pos):
                if index in [0, 3]:
                    pygame.draw.circle(self.screen, pygame.Color("black"), pos, pip_size)
        if roll in [4, 5, 6]:
            corner_pos = self._get_corner_pip_positions(die_pos, die_size)
            for pos in corner_pos:
                pygame.draw.circle(self.screen, pygame.Color("black"), pos, pip_size)
        if roll == 6:
            middle_pip_pos = [(die_pos[0] + die_size / 4, die_pos[1] + die_size / 2),
                              (die_pos[0] + die_size * 3 / 4, die_pos[1] + die_size / 2)]
            for pos in middle_pip_pos:
                pygame.draw.circle(self.screen, pygame.Color("black"), pos, pip_size)

    def _get_corner_pip_positions(self, die_pos, die_size):
        corner_pip_pos = [(die_pos[0] + die_size / 4, die_pos[1] + die_size / 4),
                          (die_pos[0] + die_size / 4, die_pos[1] + die_size * 3 / 4),
                          (die_pos[0] + die_size * 3 / 4, die_pos[1] + die_size / 4),
                          (die_pos[0] + die_size * 3 / 4, die_pos[1] + die_size * 3 / 4),
                          ]

        return corner_pip_pos

    def roll(self):
        for _ in range(random.randint(10, 30)):
            self.roll_val = random.randint(1, 6)
            self.draw_die()
            pygame.display.flip()
            time.sleep(0.05)

        return self.roll_val

# if __name__ == '__main__':
#     board = Board()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     running = False
#                 if event.key == K_RETURN:
#                     # print("HERE")
#                     board.roll()
