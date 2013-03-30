def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

# Blocks
class Block(object):
    def __init__(self, top, bottom, side):
        self.top = top
        self.bottom = bottom
        self.side = side

class GrassBlock(Block):
    def __init__(self):
        super(GrassBlock, self).__init__(tex_coord(1,0), tex_coord(0,1), tex_coord(0,0))

class SandBlock(Block):
    def __init__(self):
        super(SandBlock, self).__init__(tex_coord(1,1), tex_coord(1,1), tex_coord(1,1))

class BrickBlock(Block):
    def __init__(self):
        super(BrickBlock, self).__init__(tex_coord(2,0), tex_coord(2,0), tex_coord(2,0))

class StoneBlock(Block):
    def __init__(self):
        super(StoneBlock, self).__init__(tex_coord(2,1), tex_coord(2,1), tex_coord(2,1))

class DirtBlock(Block):
    def __init__(self):
        super(DirtBlock, self).__init__(tex_coord(0,1), tex_coord(0,1), tex_coord(0,1))

def block_texture(block):
    result = []
    result.extend(block.top)
    result.extend(block.bottom)
    result.extend(block.side * 4)
    return result

grass_block = GrassBlock()
sand_block = SandBlock()
brick_block = BrickBlock()
stone_block = StoneBlock() 
dirt_block = DirtBlock()