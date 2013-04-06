from globals import *
import sounds


def get_texture_coordinates(x, y, tileset_size=TERRAINMAP_BLOCK_SIZE):
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

    width = 1.0
    height = 1.0

    # Texture coordinates from the tileset.
    top_texture = ()
    bottom_texture = ()
    side_texture = ()

    # Sounds
    break_sound = None

    # Physical attributes
    hardness = 0    # hardness can be found on http://www.minecraftwiki.net/wiki/Digging#Blocks_by_hardness
    density = 1
    transparent = False

    # Inventory attributes
    max_stack_size = 64
    amount_label_color = 255, 255, 255, 255
    name = "Block"  # Blocks that drop another item don't need a name

    def __init__(self, width=None, height=None):
        self.drop_id = self.id

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        # Applies get_texture_coordinates to each of the faces to be textured.
        for k in ('top_texture', 'bottom_texture', 'side_texture'):
            v = getattr(self, k)
            if v:
                setattr(self, k, get_texture_coordinates(*v))

        self.texture_data = self.get_texture_data()

        BLOCKS_DIR[self.id] = self

    def get_texture_data(self):
        result = []
        result.extend(self.top_texture)
        result.extend(self.bottom_texture)
        result.extend(self.side_texture * 4)
        return result

    def get_vertices(self, x, y, z):
        w = self.width / 2.0
        h = self.height / 2.0
        xm = x - w
        xp = x + w
        ym = y - h
        yp = y + h
        zm = z - w
        zp = z + w
        return [
            xm,yp,zm, xm,yp,zp, xp,yp,zp, xp,yp,zm,  # top
            xm,ym,zm, xp,ym,zm, xp,ym,zp, xm,ym,zp,  # bottom
            xm,ym,zm, xm,ym,zp, xm,yp,zp, xm,yp,zm,  # left
            xp,ym,zp, xp,ym,zm, xp,yp,zm, xp,yp,zp,  # right
            xm,ym,zp, xp,ym,zp, xp,yp,zp, xm,yp,zp,  # front
            xp,ym,zm, xm,ym,zm, xm,yp,zm, xp,yp,zm,  # back
        ]

    def play_break_sound(self):
        if self.break_sound is not None:
            self.break_sound.play()


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

    def __init__(self):
        super(StoneBlock, self).__init__()
        self.drop_id = CobbleBlock.id


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


class GoldOreBlock(Block):
    top_texture = 3, 4
    bottom_texture = 3, 4
    side_texture = 3, 4
    hardness = 3
    id = 14
    name = "Coal Ore"


class IronOreBlock(Block):
    top_texture = 1, 4
    bottom_texture = 1, 4
    side_texture = 1, 4
    hardness = 3
    id = 15
    name = "Iron Ore"


class DiamondOreBlock(Block):
    top_texture = 2, 4
    bottom_texture = 2, 4
    side_texture = 2, 4
    hardness = 3
    id = 56
    name = "Diamond Ore"


class CoalOreBlock(Block):
    top_texture = 0, 4
    bottom_texture = 0, 4
    side_texture = 0, 4
    hardness = 3
    id = 16
    name = "Coal Ore"


class BrickBlock(Block):
    top_texture = 2, 0
    bottom_texture = 2, 0
    side_texture = 2, 0
    hardness = 2
    id = 45
    name = "Bricks"


class LampBlock(Block):
    top_texture = 3, 1
    bottom_texture = 3, 1
    side_texture = 3, 1
    hardness = 0.3
    amount_label_color = 0, 0, 0, 255
    id = 124
    name = "Lamp"

class GlassBlock(Block):
    top_texture = 0, 5
    bottom_texture = 0, 5
    side_texture = 0, 5
    transparent = True
    hardness = 0.2
    amount_label_color = 0, 0, 0, 255
    id = 20
    name = "Glass"

class GravelBlock(Block):
    top_texture = 1, 5
    bottom_texture = 1, 5
    side_texture = 1, 5
    hardness = 0.4
    amount_label_color = 0, 0, 0, 255
    id = 13
    name = "Gravel"


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

    def play_break_sound(self):
        sounds.water_break.play()


class ChestBlock(Block):
    top_texture = 1, 2
    bottom_texture = 1, 2
    side_texture = 1, 2
    hardness = 2.5
    id = 54
    name = "Chest"


class SandstoneBlock(Block):
    top_texture = 2, 2
    bottom_texture = 2, 2
    side_texture = 2, 2
    amount_label_color = 0, 0, 0, 255
    hardness = 0.8
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
    hardness = 1.5
    id = 98
    name = "Stone Bricks"


class WoodBlock(Block):
    break_sound = sounds.wood_break


class OakWoodPlankBlock(WoodBlock):
    top_texture = 3, 3
    bottom_texture = 3, 3
    side_texture = 3, 3
    hardness = 2
    id = 5.0
    name = "Oak Wood Planks"

    def play_break_sound(self):
        sounds.wood_break.play()


class SpruceWoodPlankBlock(WoodBlock):
    top_texture = 1, 3
    bottom_texture = 1, 3
    side_texture = 1, 3
    hardness = 2
    id = 5.1
    name = "Spruce Wood Planks"

    def play_break_sound(self):
        sounds.wood_break.play()


class JungleWoodPlankBlock(WoodBlock):
    top_texture = 2, 3
    bottom_texture = 2, 3
    side_texture = 2, 3
    hardness = 2
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
    id = 80

    def __init__(self):
        super(SnowGrassBlock, self).__init__()
        self.drop_id = DirtBlock.id


class OakWoodBlock(WoodBlock):
    top_texture = 7, 1
    bottom_texture = 7, 1
    side_texture = 7, 0
    hardness = 2
    id = 17.0
    name = "Oak wood"

    def play_break_sound(self):
        sounds.wood_break.play()


class OakBranchBlock(Block):
    top_texture = 7, 0
    bottom_texture = 7, 0
    side_texture = 7, 0
    hardness = 2
    id = 17.1
    name = "Oak wood"

    def __init__(self):
        super(OakBranchBlock, self).__init__()
        self.drop_id = OakWoodBlock.id

    def play_break_sound(self):
        sounds.wood_break.play()


class JungleWoodBlock(Block):
    top_texture = 6, 1
    bottom_texture = 6, 1
    side_texture = 6, 0
    hardness = 2
    id = 17.1
    name = "Jungle wood"

    def play_break_sound(self):
        sounds.wood_break.play()


class BirchWoodBlock(Block):
    top_texture = 5, 1
    bottom_texture = 5, 1
    side_texture = 5, 0
    hardness = 2
    id = 17.2
    name = "Birch wood"

    def play_break_sound(self):
        sounds.wood_break.play()


class CactusBlock(Block):
    top_texture = 7, 5
    bottom_texture = 7, 3
    side_texture = 7, 4
    width = 0.8
    hardness = 2
    id = 81
    name = "Cactus"

class TallCactusBlock(Block):
    top_texture = 7, 5
    bottom_texture = 7, 3
    side_texture = 7, 4
    width = 0.3
    hardness = 1
    id = 81.1 # not a real MC block, so the last possible # i think.
    name = "Thin Cactus"

class LeafBlock(Block):
    def __init__(self):
        super(LeafBlock, self).__init__()
        self.drop_id = None

    def play_break_sound(self):
        sounds.leaves_break.play()


class OakLeafBlock(LeafBlock):
    top_texture = 7, 2
    bottom_texture = 7, 2
    side_texture = 7, 2
    hardness = 0.2
    id = 18.0
    name = "Oak Leaves"


class JungleLeafBlock(LeafBlock):
    top_texture = 6, 2
    bottom_texture = 6, 2
    side_texture = 6, 2
    hardness = 0.2
    id = 18.1
    name = "Jungle Leaves"


class BirchLeafBlock(LeafBlock):
    top_texture = 5, 2
    bottom_texture = 5, 2
    side_texture = 5, 2
    hardness = 0.2
    id = 18.2
    name = "Birch Leaves"

    def __init__(self):
        super(BirchLeafBlock, self).__init__()
        self.drop_id = None


class MelonBlock(Block):
    top_texture = 4, 3
    bottom_texture = 4, 3
    side_texture = 4, 2
    hardness = 1
    width = 0.8
    id = 103
    name = "Melon"

class PumpkinBlock(Block):
    top_texture = 2, 5
    bottom_texture = 2, 5
    side_texture = 3, 5
    hardness = 1
    width = 0.8
    id = 86
    name = "Pumpkin"

class TorchBlock(Block):
    top_texture = 5,5
    bottom_texture = 0, 1
    side_texture = 4, 5
    hardness = 1
    width = 0.2
    id = 50
    name = "Torch"

class YFlowersBlock(Block):
    top_texture = 6, 6
    bottom_texture = 0, 1
    side_texture = 6, 5
    hardness = 0.1
    transparent = True
    width = 0.5
    id = 37
    name = "Dandelion"


class StoneSlabBlock(Block):
    top_texture = 4, 4
    bottom_texture = 4, 4
    side_texture = 4, 4
    hardness = 2
    id = 43
    name = "Full Stone Slab"


class ClayBlock(Block):
    top_texture = 6, 4
    bottom_texture = 6, 4
    side_texture = 6, 4
    hardness = 0.6
    id = 82
    name = "Clay Block"


class CobbleBlock(Block):
    top_texture = 6, 3
    bottom_texture = 6, 3
    side_texture = 6, 3
    hardness = 2
    id = 4
    name = "Cobblestone"


class BookshelfBlock(Block):
    top_texture = 1, 2
    bottom_texture = 0, 2
    side_texture = 5, 4
    hardness = 1.5
    id = 47
    name = "Bookshelf"


class FurnaceBlock(Block):
    top_texture = 7, 7
    bottom_texture = 6, 3
    side_texture = 7, 6
    hardness = 3.5
    id = 61
    name = "Furnace"


class FarmBlock(Block):
    top_texture = 5, 3
    bottom_texture = 0, 1
    side_texture = 0, 1
    hardness = 0.5
    id = 60
    name = "Farm Dirt"

    def __init__(self):
        super(FarmBlock, self).__init__()
        self.drop_id = DirtBlock.id

## These two branches currently not used, so that OAK is a 'bigger tree'

#class JungleBranchBlock(Block):
    #top_texture = 6, 0
    #bottom_texture = 6, 0
    #side_texture = 6, 0
    #hardness = 1
    #id = 17.1
    #name = "Jungle wood"

    #def __init__(self):
        #super(JungleBranchBlock, self).__init__()
        #self.drop_id = JungleWoodBlock.id

#class BirchBranchBlock(Block):
    #top_texture = 5, 0
    #bottom_texture = 5, 0
    #side_texture = 5, 0
    #hardness = 1
    #id = 17.2
    #name = "Birch wood"

    #def __init__(self):
        #super(BirchBranchBlock, self).__init__()
        #self.drop_id = BirchWoodBlock.id

CRACK_LEVEL = 6

# not a real block, used to store crack texture data
class CrackTextureBlock(object):
    def __init__(self):
        self.crack_level = CRACK_LEVEL
        self.texture_data = []
        for i in range(self.crack_level):
            texture_coords = get_texture_coordinates(i, 7)
            tmp = []
            tmp.extend(texture_coords * 6)
            self.texture_data.append(tmp)

crack_textures = CrackTextureBlock()

air_block = AirBlock()
grass_block = GrassBlock()
sand_block = SandBlock()
brick_block = BrickBlock()
stone_block = StoneBlock()
dirt_block = DirtBlock()
lamp_block = LampBlock()
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
oakbranch_block = OakBranchBlock()
junglewood_block = JungleWoodBlock()
jungleleaf_block = JungleLeafBlock()
birchwood_block = BirchWoodBlock()
birchleaf_block = BirchLeafBlock()
cactus_block = CactusBlock()
coalore_block = CoalOreBlock()
ironore_block = IronOreBlock()
goldore_block = GoldOreBlock()
diamondore_block = DiamondOreBlock()
melon_block = MelonBlock()
stoneslab_block = StoneSlabBlock()
clay_block = ClayBlock()
cobble_block = CobbleBlock()
bookshelf_block = BookshelfBlock()
furnace_block = FurnaceBlock()
farm_block = FarmBlock()
glass_block = GlassBlock()
gravel_block = GravelBlock()
tallcactus_block = TallCactusBlock()
pumpkin_block = PumpkinBlock()
torch_block = TorchBlock()
yflowers_block = YFlowersBlock()




