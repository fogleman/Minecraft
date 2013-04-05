from blocks import *
from items import *

class Recipe(object):
	# ingre is a list that contains the ids of the ingredients
	# e.g. [[2, 2], [1, 1]]
	def __init__(self, ingre, output):
		# what blocks are needed to craft this block/item
		self.ingre = ingre
		self.output = output
		self.shapeless = False

class Recipes(object):
	def __init__(self):
		self.nr_recipes = 0
		self.recipes = []

	def remove_empty_line_col(self, ingre_list):
		# remove empty lines
		if len(ingre_list) == 0:
		    return
		    
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
					sub_ingre.append(air_block.id)
				else:
					sub_ingre.append(ingre[c].id)
			ingre_list.append(sub_ingre)

		self.remove_empty_line_col(ingre_list)

		return ingre_list

	def add_recipe(self, shape, ingre, output):
		self.recipes.append(Recipe(self.parse_recipe(shape, ingre), output))
		self.nr_recipes += 1

	def add_shapeless_recipe(self, ingre, output):
		ingre_list = [x.id for x in ingre if x.id != 0]
		ingre_list.sort()
		r = Recipe(ingre_list, output)
		r.shapeless = True
		self.recipes.append(r)

	def craft(self, input_blocks):
		id_list = []
		shapeless_id_list = []
		for line in input_blocks:
			id_list.append([b.id for b in line if b.id != 0])
			shapeless_id_list.extend([b.id for b in line if b.id != 0])
		shapeless_id_list.sort()
        
		self.remove_empty_line_col(id_list)
		for r in self.recipes:
			if r.shapeless:
				if r.ingre == shapeless_id_list:
					return r.output
			else:
				if r.ingre == id_list:
					return r.output

		return False

class SmeltingRecipe(object):
	def __init__(self, ingre, output):
		# what blocks are needed to craft this block/item
		self.ingre = ingre
		self.output = output.id

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

		return False


recipes = Recipes()
smelting = SmeltingRecipes()

# a test:
# grass | grass
#--------------  ---->  dirt
# grass | grass
recipes.add_recipe(["##", "##"], {'#': grass_block}, ItemStack(dirt_block.id, amount=1))
recipes.add_recipe(["##", "##"], {'#': stone_block}, ItemStack(stonebrick_block.id, amount=4))
recipes.add_shapeless_recipe([grass_block, stone_block], ItemStack(stone_block.id, amount=1))

if __name__ == '__main__':
    print(recipes.craft([ [grass_block, grass_block, air_block], \
					      [grass_block, grass_block, air_block], \
					      [air_block,   air_block,   air_block] ]))

    print(recipes.craft([ [air_block, grass_block, grass_block], \
				          [air_block, grass_block, grass_block], \
				          [air_block,   air_block,   air_block] ]))

    print(recipes.craft([ [air_block, stone_block, grass_block], \
				          [air_block, air_block, air_block], \
				          [air_block,   air_block,   air_block] ]))
