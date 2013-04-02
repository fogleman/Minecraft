from items import *

class Inventory(object):
    def __init__(self, slot_count = 27):
        self.slot_count = slot_count
        self.slots = [None] * self.slot_count

    def find_empty_slot(self):
        return next((index for index,value in enumerate(self.slots) if not value), -1)

    def add_item(self, item_id, quantity = 1):
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
            
        return True
          
    def remove_item(self, item_id, quantity = 1):
        if quantity < 1:
            return False
            
        index = self.get_index(item_id)
        return self.remove_by_index(index, quantity)
        
    def remove_by_index(self, index, quantity = 1):
        if quantity < 1 or index < 0 or not self.slots[index]:
            return False
            
        retval = False
        self.slots[index].change_amount(quantity*-1)
        if self.slots[index].amount == 0:
            self.slots[index] = None
            retval = True
        return retval
            
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
