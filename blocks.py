import sounds

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
    density = 1
    transparent = False

    # Inventory attributes
    max_stack_size = 64
    amount_label_color = 255, 255, 255, 255
    name = "Block"  # Blocks that drop another item don't need a name

    def __init__(self):
        self.drop_id = self.id
        # Applies get_texture_coordinates to each of the faces to be textured.
        for k in ('top_texture', 'bottom_texture', 'side_texture'):
            v = getattr(self, k)
            setattr(self, k, get_texture_coordinates(*v))

        self.texture_data = self.get_texture_data()

        BLOCKS_DIR[self.id] = self

    def get_texture_data(self):
        result = []
        result.extend(self.top_texture)
        result.extend(self.bottom_texture)
        result.extend(self.side_texture * 4)
        return result

    def play_break_sound(self):
        pass

class AirBlock(Block):
    top_texture = -1, -1
    bottom_texture = -1, -1
    side_texture = -1, -1
    max_stack_size = 0
    density = 0
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
    density = 0.5
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
# from ronmurphy .. this is taken, as all images are, from the sphax purebd craft. it is marble, from the tekkit pack.
class MarbleBlock(Block):
    top_texture = 3, 2
    bottom_texture = 3, 2
    side_texture = 3, 2
    id = 0
    name = "Marble"
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

    def play_break_sound(self):
        sounds.wood_break.play()


class SpruceWoodPlankBlock(Block):
    top_texture = 1, 3
    bottom_texture = 1, 3
    side_texture = 1, 3
    id = 5.1
    name = "Spruce Wood Planks"

    def play_break_sound(self):
        sounds.wood_break.play()


class JungleWoodPlankBlock(Block):
    top_texture = 2, 3
    bottom_texture = 2, 3
    side_texture = 2, 3
    id = 5.3
    name = "Jungle Wood Planks"

    def play_break_sound(self):
        sounds.wood_break.play()


# FIXME: Can't find its specific id on minecraftwiki.
# from ronmurphy: This is just the snowy side grass from the above texture pack.  MC has one like this also.
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

    def play_break_sound(self):
        sounds.wood_break.play()

class JungleWoodBlock(Block):
    top_texture = 6, 1
    bottom_texture = 6, 1
    side_texture = 6, 0
    hardness = 0.6
    id = 17.1
    name = "Jungle wood"

    def play_break_sound(self):
        sounds.wood_break.play()

class BirchWoodBlock(Block):
    top_texture = 5, 1
    bottom_texture = 5, 1
    side_texture = 5, 0
    hardness = 0.6
    id = 17.2
    name = "Birch wood"

    def play_break_sound(self):
        sounds.wood_break.play()

class CactusBlock(Block):
    top_texture = 7, 5
    bottom_texture = 7, 3
    side_texture = 7, 4
    hardness = 0.6
    id = 17.0
    name = "Cactus"

class OakLeafBlock(Block):
    top_texture = 7, 2
    bottom_texture = 7, 2
    side_texture = 7, 2
    hardness = 0.2
    id = 18.0
    name = "Oak Leaves"


    def __init__(self):
        super(OakLeafBlock, self).__init__()
        self.drop_id = None

class JungleLeafBlock(Block):
    top_texture = 6, 2
    bottom_texture = 6, 2
    side_texture = 6, 2
    hardness = 0.6
    id = 18.1
    name = "Jungle Leaves"

    def __init__(self):
        super(JungleLeafBlock, self).__init__()
        self.drop_id = None

class BirchLeafBlock(Block):
    top_texture = 5, 2
    bottom_texture = 5, 2
    side_texture = 5, 2
    hardness = 0.6
    id = 18.2
    name = "Birch Leaves"

    def __init__(self):
        super(BirchLeafBlock, self).__init__()
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
oakleaf_block = OakLeafBlock()
junglewood_block = JungleWoodBlock()
jungleleaf_block = JungleLeafBlock()
birchwood_block = BirchWoodBlock()
birchleaf_block = BirchLeafBlock()
cactus_block = CactusBlock()
