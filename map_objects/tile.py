class Tile:
    """
    Class for a Tile on a map, checks if the tile is blocked or not and if it blocks sight or not
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False
