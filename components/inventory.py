import tcod as libtcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Inventory is full, you cannot carry any more items!', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You have picked up a {0}'.format(item.name), libtcod.blue)
            })

            self.items.append(item)

        return results