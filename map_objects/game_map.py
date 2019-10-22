from map_objects.tile import Tile
from random import randint
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # All titles are blocked unless otherwise
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):

        rooms = []
        num_rooms = 0

        for r in range(max_rooms):

            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            # Checks for intersection
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # if there is no intersections

                self.create_room(new_room)

                # center coordinates of the new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # The room where the player is spawned
                    player.x = new_x
                    player.y = new_y

                else:
                    # The rooms after the first room is created - connect it to the previous room
                    # The coordinates of the previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Randomly choose either vertical or horizontal connections
                    if randint(0, 1) == 1:
                        # Horizontal connection then vertical
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                    else:
                        # Vertical connection then horizontal
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, prev_y)

                # Append the new room to the list of rooms
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # Carves out a room out of the tiles and makes them passable/walkable
        # Leaves at least 1 tile for room separation
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Chooses a random location in a room
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
