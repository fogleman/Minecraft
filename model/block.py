""" Basic unit of the game. Cube of 1x1x1 """
inventory = {}
inventory['grass'] = 2
inventory['sand'] = 2
inventory['brick'] = 2
inventory['stone'] = 1


class Block:
    """ Represents a block made out of one of the materials available
    in the inventory. """

    def __init__(self, madeof='grass'):
        self.type_num = inventory[madeof]
        self.madeof = madeof

    def __repr__(self):
        return self.madeof

GRASS = Block('grass')
BRICK = Block('brick')
SAND = Block('sand')
STONE = Block('stone')
