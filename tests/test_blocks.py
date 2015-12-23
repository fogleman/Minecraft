import unittest

from model.block import Block
import model.block as block


class BlockTest(unittest.TestCase):

    def test_initialize_block(self):
        my_block = Block()

    def test_grass_block(self):
        my_block = block.GRASS
        self.assertEqual('grass', my_block.madeof)
        self.assertEqual(2, my_block.type_num)

    def test_stone_block(self):
        my_block = block.STONE
        self.assertEqual('stone', my_block.madeof)
        self.assertEqual(1, my_block.type_num)
