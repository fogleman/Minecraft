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
            if len(line) == 0:
                continue
            sum = 0
            for id in line:
                sum = sum + id
            if sum == 0:    # empty line
                ingre_list.pop(i)

        #remove empty column
        for i in (0, -1):
            sum = 0
            for line in ingre_list:
                if len(line) == 0:
                    continue
                sum = sum + line[i]
            if sum == 0:
                for line in ingre_list:
                    if len(line) == 0:
                        continue
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
            id_list.append([b.id for b in
                            line])    # removed b.id != 0: it may make the
                            # shape different
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

        return None


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
# stone items
recipes.add_recipe(["##", "##"], {'#': stone_block},
                   ItemStack(stonebrick_block.id, amount=4))
recipes.add_recipe(["###", "# #", "###"], {'#': cobble_block},
                   ItemStack(furnace_block.id, amount=1))

# wood items
<<<<<<< HEAD
recipes.add_recipe(["#"], {'#': oakwood_block},
                   ItemStack(oakwoodplank_block.id, amount=4))
recipes.add_recipe(["#"], {'#': junglewood_block},
                   ItemStack(junglewoodplank_block.id, amount=4))
recipes.add_recipe(["#", "#"], {'#': oakwoodplank_block},
                   ItemStack(stick_item.id, amount=4))
recipes.add_recipe(["#", "#"], {'#': junglewoodplank_block},
                   ItemStack(stick_item.id, amount=4))
recipes.add_recipe(["#", "#"], {'#': oakwoodplank_block},
                   ItemStack(stick_item.id, amount=4))
recipes.add_recipe(["#", "#"], {'#': sprucewoodplank_block},
                   ItemStack(stick_item.id, amount=4))
recipes.add_recipe(["###", "# #", "###"], {'#': oakwoodplank_block},
                   ItemStack(chest_block.id, amount=1))
recipes.add_recipe(["###", "# #", "###"], {'#': sprucewoodplank_block},
                   ItemStack(chest_block.id, amount=1))
recipes.add_recipe(["###", "# #", "###"], {'#': junglewoodplank_block},
                   ItemStack(chest_block.id, amount=1))

recipes.add_recipe(["##", "##"], {'#': oakwoodplank_block},
                   ItemStack(craft_block.id, amount=1))
recipes.add_recipe(["##", "##"], {'#': sprucewoodplank_block},
                   ItemStack(craft_block.id, amount=1))
recipes.add_recipe(["##", "##"], {'#': junglewoodplank_block},
                   ItemStack(craft_block.id, amount=1))

#  wood axes
recipes.add_recipe(["###", "@", " @ "], {'#': sprucewoodplank_block, '@': stick_item},
                   ItemStack(wood_axe.id, amount=4))
recipes.add_recipe(["###", "@", " @ "], {'#': oakwoodplank_block, '@': stick_item},
                   ItemStack(wood_axe.id, amount=4))
recipes.add_recipe(["###", "@", " @ "], {'#': junglewoodplank_block, '@': stick_item},
                   ItemStack(wood_axe.id, amount=4))

#  diamond tools
recipes.add_recipe(["###", " @ ", " @ "], {'#': diamond_item, '@': stick_item},
                   ItemStack(diamond_pickaxe.id, amount=4))
recipes.add_recipe(["## ", "#@ ", " @ "], {'#': diamond_item, '@': stick_item},
                   ItemStack(diamond_axe.id, amount=4))
# stone tools
recipes.add_recipe(["###", " @ ", " @ "], {'#': cobble_block, '@': stick_item},
                   ItemStack(stone_axe.id, amount=4))
recipes.add_recipe(["## ", "#@ ", " @ "], {'#': cobble_block, '@': stick_item},
                   ItemStack(stone_pickaxe.id, amount=4))

#sand items
=======
recipes.add_shapeless_recipe((oakwood_block,), 
                    ItemStack(oakwoodplank_block.id, amount=4))
recipes.add_shapeless_recipe((junglewood_block,), 
                    ItemStack(junglewoodplank_block.id, amount=4))
for wood in (oakwoodplank_block, junglewoodplank_block, sprucewoodplank_block):
    recipes.add_recipe(["#", "#"], {'#': wood}, 
                        ItemStack(stick_item.id, amount=4))
    recipes.add_recipe(["###", "# #", "###"], {'#': wood},
                        ItemStack(chest_block.id, amount=1))
    recipes.add_recipe(["##", "##"], {'#': wood},
                        ItemStack(craft_block.id, amount=1))

# sand items
>>>>>>> 438451cba85112c9d332b3ca83fbf12b93b46f49
recipes.add_recipe(["##", "##"], {'#': sand_block},
                   ItemStack(sandstone_block.id, amount=1))

# dye items
recipes.add_recipe(["#"], {'#': yflowers_block},
                   ItemStack(yellowdye_item.id, amount=4))


# combined items
recipes.add_recipe(["#", "@"], {'#': coal_item, '@': stick_item},
                   ItemStack(torch_block.id, amount=4))
