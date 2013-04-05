from blocks import *
# items and blocks share a common id table
# ids of items should be >= ITEM_ID_MIN
ITEM_ID_MIN = 256

ITEMS_DIR = {}

class Item(object):
    def __init__(self, max_stack_size):
        self.max_stack_size = max_stack_size
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
        return BLOCKS_DIR[self.id].name

