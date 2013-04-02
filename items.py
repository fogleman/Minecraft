class Item(object):
    def __init__(self):
        self.max_stack_size = 0

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
        
    def change_amount(self, change=0):
        if change == 0:
            return
        self.amount += change
        if self.amount < 0:
            self.amount = 0
