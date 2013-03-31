from blocks import *
from items import *

class Recipe(object):
	# ingre is a list that contains the ids of the ingredients
	# e.g. [[2, 2], [1, 1]]
	def __init__(self, ingre, output):
		# what blocks are needed to craft this block/item
		self.ingre = ingre
		self.output = output.id()

class Recipes(object):
	def __init__(self):
		self.nr_recipes = 0
		self.recipes = []

	def remove_empty_line_col(self, ingre_list):
		# remove empty lines
		for i in (0, -1):
			line = ingre_list[i]
			sum = 0
			for id in line:
				sum = sum + id
			if sum == 0:	# empty line
				ingre_list.pop(i)

		#remove empty column
		for i in (0, -1):
			sum = 0
			for line in ingre_list:
				sum = sum + line[i]
			if sum == 0:
				for line in ingre_list:
					line.pop(i)

	def parse_recipe(self, shape, ingre):
		ingre_list = []

		for line in shape:
			sub_ingre = []

			# line length should not be greater than 3
			if len(line) > 3:
				print('add_recipe(): line length should be <= 3!')
				return

			for c in line:
				if c == ' ':
					sub_ingre.append(air_block.id())
				else:
					sub_ingre.append(ingre[c].id())
			ingre_list.append(sub_ingre)

		self.remove_empty_line_col(ingre_list)

		return ingre_list

	def add_recipe(self, shape, ingre, output):
		self.recipes.append(Recipe(self.parse_recipe(shape, ingre), output))
		self.nr_recipes += 1

	def craft(self, input_blocks):
		id_list = []
		for line in input_blocks:
			id_list.append([b.id() for b in line])

		self.remove_empty_line_col(id_list)
		for r in self.recipes:
			if r.ingre == id_list:
				return r.output

class SmeltingRecipe(object):
	def __init__(self, ingre, output):
		# what blocks are needed to craft this block/item
		self.ingre = ingre
		self.output = output.id()

class SmeltingRecipes(object):
	def __init__(self):
		self.nr_recipes = 0
		self.recipes = []

	def add_recipe(self, ingre, output):
		self.recipes.append(SmeltingRecipe(ingre, output))
		self.nr_recipes += 1

	def smelt(self, ingre):
		for r in self.recipes:
			if r.ingre == ingre:
				return r.output


recipes = Recipes()
smelting = SmeltingRecipes()

# a test:
# grass | grass
#--------------  ---->  dirt
# grass | grass
recipes.add_recipe(["##", "##"], {'#': grass_block}, dirt_block)

recipes.craft([ [grass_block, grass_block, air_block], \
					  [grass_block, grass_block, air_block], \
					  [air_block,   air_block,   air_block] ])

recipes.craft([ [air_block, grass_block, grass_block], \
				      [air_block, grass_block, grass_block], \
				      [air_block,   air_block,   air_block] ])
