def get_texture_coordinates(x, y, tileset_size=8):
    m = 1.0 / tileset_size
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


BLOCKS_DIR = {}


class Block(object):
    id = None  # Original minecraft id (also called data value).
               # Verify on http://www.minecraftwiki.net/wiki/Data_values
               # when creating a new "official" block.
    drop_id = None

    # Texture coordinates from the tileset.
    top_texture = ()
    bottom_texture = ()
    side_texture = ()

    # Physical attributes
    hardness = 0
    transparent = False

    # Inventory attributes
    max_stack_size = 64
    amount_label_color = 255, 255, 255, 255
    name = "Block"

    def __init__(self):
        self.drop_id = self.id
        # Applies get_texture_coordinates to each of the faces to be textured.
        for k in ('top_texture', 'bottom_texture', 'side_texture'):
            v = getattr(self, k)
            setattr(self, k, get_texture_coordinates(*v))

        BLOCKS_DIR[self.id] = self

    def get_texture_data(self):
        result = []
        result.extend(self.top_texture)
        result.extend(self.bottom_texture)
        result.extend(self.side_texture * 4)
        return result


class AirBlock(Block):
    top_texture = -1, -1
    bottom_texture = -1, -1
    side_texture = -1, -1
    max_stack_size = 0
    id = 0
    name = "Air"


class StoneBlock(Block):
    top_texture = 2, 1
    bottom_texture = 2, 1
    side_texture = 2, 1
    hardness = 1.5
    id = 1
    name = "Stone"


class GrassBlock(Block):
    top_texture = 1, 0
    bottom_texture = 0, 1
    side_texture = 0, 0
    hardness = 0.6
    id = 2

    def __init__(self):
        super(GrassBlock, self).__init__()
        self.drop_id = DirtBlock.id


class DirtBlock(Block):
    top_texture = 0, 1
    bottom_texture = 0, 1
    side_texture = 0, 1
    hardness = 0.5
    id = 3
    name = "Dirt"


class SandBlock(Block):
    top_texture = 1, 1
    bottom_texture = 1, 1
    side_texture = 1, 1
    hardness = 0.5
    amount_label_color = 0, 0, 0, 255
    id = 12
    name = "Sand"


class BrickBlock(Block):
    top_texture = 2, 0
    bottom_texture = 2, 0
    side_texture = 2, 0
    hardness = 1.5
    id = 45
    name = "Bricks"


class GlassBlock(Block):
    top_texture = 3, 1
    bottom_texture = 3, 1
    side_texture = 3, 1
    hardness = 0.2
    amount_label_color = 0, 0, 0, 255
    id = 20
    name = "Glass"


class BedrockBlock(Block):
    top_texture = 3, 0
    bottom_texture = 3, 0
    side_texture = 3, 0
    hardness = -1  # Unbreakable
    id = 7
    name = "Bedrock"


class WaterBlock(Block):
    top_texture = 0, 2
    bottom_texture = 0, 2
    side_texture = 0, 2
    transparent = True
    hardness = -1  # Unobtainable
    id = 8
    name = "Water"


class ChestBlock(Block):
    top_texture = 1, 2
    bottom_texture = 1, 2
    side_texture = 1, 2
    id = 54
    name = "Chest"


class SandstoneBlock(Block):
    top_texture = 2, 2
    bottom_texture = 2, 2
    side_texture = 2, 2
    amount_label_color = 0, 0, 0, 255
    id = 24
    name = "Sandstone"


# FIXME: This texture is not in the original Minecraft.  Or is it quartz?
class MarbleBlock(Block):
    top_texture = 3, 2
    bottom_texture = 3, 2
    side_texture = 3, 2
    id = 0
    amount_label_color = 0, 0, 0, 255


class StonebrickBlock(Block):
    top_texture = 0, 3
    bottom_texture = 0, 3
    side_texture = 0, 3
    id = 98
    name = "Stone Bricks"


class OakWoodPlankBlock(Block):
    top_texture = 3, 3
    bottom_texture = 3, 3
    side_texture = 3, 3
    id = 5.0
    name = "Oak Wood Planks"


class SpruceWoodPlankBlock(Block):
    top_texture = 1, 3
    bottom_texture = 1, 3
    side_texture = 1, 3
    id = 5.1
    name = "Spruce Wood Planks"


class JungleWoodPlankBlock(Block):
    top_texture = 2, 3
    bottom_texture = 2, 3
    side_texture = 2, 3
    id = 5.3
    name = "Jungle Wood Planks"


# FIXME: Can't find its specific id on minecraftwiki.
class SnowGrassBlock(Block):
    top_texture = 4, 1
    bottom_texture = 0, 1
    side_texture = 4, 0
    hardness = 0.6
    id = 2

    def __init__(self):
        super(SnowGrassBlock, self).__init__()
        self.drop_id = DirtBlock.id


class OakWoodBlock(Block):
    top_texture = 7, 1
    bottom_texture = 7, 1
    side_texture = 7, 0
    hardness = 0.6
    id = 17.0
    name = "Oak wood"


class LeafBlock(Block):
    top_texture = 7, 2
    bottom_texture = 7, 2
    side_texture = 7, 2
    hardness = 0.1
    id = 18.0

    def __init__(self):
        super(LeafBlock, self).__init__()
        self.drop_id = None


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
snowgrass_block = SnowGrassBlock()
oakwood_block = OakWoodBlock()
leaf_block = LeafBlock()
