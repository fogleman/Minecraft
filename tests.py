import unittest
import random
from inventory import Inventory
from items import ItemStack
import globals

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
            item = random.choice(globals.ITEMS_DIR.keys())
            block = random.choice(globals.BLOCKS_DIR.keys())
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
        block = random.choice(globals.BLOCKS_DIR.keys())
        max_items = globals.BLOCKS_DIR[block].max_stack_size * 20
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        item = random.choice(globals.ITEMS_DIR.keys())
        inv2 = Inventory(slot_count=20)
        max_items2 = globals.ITEMS_DIR[item].max_stack_size * 20
        for i in xrange(0, max_items2):
            self.assertTrue(inv2.add_item(item))
        self.assertNotIn(None, inv.slots)
        self.assertNotIn(None, inv2.slots)
        for slot in inv.slots:
            self.assertEqual(slot.type, block)
            self.assertEqual(slot.amount, globals.BLOCKS_DIR[block].max_stack_size)
        for slot in inv2.slots:
            self.assertEqual(slot.type, item)
            self.assertEqual(slot.amount, globals.ITEMS_DIR[item].max_stack_size)

    def test_remove(self):
        inv = Inventory(slot_count=20)
        block = random.choice(globals.BLOCKS_DIR.keys())
        max_items = globals.BLOCKS_DIR[block].max_stack_size * 20
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        self.assertFalse(inv.remove_item(block, quantity=0))
        for i in xrange(0, 20):
            self.assertTrue(inv.remove_item(block, quantity=globals.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in xrange(0, max_items):
            self.assertTrue(inv.add_item(block))
        for i in xrange(0, 20):
            self.assertTrue(inv.remove_by_index(i, quantity=globals.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in xrange(0, 20):
            inv.slots[i] = ItemStack(block, amount=1)
            inv.slots[i].change_amount(-1)
        inv.remove_unnecessary_stacks()
        self.assertEqual(inv.slots, [None] * 20)

if __name__ == '__main__':
    unittest.main()