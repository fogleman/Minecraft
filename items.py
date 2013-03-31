class Item(object):
	def __init__(self):
		self.max_stack_size = 0

	def on_right_click(self):
		pass

class ItemStack(object):
	def __init__(self, type = 0, amount = 0, durability = -1, data = 0):
		self.type = type
		self.amount = amount
		self. durability =  durability
		self.data = data
