class Inventory(object):
    def __init__(self):
        self.items = {}
	      
    def add_item(self, item_id, quantity = 1):
        if item_id not in self.items:
            self.items[item_id] = 0
        self.items[item_id] += quantity
        print "%s: %s" % (item_id, self.items[item_id])
	      
    def remove_item(self, item_id, quantity = 1):
        if item_id in self.items:
            self.items[item_id] -= quantity
            if self.items[item_id] <= 0:
                del self.items[item_id]
            else:
                print "%s: %s" % (item_id, self.items[item_id])

    def get_item(self, item_id):
        if item_id in self.items:
            return self.items[item_id]
        return 0

    def get_items(self):
        return self.items
