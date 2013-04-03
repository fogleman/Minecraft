def tex_coord(x, y, n=8):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


BLOCKS_DIR = {}


class Block(object):
    top = None
    bottom = None
    side = None
    hardness = None
    max_stack_size = 64
    amount_label_color = (255, 255, 255, 255)
    transparent = False
    id = None

    def __init__(self):
        BLOCKS_DIR[self.id] = self

    def drop(self):
        return self.id


class AirBlock(Block):
    top = tex_coord(-1, -1)
    bottom = tex_coord(-1, -1)
    side = tex_coord(-1, -1)
    hardness = 0
    max_stack_size = 0
    id = 0


class StoneBlock(Block):
    top = tex_coord(2, 1)
    bottom = tex_coord(2, 1)
    side = tex_coord(2, 1)
    hardness = 1.5
    id = 1


class GrassBlock(Block):
    top = tex_coord(1, 0)
    bottom = tex_coord(0, 1)
    side = tex_coord(0, 0)
    hardness = 0.6
    id = 2

    def drop(self):
        return DirtBlock.id


class DirtBlock(Block):
    top = tex_coord(0, 1)
    bottom = tex_coord(0, 1)
    side = tex_coord(0, 1)
    hardness = 0.5
    id = 3


class SandBlock(Block):
    top = tex_coord(1, 1)
    bottom = tex_coord(1, 1)
    side = tex_coord(1, 1)
    hardness = 0.5
    amount_label_color = (0, 0, 0, 255)
    id = 12


class BrickBlock(Block):
    top = tex_coord(2, 0)
    bottom = tex_coord(2, 0)
    side = tex_coord(2, 0)
    hardness = 1.5
    id = 45


class GlassBlock(Block):
    top = tex_coord(3, 1)
    bottom = tex_coord(3, 1)
    side = tex_coord(3, 1)
    hardness = 0.2
    amount_label_color = (0, 0, 0, 255)
    id = 20


class BedrockBlock(Block):
    top = tex_coord(3, 0)
    bottom = tex_coord(3, 0)
    side = tex_coord(3, 0)
    hardness = -1  # Unbreakable
    id = 7


class WaterBlock(Block):
    top = tex_coord(0, 2)
    bottom = tex_coord(0, 2)
    side = tex_coord(0, 2)
    hardness = 0
    transparent = True
    id = 8


class ChestBlock(Block):
    top = tex_coord(1, 2)
    bottom = tex_coord(1, 2)
    side = tex_coord(1, 2)
    hardness = 0
    id = 54


class SandstoneBlock(Block):
    top = tex_coord(2, 2)
    bottom = tex_coord(2, 2)
    side = tex_coord(2, 2)
    hardness = 0
    amount_label_color = (0, 0, 0, 255)
    id = 24


class MarbleBlock(Block):
    top = tex_coord(3, 2)
    bottom = tex_coord(3, 2)
    side = tex_coord(3, 2)
    hardness = 0
    id = 0  # Why the same id than AirBlock and StonebrickBlock?


class StonebrickBlock(Block):
    top = tex_coord(0, 3)
    bottom = tex_coord(0, 3)
    side = tex_coord(0, 3)
    hardness = 0
    id = 0  # Why the same id than AirBlock and MarbleBlock?


class LWoodBlock(Block):
    top = tex_coord(3, 3)
    bottom = tex_coord(3, 3)
    side = tex_coord(3, 3)
    hardness = 0
    id = 5.1


class MWoodBlock(Block):
    top = tex_coord(2, 3)
    bottom = tex_coord(2, 3)
    side = tex_coord(2, 3)
    hardness = 0
    id = 5.2


class DWoodBlock(Block):
    top = tex_coord(1, 3)
    bottom = tex_coord(1, 3)
    side = tex_coord(1, 3)
    hardness = 0
    id = 5.3


class SnowGrassBlock(Block):
    top = tex_coord(4, 1)
    bottom = tex_coord(0, 1)
    side = tex_coord(4, 0)
    hardness = 0.6
    id = 2

    def drop(self):
        return DirtBlock.id


class TreeTrunkBlock(Block):
    top = tex_coord(7, 1)
    bottom = tex_coord(7, 1)
    side = tex_coord(7, 0)
    hardness = 0.6
    id = 17  # MC Log ID


class LeafBlock(Block):
    top = tex_coord(7, 2)
    bottom = tex_coord(7, 2)
    side = tex_coord(7, 2)
    hardness = 0.6
    id = 2

    def drop(self):
        return 0  # Why the same id than AirBlock, MarbleBlock and StonebrickBlock?

def block_texture(block):
    result = []
    result.extend(block.top)
    result.extend(block.bottom)
    result.extend(block.side * 4)  # 4
    return result


air_block = AirBlock()
grass_block = GrassBlock()
sand_block = SandBlock()
brick_block = BrickBlock()
stone_block = StoneBlock()
dirt_block = DirtBlock()
glass_block = GlassBlock()
bed_block = BedrockBlock()
water_block = WaterBlock()
chest_block = ChestBlock()
sandstone_block = SandstoneBlock()
marble_block = MarbleBlock()
stonebrick_block = StonebrickBlock()
lw_block = LWoodBlock()
mw_block = MWoodBlock()
dw_block = DWoodBlock()
snowg_block = SnowGrassBlock()
log_block = TreeTrunkBlock()
leaf_block = LeafBlock()
