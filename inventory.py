from items import *

class Inventory(object):
    def __init__(self, slot_count = 27):
        self.slot_count = slot_count
        self.slots = [None] * self.slot_count
          
    def add_item(self, item_id, quantity = 1):
        if quantity < 1:
            return False

        item_stack = self.get_item(item_id)
        
        if item_stack:
            item_stack.change_amount(quantity)
        else:            
            index = next((index for index,value in enumerate(self.slots) if not value), -1)
            
            if index == -1 and len(self.slots) == self.slot_count:
                return False

            item_stack = ItemStack(type=item_id, amount=quantity)
            self.slots.insert(index, item_stack)
            
        return True
          
    def remove_item(self, item_id, quantity = 1):
        if quantity < 1:
            return False
            
        index = self.get_index(item_id)
        if index >= 0:
            self.slots[index].change_amount(quantity*-1)
            if self.slots[index].amount == 0:
                self.slots[index] = None
                return True
        return False
            
    def at(self, index):
        index = int(index)
        if index >= 0 and index < self.slot_count:
            return self.slots[index]
        return None
        
    def get_index(self, item_id):
        return next((index for index, x in enumerate(self.slots) if x and x.type == item_id), -1)

    def get_item(self, item_id):
        return next((x for x in self.slots if x and x.type == item_id), None)

    def get_items(self):
        return self.slots
        

class QuickSlots(Inventory):
    def __init__(self, slot_count = 9):
        super(QuickSlots, self).__init__(slot_count)