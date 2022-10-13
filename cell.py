import pygame

colors = {
    0: pygame.Color("White"),
    1: pygame.Color("Red"),
    2: pygame.Color("green"),
    3: pygame.Color("skyblue"),
    4: pygame.Color("Gold")
}

class Cell:

    def __init__(self, x, y, color_id, cell_size=50, border_size=3):
        self.x = x
        self.y = y
        self.color_id = int(color_id)
        self.cell_size = cell_size
        self.border_size = border_size
        self.piece_radius = 20

    def colour(self):
        try:
            return colors[self.color_id]
        except KeyError:
            return pygame.Color("Black")

    def position(self):
        x = self.x * (self.cell_size + self.border_size)
        y = self.y * (self.cell_size + self.border_size)

        return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour(), pygame.Rect(self.position(), (self.cell_size, self.cell_size)))

    def draw_piece(self, screen, color):

        if color.upper() == "RED":
            color = pygame.Color("red")
        if color.upper() == "GREEN":
            color = pygame.Color("green")
        if color.upper() == "YELLOW":
            color = pygame.Color("gold")
        if color.upper() == "BLUE":
            color = pygame.Color("skyblue")

        pygame.draw.circle(screen, pygame.Color("black"), self.position(self.cell_size / 2), self.piece_radius + self.border_size)
        pygame.draw.circle(screen, color, self.position(self.cell_size / 2))