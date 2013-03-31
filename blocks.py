def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

# Blocks
class Block(object):
    def __init__(self, top, bottom, side, hardness):
        self.top = top
        self.bottom = bottom
        self.side = side
        self.hardness = hardness

class AirBlock(Block):
    def __init__(self):
        # Air block has no texture
        super(AirBlock, self).__init__(tex_coord(-1,-1), tex_coord(-1,-1), tex_coord(-1,-1), 0)
    def id(self):
        return 0

class StoneBlock(Block):
    def __init__(self):
        super(StoneBlock, self).__init__(tex_coord(2,1), tex_coord(2,1), tex_coord(2,1), 1.5)
    def id(self):
        return 1

class GrassBlock(Block):
    def __init__(self):
        super(GrassBlock, self).__init__(tex_coord(1,0), tex_coord(0,1), tex_coord(0,0), 0.6)
    def id(self):
        return 2

class DirtBlock(Block):
    def __init__(self):
        super(DirtBlock, self).__init__(tex_coord(0,1), tex_coord(0,1), tex_coord(0,1), 0.5)
    def id(self):
        return 3

class SandBlock(Block):
    def __init__(self):
        super(SandBlock, self).__init__(tex_coord(1,1), tex_coord(1,1), tex_coord(1,1), 0.5)
    def id(self):
        return 12

class BrickBlock(Block):
    def __init__(self):
        super(BrickBlock, self).__init__(tex_coord(2,0), tex_coord(2,0), tex_coord(2,0), 1.5)
    def id(self):
        return 45

class GlassBlock(Block):
    def __init__(self):
        super(GlassBlock, self).__init__(tex_coord(3,1), tex_coord(3,1), tex_coord(3,1), 0.2)
    def id(self):
        return 20

class BedrockBlock(Block):
    def __init__(self):
        super(BedrockBlock, self).__init__(tex_coord(3,0), tex_coord(3,0), tex_coord(3,0), 99)
    def id(self):
        return 7


def block_texture(block):
    result = []
    result.extend(block.top)
    result.extend(block.bottom)
    result.extend(block.side * 4)
    return result

air_block = AirBlock()
grass_block = GrassBlock()
sand_block = SandBlock()
brick_block = BrickBlock()
stone_block = StoneBlock()
dirt_block = DirtBlock()
glass_block = GlassBlock()
bed_block = BedrockBlock()

BLOCKS = [grass_block, sand_block, brick_block, dirt_block, stone_block, glass_block, bed_block]

