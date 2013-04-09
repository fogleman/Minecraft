from blocks import *
# items and blocks share a common id table
# ids of items should be >= ITEM_ID_MIN
ITEM_ID_MIN = 256

# From MinecraftWiki
# Items are objects which do not exist outside of the player's inventory and hands 
# i.e., they cannot be placed in the game world. 
# Some items simply place blocks or entities into the game world when used.
# Type
# * Materials: iron ingot, gold ingot, etc.
# * Food: found or crafted by the player and eaten to regain hunger points
# * Poitions
# * Tools
# * Informative items: map, compass and clock
# * Weapons
# * Armor

ITEMS_DIR = {}

class Item(object):
    id = None
    max_stack_size = 0
    amount_label_color = 255, 255, 255, 255
    name = "Item"

    def __init__(self):
        ITEMS_DIR[self.id] = self

    def on_right_click(self):
        pass

class ItemStack(object):
    def __init__(self, type = 0, amount = 1, durability = -1, data = 0):
        if amount < 1:
            amount = 1
        self.type = type
        self.amount = amount
        self.durability = durability
        self.data = data
        if type >= ITEM_ID_MIN:
            self.max_stack_size = ITEMS_DIR[type].max_stack_size
        else:
            self.max_stack_size = BLOCKS_DIR[type].max_stack_size

    # for debugging
    def __repr__(self):
        return '{ Item stack with type = ' + str(self.type) + ' }'

    def change_amount(self, change=0):
        overflow = 0
        if change != 0:
            self.amount += change
            if self.amount < 0:
                self.amount = 0
            elif self.amount > self.max_stack_size:
                overflow = self.amount - self.max_stack_size
                self.amount -= overflow

        return overflow

    # compatible with blocks
    @property
    def id(self):
        return self.type

    # compatible with blocks
    @property
    def name(self):
        if self.id >= ITEM_ID_MIN:
            return ITEMS_DIR[self.id].name
        else:
            return BLOCKS_DIR[self.id].name

class WoodAxe(Item):
    max_stack_size = 1
    id = 271
    name = "Wooden Axe"

wood_axe = WoodAxe()