from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURNS = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
