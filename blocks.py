def tex_coord(x, y, n=8):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


BLOCKS_DIR = {}


class Block(object):
    top = ()
    bottom = ()
    side = ()
    hardness = 0
    max_stack_size = 64
    amount_label_color = 255, 255, 255, 255
    transparent = False
    id = None  # Original minecraft id (also called data value).
               # Verify on http://www.minecraftwiki.net/wiki/Data_values
               # when creating a new "official" block.
    drop_id = None

    def __init__(self):
        self.drop_id = self.id
        BLOCKS_DIR[self.id] = self

    def get_texture_data(self):
        result = []
        result.extend(self.top)
        result.extend(self.bottom)
        result.extend(self.side * 4)
        return result


class AirBlock(Block):
    top = tex_coord(-1, -1)
    bottom = tex_coord(-1, -1)
    side = tex_coord(-1, -1)
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

    def __init__(self):
        self.drop_id = DirtBlock.id
        super(GrassBlock, self).__init__()


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
    amount_label_color = 0, 0, 0, 255
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
    amount_label_color = 0, 0, 0, 255
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
    transparent = True
    id = 8


class ChestBlock(Block):
    top = tex_coord(1, 2)
    bottom = tex_coord(1, 2)
    side = tex_coord(1, 2)
    id = 54


class SandstoneBlock(Block):
    top = tex_coord(2, 2)
    bottom = tex_coord(2, 2)
    side = tex_coord(2, 2)
    amount_label_color = 0, 0, 0, 255
    id = 24


# FIXME: This texture is not in the original Minecraft.  Or is it quartz?
class MarbleBlock(Block):
    top = tex_coord(3, 2)
    bottom = tex_coord(3, 2)
    side = tex_coord(3, 2)
    id = 0


class StonebrickBlock(Block):
    top = tex_coord(0, 3)
    bottom = tex_coord(0, 3)
    side = tex_coord(0, 3)
    id = 98


class OakWoodPlankBlock(Block):
    top = tex_coord(3, 3)
    bottom = tex_coord(3, 3)
    side = tex_coord(3, 3)
    id = 5.0


class SpruceWoodPlankBlock(Block):
    top = tex_coord(1, 3)
    bottom = tex_coord(1, 3)
    side = tex_coord(1, 3)
    id = 5.1


class JungleWoodPlankBlock(Block):
    top = tex_coord(2, 3)
    bottom = tex_coord(2, 3)
    side = tex_coord(2, 3)
    id = 5.3


# FIXME: Can't find its specific id on minecraftwiki.
class SnowGrassBlock(Block):
    top = tex_coord(4, 1)
    bottom = tex_coord(0, 1)
    side = tex_coord(4, 0)
    hardness = 0.6
    id = 2

    def __init__(self):
        self.drop_id = DirtBlock.id


class OakWoodBlock(Block):
    top = tex_coord(7, 1)
    bottom = tex_coord(7, 1)
    side = tex_coord(7, 0)
    hardness = 0.6
    id = 17.0


class LeafBlock(Block):
    top = tex_coord(7, 2)
    bottom = tex_coord(7, 2)
    side = tex_coord(7, 2)
    hardness = 0.6
    id = 18.0
    drop_id = None


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
oakwoodplank_block = OakWoodPlankBlock()
junglewoodplank_block = JungleWoodPlankBlock()
sprucewoodplank_block = SpruceWoodPlankBlock()
snowg_block = SnowGrassBlock()
log_block = OakWoodBlock()
leaf_block = LeafBlock()
