import unittest

from block import Block
import block


class BlockTest(unittest.TestCase):

    def test_initialize_block(self):
        my_block = Block()

    def test_should_have_texture(self):
        my_block = Block()
        self.assertTrue(my_block.texture)

    def test_grass_texture(self):
        my_block = block.GRASS
        self.assertEqual(((1, 0), (0, 1), (0, 0)), my_block.texture_positions)
