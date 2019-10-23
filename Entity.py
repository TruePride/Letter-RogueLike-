import math
import tcod as libtcod

from render_functions import RenderOrder


class Entity:
    """
    Player Object
    """

    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder, fighter=None, ai=None,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # Player movement
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities,
                                                                                                   self.x + dx,
                                                                                                   self.y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # Creates a FOV map that contains the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and sets the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scans all the objects to see if there is any obstacles to navigate around
        # Checks that the object isn't itself or the target to ensure that the start and end points are free
        # If AI is next to the target then it will not use the A* approach
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* Path
        # 1.41 is set as the normal diagonal cost of moving and will be set to 0.0 if diagonal movements are not
        # possible
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between itself's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Checks if the path exists - the current path size is 25 tiles
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Finds the coordinates in the computed path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Sets the coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Uses the other move function as a backup incase if there is no paths for A*
            # Moves towards the target
            self.move_towards(target.x, target.y, game_map, entities)

        # Deletes the path
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
