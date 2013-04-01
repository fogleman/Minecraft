class Inventory(object):
	  def __init__(self):
	      self.items = {}
	      
	  def add_item(self, item_id):
	      if item_id not in self.items:
  	        self.items[item_id] = 0
	      self.items[item_id] += 1
	      print "%s: %s" % (item_id, self.items[item_id])
	      
	  def remove_item(self, item_id):
	      if item_id in self.items:
  	        self.items[item_id] -= 1
  	        if self.items[item_id] <= 0:
  	            del self.items[item_id]
    	      else:
    	          print "%s: %s" % (item_id, self.items[item_id])
	      
	  def get_items(self):
	      return self.items
