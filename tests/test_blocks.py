import unittest

from model.block import Block
import model.block as block


class BlockTest(unittest.TestCase):

    def test_initialize_block(self):
        my_block = Block()

    def test_should_have_texture(self):
        my_block = Block()
        self.assertTrue(my_block.texture)

    def test_grass_texture(self):
        my_block = block.GRASS
        self.assertEqual(((1, 0), (0, 1), (0, 0)), my_block.texture_positions)

    def test_sand_texture(self):
        my_block = block.SAND
        self.assertEqual(((1, 1), (1, 1), (1, 1)), my_block.texture_positions)

    def test_brick_texture(self):
        my_block = block.BRICK
        self.assertEqual(((2, 0), (2, 0), (2, 0)), my_block.texture_positions)

    def test_stone_texture(self):
        my_block = block.STONE
        self.assertEqual(((2, 1), (2, 1), (2, 1)), my_block.texture_positions)
