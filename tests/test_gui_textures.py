import unittest
from model import block
from model.block import Block
from gui.texture import BlockTexture


class GuiTextureTest(unittest.TestCase):

    def test_should_find_texture(self):
        my_block = Block()
        texture = BlockTexture(my_block)
        self.assertTrue(texture)

    def test_grass_texture(self):
        texture = BlockTexture(block.GRASS)
        self.assertEqual(((1, 0), (0, 1), (0, 0)), texture.texture_positions)

    def test_sand_texture(self):
        texture = BlockTexture(block.SAND)
        self.assertEqual(((1, 1), (1, 1), (1, 1)), texture.texture_positions)

    def test_brick_texture(self):
        texture = BlockTexture(block.BRICK)
        self.assertEqual(((2, 0), (2, 0), (2, 0)), texture.texture_positions)

    def test_stone_texture(self):
        texture = BlockTexture(block.STONE)
        self.assertEqual(((2, 1), (2, 1), (2, 1)), texture.texture_positions)
