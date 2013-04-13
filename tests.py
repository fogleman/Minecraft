# Imports, sorted alphabetically.

# Python packages
import random
import unittest

# Third-party packages
# Nothing for now...

# Modules from this project
from crafting import *
import globals as G
from inventory import Inventory
from items import ItemStack


class InventoryTests(unittest.TestCase):

    def test_init(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size)
            self.assertEqual(inv.slot_count, size)
            self.assertEqual(inv.slots, [None] * size)

    def test_find_empty_slot(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size).find_empty_slot()
            self.assertEqual(inv, 0 if size > 0 else -1)

    def test_add_1(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size)
            item = random.choice(G.ITEMS_DIR.keys())
            block = random.choice(G.BLOCKS_DIR.keys())
            result = inv.add_item(item)
            result2 = inv.add_item(block)
            if size == 0:
                self.assertFalse(result)
                self.assertFalse(result2)
            else:
                self.assertTrue(result)
                self.assertTrue(result2) 
                foundItem = False
                foundBlock = False
                for slot in inv.slots:
                    if slot:
                        if slot.type == item and slot.amount == 1:
                            foundItem = True
                        elif slot.type == block and slot.amount == 1:
                            foundBlock = True
                self.assertTrue(foundItem)
                self.assertTrue(foundBlock)
            self.assertEqual(result, result2)

    def test_add_2(self):
        inv = Inventory(slot_count=20)
        block = random.choice(G.BLOCKS_DIR.keys())
        max_items = G.BLOCKS_DIR[block].max_stack_size * 20
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        item = random.choice(G.ITEMS_DIR.keys())
        inv2 = Inventory(slot_count=20)
        max_items2 = G.ITEMS_DIR[item].max_stack_size * 20
        for i in xrange(0, max_items2):
            self.assertTrue(inv2.add_item(item))
        self.assertNotIn(None, inv.slots)
        self.assertNotIn(None, inv2.slots)
        for slot in inv.slots:
            self.assertEqual(slot.type, block)
            self.assertEqual(slot.amount, G.BLOCKS_DIR[block].max_stack_size)
        for slot in inv2.slots:
            self.assertEqual(slot.type, item)
            self.assertEqual(slot.amount, G.ITEMS_DIR[item].max_stack_size)

    def test_remove(self):
        inv = Inventory(slot_count=20)
        block = random.choice(G.BLOCKS_DIR.keys())
        max_items = G.BLOCKS_DIR[block].max_stack_size * 20
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        self.assertFalse(inv.remove_item(block, quantity=0))
        for i in xrange(0, 20):
            self.assertTrue(inv.remove_item(block, quantity=G.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        for i in xrange(0, 20):
            self.assertTrue(inv.remove_by_index(i, quantity=G.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in xrange(0, 20):
            inv.slots[i] = ItemStack(block, amount=1)
            inv.slots[i].change_amount(-1)
        inv.remove_unnecessary_stacks()
        self.assertEqual(inv.slots, [None] * 20)

class CraftingTests(unittest.TestCase):

    current_block_id = 0

    def generate_random_recipe(self, characters='#@'):
        recipe = []
        recipe2 = []
        recipe3 = []
        ingre = {}
        for character in characters:
            ingre[character] = G.BLOCKS_DIR.values()[self.current_block_id]
            self.current_block_id += 1
            if self.current_block_id >= len(G.BLOCKS_DIR.values()):
                self.current_block_id = 0
        for i in xrange(0, 3):
            recipe.append(''.join(random.choice(characters) for x in xrange(3)))
            recipe2.append([])
            for character in recipe[i]:
                recipe2[i].append(ingre[character])
                recipe3.append(ingre[character])
        return recipe, ingre, ItemStack(random.choice(G.BLOCKS_DIR.values()).id, amount=random.randint(1, 20)), recipe2, recipe3

    def test_add_1(self, characters='#@'):
        self.recipes = Recipes()
        recipes = []
        ingres = []
        outputs = []
        for i in xrange(0, 50):
            recipe, ingre, output, recipe2, recipe3 = self.generate_random_recipe(characters=characters)
            recipes.append(recipe2)
            ingres.append(ingre)
            outputs.append(output)
            self.recipes.add_recipe(recipe, ingre, output)
        self.assertEqual(self.recipes.nr_recipes, 50)
        for i, recipe in enumerate(recipes):
            self.assertEqual(self.recipes.craft(recipe), outputs[i])

    def test_add_2(self, characters='#@'):
        self.recipes = Recipes()
        recipes = []
        ingres = []
        outputs = []
        for i in xrange(0, 25):
            recipe, ingre, output, recipe2, recipe3 = self.generate_random_recipe(characters=characters)
            recipes.append(recipe2)
            ingres.append(ingre)
            outputs.append(output)
            self.recipes.add_shapeless_recipe(recipe3, output)
        for i, recipe in enumerate(recipes):
            self.assertEqual(self.recipes.craft(recipe), outputs[i])

    def test_add_3(self):
        self.recipes = Recipes()
        recipes = []
        ingres = []
        outputs = []
        for i in xrange(0, 25):
            shapeless = random.choice([True, False])
            if shapeless:
                recipe, ingre, output, recipe2, recipe3 = self.generate_random_recipe()
            else:
                recipe, ingre, output, recipe2, recipe3 = self.generate_random_recipe(characters='12')
            recipes.append(recipe2)
            ingres.append(ingre)
            outputs.append(output)
            if shapeless:
                self.recipes.add_shapeless_recipe(recipe3, output)
            else:
                self.recipes.add_recipe(recipe, ingre, output)
        for i, recipe in enumerate(recipes):
            self.assertEqual(self.recipes.craft(recipe), outputs[i])

    def test_add_4(self):
        self.test_add_1(characters='!@#$123456789')

    def test_add_5(self):
        self.test_add_2(characters='!@#$123456789')

if __name__ == '__main__':
    unittest.main()