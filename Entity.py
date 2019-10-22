class Entity:
    """
    Player Object
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # Player movement
        self.x += dx
        self.y += dy
