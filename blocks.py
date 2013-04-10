# coding: utf-8

from __future__ import unicode_literals
from globals import *
import sounds


def get_texture_coordinates(x, y, tileset_size=TILESET_SIZE):
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

    id_main = None  # Whole number component of id
    id_sub = None  # Decimal component of id

    width = 1.0
    height = 1.0

    # Texture coordinates from the tileset.
    top_texture = ()
    bottom_texture = ()
    side_texture = ()

    # Sounds
    break_sound = sounds.wood_break

    # Physical attributes
    hardness = 0.0  # hardness can be found on http://www.minecraftwiki.net/wiki/Digging#Blocks_by_hardness
    density = 1
    transparent = False
    regenerated_health = 0

    # Inventory attributes
    max_stack_size = 64
    amount_label_color = 255, 255, 255, 255
    name = "Block"

    digging_tool = -1

    def __init__(self, width=None, height=None):
        self.drop_id = self.id
        if self.id is not None:
            self.id_main = int(self.id)
            self.id_sub = int(str(self.id % 1)[2:] or 0)

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

    def __str__(self):
        return self.name

    def get_texture_data(self):
        return list(self.top_texture + self.bottom_texture
                    + self.side_texture * 4)

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

    def play_break_sound(self, player=None, position=None):
        if self.break_sound is not None:
            sounds.play_sound(self.break_sound, player=player, position=position)


class AirBlock(Block):
    top_texture = -1, -1
    bottom_texture = -1, -1
    side_texture = -1, -1
    max_stack_size = 0
    density = 0
    id = 0
    name = "Air"


class WoodBlock(Block):
    break_sound = sounds.wood_break
    digging_tool = AXE


class HardBlock(Block):
    break_sound = sounds.stone_break

class StoneBlock(HardBlock):
    top_texture = 2, 1
    bottom_texture = 2, 1
    side_texture = 2, 1
    hardness = 1.5
    id = 1
    name = "Stone"
    digging_tool = PICKAXE

    def __init__(self):
        super(StoneBlock, self).__init__()
        self.drop_id = CobbleBlock.id


class GrassBlock(Block):
    top_texture = 1, 0
    bottom_texture = 0, 1
    side_texture = 0, 0
    hardness = 0.6
    id = 2
    break_sound = sounds.dirt_break
    name = 'Grass'
    digging_tool = SHOVEL

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
    digging_tool = SHOVEL
    break_sound = sounds.dirt_break

class SnowBlock(Block):
    top_texture = 4, 1
    bottom_texture = 4, 1
    side_texture = 4, 1
    hardness = 0.5
    id = 80
    name = "Snow"
    amount_label_color = 0, 0, 0, 255
    break_sound = sounds.dirt_break

class SandBlock(Block):
    top_texture = 1, 1
    bottom_texture = 1, 1
    side_texture = 1, 1
    hardness = 0.5
    amount_label_color = 0, 0, 0, 255
    id = 12
    name = "Sand"
    digging_tool = SHOVEL
    break_sound = sounds.sand_break


class GoldOreBlock(HardBlock):
    top_texture = 3, 4
    bottom_texture = 3, 4
    side_texture = 3, 4
    hardness = 3
    id = 14
    digging_tool = PICKAXE
    name = "Gold Ore"


class IronOreBlock(HardBlock):
    top_texture = 1, 4
    bottom_texture = 1, 4
    side_texture = 1, 4
    hardness = 3
    id = 15
    digging_tool = PICKAXE
    name = "Iron Ore"


class DiamondOreBlock(HardBlock):
    top_texture = 2, 4
    bottom_texture = 2, 4
    side_texture = 2, 4
    hardness = 3
    id = 56
    digging_tool = PICKAXE
    def __init__(self):
        super(DiamondOreBlock, self).__init__()
        self.drop_id = 264
    name = "Diamond Ore"


class CoalOreBlock(HardBlock):
    top_texture = 0, 4
    bottom_texture = 0, 4
    side_texture = 0, 4
    hardness = 3
    id = 16
    digging_tool = PICKAXE
    def __init__(self):
        super(CoalOreBlock, self).__init__()
        self.drop_id = 263
    name = "Coal Ore"


class BrickBlock(HardBlock):
    top_texture = 2, 0
    bottom_texture = 2, 0
    side_texture = 2, 0
    hardness = 2
    id = 45
    digging_tool = PICKAXE
    name = "Bricks"


class LampBlock(Block):
    top_texture = 3, 1
    bottom_texture = 3, 1
    side_texture = 3, 1
    hardness = 0.3
    amount_label_color = 0, 0, 0, 255
    id = 124
    name = "Lamp"
    break_sound = sounds.glass_break


class GlassBlock(Block):
    top_texture = 0, 5
    bottom_texture = 0, 5
    side_texture = 0, 5
    transparent = True
    hardness = 0.2
    amount_label_color = 0, 0, 0, 255
    id = 20
    name = "Glass"
    break_sound = sounds.glass_break


class GravelBlock(Block):
    top_texture = 1, 5
    bottom_texture = 1, 5
    side_texture = 1, 5
    hardness = 0.4
    amount_label_color = 0, 0, 0, 255
    id = 13
    name = "Gravel"
    digging_tool = SHOVEL
    break_sound = sounds.gravel_break


class BedrockBlock(HardBlock):
    top_texture = 3, 0
    bottom_texture = 3, 0
    side_texture = 3, 0
    hardness = -1  # Unbreakable
    id = 7
    name = "Bedrock"


class WaterBlock(Block):
    top_texture = 0, 2
    bottom_texture = 6, 7
    side_texture = 6, 7
    transparent = True
    hardness = -1  # Unobtainable
    density = 0.5
    id = 8
    name = "Water"
    break_sound = sounds.water_break


class CraftTableBlock(WoodBlock):
    top_texture = 8, 1
    bottom_texture = 1, 1
    side_texture = 8, 0
    hardness = 2.5
    id = 58
    name = "Crafting Table"

class MetaBlock(WoodBlock): # this is a experimental block.
    top_texture = 9, 0
    bottom_texture = 9, 0
    side_texture = 9, 0
    hardness = 2.5
    id = 0.1
    name = "Action"


class SandstoneBlock(HardBlock):
    top_texture = 2, 2
    bottom_texture = 2, 2
    side_texture = 2, 2
    amount_label_color = 0, 0, 0, 255
    hardness = 0.8
    id = 24
    name = "Sandstone"


# Changed Marble to Quartz -- It seems that Quartz is MC's answer to Tekkit's MArble.
class QuartzBlock(HardBlock):
    top_texture = 3, 2
    bottom_texture = 9, 4
    side_texture = 3, 2
    id = 155.0
    hardness = 2
    name = "Quartz"
    amount_label_color = 0, 0, 0, 255
    digging_tool = PICKAXE


class StonebrickBlock(HardBlock):
    top_texture = 0, 3
    bottom_texture = 0, 3
    side_texture = 0, 3
    hardness = 1.5
    id = 98
    name = "Stone Bricks"


class OakWoodPlankBlock(WoodBlock):
    top_texture = 3, 3
    bottom_texture = 3, 3
    side_texture = 3, 3
    hardness = 2
    id = 5.0
    name = "Oak Wood Planks"


class SpruceWoodPlankBlock(WoodBlock):
    top_texture = 1, 3
    bottom_texture = 1, 3
    side_texture = 1, 3
    hardness = 2
    id = 5.1
    name = "Spruce Wood Planks"


class JungleWoodPlankBlock(WoodBlock):
    top_texture = 2, 3
    bottom_texture = 2, 3
    side_texture = 2, 3
    hardness = 2
    id = 5.3
    name = "Jungle Wood Planks"


# FIXME: Can't find its specific id on minecraftwiki.
# from ronmurphy: This is just the snowy side grass from the above texture pack.  MC has one like this also.
class SnowGrassBlock(Block):
    top_texture = 4, 1
    bottom_texture = 0, 1
    side_texture = 4, 0
    hardness = 0.6
    id = 80
    break_sound = sounds.dirt_break

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


class OakBranchBlock(WoodBlock):
    top_texture = 7, 0
    bottom_texture = 7, 0
    side_texture = 7, 0
    hardness = 2
    id = 17.1
    name = "Oak wood"

    def __init__(self):
        super(OakBranchBlock, self).__init__()
        self.drop_id = OakWoodBlock.id


class JungleWoodBlock(WoodBlock):
    top_texture = 6, 1
    bottom_texture = 6, 1
    side_texture = 6, 0
    hardness = 2
    id = 17.1
    name = "Jungle wood"


class BirchWoodBlock(WoodBlock):
    top_texture = 5, 1
    bottom_texture = 5, 1
    side_texture = 5, 0
    hardness = 2
    id = 17.2
    amount_label_color = 0, 0, 0, 255
    name = "Birch wood"


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
    transparent = True
    width = 0.3
    hardness = 1
    id = 81.1  # not a real MC block, so the last possible # i think.
    name = "Thin Cactus"


class LeafBlock(Block):
    break_sound = sounds.leaves_break

    def __init__(self):
        super(LeafBlock, self).__init__()
        self.drop_id = None


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
    transparent = True
    hardness = 1
    width = 0.8
    id = 103
    name = "Melon"
    regenerated_health = 3
    break_sound = sounds.melon_break


class PumpkinBlock(Block):
    top_texture = 2, 5
    bottom_texture = 2, 5
    side_texture = 3, 5
    transparent = True
    hardness = 1
    width = 0.8
    id = 86
    name = "Pumpkin"
    break_sound = sounds.melon_break


class TorchBlock(WoodBlock):
    top_texture = 5, 5
    bottom_texture = 0, 1
    side_texture = 4, 5
    hardness = 1
    width = 0.2
    id = 50
    name = "Torch"


class YFlowersBlock(Block):
    top_texture = 6, 6
    bottom_texture = 1, 0
    side_texture = 6, 5
    hardness = 0.1
    transparent = True
    width = 0.5
    id = 37
    name = "Dandelion"
    break_sound = sounds.leaves_break


class StoneSlabBlock(HardBlock):
    top_texture = 4, 4
    bottom_texture = 4, 4
    side_texture = 4, 4
    hardness = 2
    id = 43
    name = "Full Stone Slab"


class ClayBlock(HardBlock):
    top_texture = 6, 4
    bottom_texture = 6, 4
    side_texture = 6, 4
    hardness = 0.6
    id = 82
    name = "Clay Block"


class CobbleBlock(HardBlock):
    top_texture = 6, 3
    bottom_texture = 6, 3
    side_texture = 6, 3
    hardness = 2
    id = 4
    name = "Cobblestone"


class CobbleFenceBlock(HardBlock):
    top_texture = 6, 3
    bottom_texture = 6, 3
    side_texture = 6, 3
    transparent = True
    hardness = 2
    width = 0.6
    id = 4.1
    name = "Cobblestone Fence Post"


class BookshelfBlock(WoodBlock):
    top_texture = 1, 2
    bottom_texture = 0, 2
    side_texture = 5, 4
    hardness = 1.5
    id = 47
    name = "Bookshelf"


class FurnaceBlock(HardBlock):
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
    break_sound = sounds.dirt_break

    def __init__(self):
        super(FarmBlock, self).__init__()
        self.drop_id = DirtBlock.id

class ChestBlock(Block):
    top_texture = 8, 4
    bottom_texture = 8, 2
    side_texture = 8, 3
    hardness = 2
    id = 54
    name = "Chest"


class CactusBlock(Block):
    top_texture = 7, 5
    bottom_texture = 7, 3
    side_texture = 7, 4
    transparent = True
    width = 0.8
    hardness = 2
    id = 81
    name = "Cactus"

# Wool blocks

class BlackWoolBlock(Block):
    top_texture = 15, 0
    bottom_texture = 15, 0
    side_texture = 15, 0
    hardness = 1
    id =35.15
    name = "Black Wool"

class RedWoolBlock(Block):
    top_texture = 15, 1
    bottom_texture = 15, 1
    side_texture = 15, 1
    hardness = 1
    id =35.14
    name = "Red Wool"

class GreenWoolBlock(Block):
    top_texture = 15, 2
    bottom_texture = 15, 2
    side_texture = 15, 2
    hardness = 1
    id =35.13
    name = "Green Wool"

class BrownWoolBlock(Block):
    top_texture = 15, 3
    bottom_texture = 15, 3
    side_texture = 15, 3
    hardness = 1
    id =35.12
    name = "Brown Wool"

class BlueWoolBlock(Block):
    top_texture = 15, 4
    bottom_texture = 15, 4
    side_texture = 15, 4
    hardness = 1
    id =35.11
    name = "Blue Wool"

class PurpleWoolBlock(Block):
    top_texture = 15, 5
    bottom_texture = 15, 5
    side_texture = 15, 5
    hardness = 1
    id =35.10
    name = "Purple Wool"

class CyanWoolBlock(Block):
    top_texture = 15, 6
    bottom_texture = 15, 6
    side_texture = 15, 6
    hardness = 1
    id =35.9
    name = "Cyan Wool"

class LightGreyWoolBlock(Block):
    top_texture = 15, 7
    bottom_texture = 15, 7
    side_texture = 15, 7
    hardness = 1
    id =35.8
    name = "Light Grey Wool"

class GreyWoolBlock(Block):
    top_texture = 15, 8
    bottom_texture = 15, 8
    side_texture = 15, 8
    hardness = 1
    id =35.7
    name = "Grey Wool"

class PinkWoolBlock(Block):
    top_texture = 15, 9
    bottom_texture = 15, 9
    side_texture = 15, 9
    hardness = 1
    id =35.6
    name = "Pink Wool"

class LimeWoolBlock(Block):
    top_texture = 15, 10
    bottom_texture = 15, 10
    side_texture = 15, 10
    width = 0.8
    hardness = 1
    id =35.5
    name = "Lime Wool"

class YellowWoolBlock(Block):
    top_texture = 15, 11
    bottom_texture = 15, 11
    side_texture = 15, 11
    hardness = 1
    id =35.4
    name = "Yellow Wool"

class LightBlueWoolBlock(Block):
    top_texture = 15, 12
    bottom_texture = 15, 12
    side_texture = 15, 12
    hardness = 1
    id =35.3
    name = "Light Blue Wool"

class MagentaWoolBlock(Block):
    top_texture = 15, 13
    bottom_texture = 15, 13
    side_texture = 15, 13
    hardness = 1
    id =35.2
    name = "Magenta Wool"

class OrangeWoolBlock(Block):
    top_texture = 15, 14
    bottom_texture = 15, 14
    side_texture = 15, 14
    hardness = 1
    id =35.1
    name = "Orange Wool"

class WhiteWoolBlock(Block):
    top_texture = 15, 15
    bottom_texture = 15, 15
    side_texture = 15, 15
    hardness = 1
    id =35.0
    name = "White Wool"
amount_label_color = 0, 0, 0, 255

# moreplants
class RoseBlock(Block):
    top_texture = 0, -15
    bottom_texture = 10, 0
    side_texture = 10, 0
    hardness = .08
    id =38
    name = "Rose"
amount_label_color = 0, 0, 0, 255

class ReedBlock(Block):
    top_texture = 0, -15
    bottom_texture = 10, 1
    side_texture = 10, 1
    hardness = 0.8
    transparent = True
    id =83
    name = "Reed"
    max_stack_size = 16
    amount_label_color = 0, 0, 0, 255
    def __init__(self):
        super(ReedBlock, self).__init__()
        self.drop_id = 338

class PotatoBlock(Block):
    top_texture = 0, -15
    bottom_texture = 10, 3
    side_texture = 10, 3
    hardness = 0.8
    transparent = True
    id =142
    name = "Potato"
    max_stack_size = 16
    amount_label_color = 0, 0, 0, 255
    def __init__(self):
        super(PotatoBlock, self).__init__()
        self.drop_id = 392

class CarrotBlock(Block):
    top_texture = 0, -15
    bottom_texture = 10, 2
    side_texture = 10, 2
    hardness = 0.8
    transparent = True
    id =141
    name = "Carrot"
    max_stack_size = 16
    amount_label_color = 0, 0, 0, 255
    def __init__(self):
        super(CarrotBlock, self).__init__()
        self.drop_id = 391

class DiamondBlock(HardBlock):
    top_texture = 11, 0
    bottom_texture = 11, 0
    side_texture = 11, 0
    hardness = 5
    id = 57
    digging_tool = PICKAXE
    name = "Diamond Block"

class GoldBlock(HardBlock):
    top_texture = 11, 1
    bottom_texture = 11, 1
    side_texture = 11, 1
    hardness = 4
    id = 41
    digging_tool = PICKAXE
    name = "Gold Block"

class IronBlock(HardBlock):
    top_texture = 11, 2
    bottom_texture = 11, 2
    side_texture = 11, 2
    hardness = 4
    id = 42
    digging_tool = PICKAXE
    name = "Iron Block"

class StonebrickBlock(HardBlock):
    top_texture = 0, 3
    bottom_texture = 0, 3
    side_texture = 0, 3
    hardness = 1.5
    id = 98.0
    name = "Stone Bricks"

class CrackedStonebrickBlock(HardBlock):
    top_texture = 9, 2
    bottom_texture = 9, 2
    side_texture = 9, 2
    hardness = 1.5
    id = 98.1
    name = "Cracked Stone Bricks"

class MossyStonebrickBlock(HardBlock):
    top_texture = 9, 1
    bottom_texture = 9, 1
    side_texture = 9, 1
    hardness = 1.5
    id = 98.2
    name = "Mossy Stone Bricks"

# Changed Marble to Quartz -- It seems that Quartz is MC's answer to Tekkit's MArble.
class QuartzBlock(HardBlock):
    top_texture = 3, 2
    bottom_texture = 9, 4
    side_texture = 3, 2
    id = 155.0
    hardness = 2
    name = "Quartz"
    amount_label_color = 0, 0, 0, 255
    digging_tool = PICKAXE

class ColumnQuartzBlock(HardBlock):
    top_texture = 3, 2
    bottom_texture = 9, 4
    side_texture = 9, 5
    id = 155.2
    hardness = 2
    name = "Column Quartz"
    amount_label_color = 0, 0, 0, 255
    digging_tool = PICKAXE

class ChisledQuartzBlock(HardBlock):
    top_texture = 3, 2
    bottom_texture = 9, 4
    side_texture = 9, 6
    id = 155.1
    hardness = 2
    name = "Chisled Quartz"
    amount_label_color = 0, 0, 0, 255
    digging_tool = PICKAXE

class IceBlock(Block):
    top_texture = 8, 7
    bottom_texture = 8, 7
    side_texture = 8, 7
    id = 79
    hardness = 0.5
    transparent = True
    name = "Ice"
    amount_label_color = 0, 0, 0, 255

class MossyStoneBlock(HardBlock):
    top_texture = 9, 3
    bottom_texture = 9, 3
    side_texture = 9, 3
    hardness = 1.5
    id = 48
    name = "Mossy Stone"
    digging_tool = PICKAXE
    max_stack_size = 64

CRACK_LEVELS = 10


# not a real block, used to store crack texture data
class CrackTextureBlock(object):
    def __init__(self):
        self.crack_level = CRACK_LEVELS
        self.texture_data = []
        for i in range(self.crack_level):
            texture_coords = get_texture_coordinates(i, 8)
            self.texture_data.append(texture_coords * 6)

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
craft_block = CraftTableBlock()
sandstone_block = SandstoneBlock()
quartz_block = QuartzBlock()
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
cobblefence_block = CobbleFenceBlock()
snow_block = SnowBlock()
meta_block = MetaBlock()
chest_block = ChestBlock()
# wool
blackwool_block = BlackWoolBlock()
redwool_block = RedWoolBlock()
greenwool_block = GreenWoolBlock()
brownwool_block = BrownWoolBlock()
bluewool_block = BlueWoolBlock()
purplewool_block = PurpleWoolBlock()
cyanwool_block = CyanWoolBlock()
lightgreywool_block = LightGreyWoolBlock()
greywool_block = GreyWoolBlock()
pinkwool_block = PinkWoolBlock()
limewool_block = LimeWoolBlock()
yellowwool_block = YellowWoolBlock()
lightbluewool_block = LightBlueWoolBlock()
magentawool_block = MagentaWoolBlock()
orangewool_block = OrangeWoolBlock()
whitewool_block = WhiteWoolBlock()

rose_block = RoseBlock()
reed_block = ReedBlock()
potato_block = PotatoBlock()
carrot_block = CarrotBlock()
diamond_block = DiamondBlock()
gold_block = GoldBlock()
iron_block = IronBlock()
stonebrickcracked_block = CrackedStonebrickBlock()
stonebrickmossy_block = MossyStonebrickBlock()
quartzcolumn_block = ColumnQuartzBlock()
quartzchisled_block = ChisledQuartzBlock()
ice_block = IceBlock()


