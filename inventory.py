from items import *
import sys

class Inventory(object):
    def __init__(self, slot_count = 27):
        self.slot_count = slot_count
        self.slots = [None] * self.slot_count
        self.sort_mode = 0

    def find_empty_slot(self):
        return next((index for index,value in enumerate(self.slots) if not value), -1)

    def add_item(self, item_id, quantity = 1):
        self.sort()
        if quantity < 1:
            return False

        item_stack = self.get_item(item_id)
        if item_id >= ITEM_ID_MIN:
            max_size = ITEMS_DIR[item_id].max_stack_size
        else:
            max_size = BLOCKS_DIR[item_id].max_stack_size

        if item_stack:
            retval = False
            while quantity > 0:
                # can't find an unfilled slot
                if not item_stack:
                    # find an empty slot to store these items
                    index = self.find_empty_slot()
            
                    if index == -1 and len(self.slots) == self.slot_count:
                        return retval

                    # overflow ?
                    if quantity > max_size:
                        quantity -= max_size
                        item_stack = ItemStack(type=item_id, amount=max_size)
                    else: 
                        item_stack = ItemStack(type=item_id, amount=quantity)
                        quantity = 0

                    self.slots.insert(index, item_stack)
                    retval = True
                else:
                    capacity = max_size - item_stack.amount
                    if quantity < capacity:     # there is a slot with enough space
                        item_stack.change_amount(quantity)
                        self.sort()
                        return True
                    else:   # overflow
                        quantity -= capacity
                        item_stack.change_amount(capacity)
                        # find next unfilled slot
                        item_stack = self.get_unfilled_item(item_id)

        else:            
            while quantity > 0:
                index = self.find_empty_slot()
            
                retval = False
                if index == -1 and len(self.slots) == self.slot_count:
                    return retval

                # overflow ?
                if quantity > max_size:
                    quantity -= max_size
                    item_stack = ItemStack(type=item_id, amount=max_size)
                else: 
                    item_stack = ItemStack(type=item_id, amount=quantity)
                    quantity = 0

                self.slots.insert(index, item_stack)
                retval = True
        self.sort()   
        return True
          
    def remove_item(self, item_id, quantity = 1):
        self.sort()
        if quantity < 1:
            return False
            
        index = self.get_index(item_id)
        if index >= 0:
            self.slots[index].change_amount(quantity*-1)
            if self.slots[index].amount == 0:
                self.slots[index] = None
                self.sort()
                return True
        self.sort()
        return False
            
    def sort(self, reverse=True):
        if self.sort_mode == 0:
            self.sort_with_key(key=lambda x: x.id() if x != None else -sys.maxint - 1, reverse=True) 
        if self.sort_mode == 1:
            self.sort_with_key(key=lambda x: x.amount if x != None else -sys.maxint - 1, reverse=True)
        elif self.sort_mode == 2:
            self.sort_with_key(key=lambda x: x.amount if x != None else sys.maxint - 1, reverse=False)

    def sort_with_key(self, key, reverse=True):
        self.slots = sorted(self.slots, key=key, reverse=reverse) 

    def change_sort_mode(self, change=1):
        self.sort_mode += change
        if self.sort_mode > 2:
            self.sort_mode = 0
        elif self.sort_mode < 0:
            self.sort_mode = 2
        self.sort()

    def at(self, index):
        index = int(index)
        if index >= 0 and index < self.slot_count:
            return self.slots[index]
        return None
        
    def get_index(self, item_id):
        return next((index for index, x in enumerate(self.slots) if x and x.type == item_id), -1)

    def get_item(self, item_id):
        return next((x for x in self.slots if x and x.type == item_id), None)

    def get_unfilled_item(self, item_id):
        return next((x for x in self.slots if x and (x.type == item_id) and (x.amount < x.max_stack_size)), None)

    def get_items(self):
        return self.slots
