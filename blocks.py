def tex_coord(x, y, n=8):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

BLOCKS_DIR = {}

# Blocks
class Block(object):
    transparent = False
    def __init__(self, top, bottom, side, hardness, max_stack_size, amount_label_color=(255, 255, 255, 255)):
        self.top = top
        self.bottom = bottom
        self.side = side
        self.hardness = hardness
        self.max_stack_size = max_stack_size
        self.amount_label_color = amount_label_color
        self.transparent = False
        BLOCKS_DIR[self.id()] = self
    def drop(self):
        return self.id()

class AirBlock(Block):
    def __init__(self):
        # Air block has no texture
        super(AirBlock, self).__init__(tex_coord(-1,-1), tex_coord(-1,-1), tex_coord(-1,-1), 0, 0, (255, 255, 255, 255))
    def id(self):
        return 0

class StoneBlock(Block):
    def __init__(self):
        super(StoneBlock, self).__init__(tex_coord(2,1), tex_coord(2,1), tex_coord(2,1), 1.5, 64, (255, 255, 255, 255))
    def id(self):
        return 1

class GrassBlock(Block):
    def __init__(self):
        super(GrassBlock, self).__init__(tex_coord(1,0), tex_coord(0,1), tex_coord(0,0), 0.6, 64, (255, 255, 255, 255))
    def id(self):
        return 2
    def drop(self):
        return DirtBlock().id()

class DirtBlock(Block):
    def __init__(self):
        super(DirtBlock, self).__init__(tex_coord(0,1), tex_coord(0,1), tex_coord(0,1), 0.5, 64, (255, 255, 255, 255))
    def id(self):
        return 3

class SandBlock(Block):
    def __init__(self):
        super(SandBlock, self).__init__(tex_coord(1,1), tex_coord(1,1), tex_coord(1,1), 0.5, 64, (0, 0, 0, 255))
    def id(self):
        return 12

class BrickBlock(Block):
    def __init__(self):
        super(BrickBlock, self).__init__(tex_coord(2,0), tex_coord(2,0), tex_coord(2,0), 1.5, 64, (255, 255, 255, 255))
    def id(self):
        return 45

class GlassBlock(Block):
    def __init__(self):
        super(GlassBlock, self).__init__(tex_coord(3,1), tex_coord(3,1), tex_coord(3,1), 0.2, 64, (0, 0, 0, 255))
    def id(self):
        return 20

class BedrockBlock(Block):
    def __init__(self):
        # !! hardness = -1
        super(BedrockBlock, self).__init__(tex_coord(3,0), tex_coord(3,0), tex_coord(3,0), -1, 64, (255, 255, 255, 255))
    def id(self):
        return 7

class WaterBlock(Block):
    def __init__(self):
        super(WaterBlock, self).__init__(tex_coord(0, 2), tex_coord(0, 2), tex_coord(0, 2), 0, 64)
        self.transparent = True
    def id(self):
        return 8

class ChestBlock(Block):
    def __init__(self):
        super(ChestBlock, self).__init__(tex_coord(1, 2), tex_coord(1, 2), tex_coord(1, 2), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 54

class SandstoneBlock(Block):
    def __init__(self):
        super(SandstoneBlock, self).__init__(tex_coord(2, 2), tex_coord(2, 2), tex_coord(2, 2), 0, 64, (0, 0, 0, 255))
    def id(self):
        return 24

class MarbleBlock(Block):
    def __init__(self):
        super(MarbleBlock, self).__init__(tex_coord(3, 2), tex_coord(3, 2), tex_coord(3, 2), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 0

class StonebrickBlock(Block):
    def __init__(self):
        super(StonebrickBlock, self).__init__(tex_coord(0, 3), tex_coord(0, 3), tex_coord(0, 3), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 0

class LWoodBlock(Block):
    def __init__(self):
        super(LWoodBlock, self).__init__(tex_coord(3, 3), tex_coord(3, 3), tex_coord(3, 3), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 5.1

class MWoodBlock(Block):
    def __init__(self):
        super(MWoodBlock, self).__init__(tex_coord(2, 3), tex_coord(2, 3), tex_coord(2, 3), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 5.2

class DWoodBlock(Block):
    def __init__(self):
        super(DWoodBlock, self).__init__(tex_coord(1, 3), tex_coord(1, 3), tex_coord(1, 3), 0, 64, (255, 255, 255, 255))
    def id(self):
        return 5.3

class SnowGrassBlock(Block):
    def __init__(self):
        super(SnowGrassBlock, self).__init__(tex_coord(4, 1), tex_coord(0, 1), tex_coord(4, 0), 0.6, 64, (255, 255, 255, 255))
    def id(self):
        return 2
    def drop(self):
        return DirtBlock().id()

class TreeTrunkBlock(Block):
    def __init__(self):
        super(TreeTrunkBlock, self).__init__(tex_coord(7, 1), tex_coord(7, 1), tex_coord(7, 0), 0.6, 64, (255, 255, 255, 255))
    def id(self):
        return 17 # MC Log ID
    def drop(self):
        return TreeTrunkBlock().id()

class LeafBlock(Block):
    def __init__(self):
        super(LeafBlock, self).__init__(tex_coord(7, 2), tex_coord(7, 2), tex_coord(7, 2), 0.6, 64, (255, 255, 255, 255))
    def id(self):
        return 2
    def drop(self):
        return 0

def block_texture(block):
    result = []
    result.extend(block.top)
    result.extend(block.bottom)
    result.extend(block.side * 4) #4
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

