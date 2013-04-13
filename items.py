# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
from blocks import *
import globals as G


# From MinecraftWiki
# Items are objects which do not exist outside of the player's inventory and hands
# i.e., they cannot be placed in the game world.
# Some items simply place blocks or entities into the game world when used.
# Type
# * Materials: iron ingot, gold ingot, etc.
# * Food: found or crafted by the player and eaten to regain hunger points
# * Potions
# * Tools
# * Informative items: map, compass and clock
# * Weapons
# * Armor


class Item(object):
    id = None
    max_stack_size = 0
    amount_label_color = 255, 255, 255, 255
    name = "Item"
    group = None

    # How long can this item burn (-1 for non-fuel items)
    burning_time = -1
    # How long does it take to smelt this item (-1 for unsmeltable items)
    smelting_time = -1

    def __init__(self):
        self.id = BlockID(self.id)
        G.ITEMS_DIR[self.id] = self

    def on_right_click(self):
        pass

class ItemStack(object):
    def __init__(self, type = 0, amount = 1, durability = 0, data = 0):
        if amount < 1:
            amount = 1
        self.type = BlockID(type, durability)
        self.amount = amount
        self.durability = durability
        self.data = data
        if type >= G.ITEM_ID_MIN:
            self.max_stack_size = G.ITEMS_DIR[type].max_stack_size
        else:
            self.max_stack_size = G.BLOCKS_DIR[type].max_stack_size

    # for debugging
    def __repr__(self):
        return '{ Item stack with type = ' + str(self.type) + ' }'

    def change_amount(self, change=0):
        overflow = 0
        if change != 0:
            self.amount += change
            if self.amount < 0:
                self.amount = 0
            elif self.amount > self.max_stack_size:
                overflow = self.amount - self.max_stack_size
                self.amount -= overflow

        return overflow

    # compatible with blocks
    @property
    def id(self):
        return self.type

    # compatible with blocks
    @property
    def name(self):
        return self.get_object().name

    def get_object(self):
        if self.id >= G.ITEM_ID_MIN:
            return G.ITEMS_DIR[self.id]
        else:
            return G.BLOCKS_DIR[self.id]

class CoalItem(Item):
    id = 263
    max_stack_size = 64
    name = "Coal"
    burning_time = 80

class LadderItem(Item):
    id = 999
    max_stack_size = 64
    name = "Ladder"

class DiamondItem(Item):
    id = 264
    max_stack_size = 64
    name = "Diamond"

class IronIngotItem(Item):
    id = 265
    max_stack_size = 64
    name = "Iron Ingot"

class GoldIngotItem(Item):
    id = 266
    max_stack_size = 64
    name = "Gold Ingot"

class StickItem(Item):
    id = 280
    max_stack_size = 64
    name = "Stick"

class FlintItem(Item):
    id = 318
    max_stack_size = 64
    name = "Flint"

class YellowDyeItem(Item):
    id = 351
    max_stack_size = 64
    name = "Dandelion Yellow Dye"

class CactusGreenDyeItem(Item):
    id = 351,2
    max_stack_size = 64
    name = "Cactus Green Dye"

class RedDyeItem(Item):
    id = 351,1
    max_stack_size = 64
    name = "Red Dye"

class SugarItem(Item):
    id = 353
    max_stack_size = 64
    name = "Sugar"

class PaperItem(Item):
    id = 339
    max_stack_size = 64
    name = "Cactus Green Dye"

class Tool(Item):
    material = None
    multiplier = 0
    tool_type = None

    def __init__(self):
        super(Tool, self).__init__()
        self.multiplier = 2 * (self.material + 1)

class WoodAxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 271
    name = "Wooden Axe"

class StoneAxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 275
    name = "Stone Axe"

class IronAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258
    name = "Iron Axe"

class EmeraldAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,1
    name = "Emerald Axe"

class RubyAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,2
    name = "Ruby Axe"

class SapphireAxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 258,3
    name = "Sapphire Axe"

class DiamondAxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 279
    name = "Diamond Axe"

class GoldenAxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.AXE
    max_stack_size = 1
    id = 286
    name = "Golden Axe"

class WoodPickaxe(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 270
    name = "Wooden Pickaxe"

class StonePickaxe(Tool):
    material = G.STONE_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 274
    name = "Stone Pickaxe"

class IronPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257
    name = "Iron Pickaxe"

class EmeraldPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,1
    name = "Emerald Pickaxe"

class RubyPickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,2
    name = "Ruby Pickaxe"

class SapphirePickaxe(Tool):
    material = G.IRON_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 257,3
    name = "Sapphire Pickaxe"

class DiamondPickaxe(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 278
    name = "Diamond Pickaxe"

class GoldenPickaxe(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.PICKAXE
    max_stack_size = 1
    id = 285
    name = "Golden Pickaxe"

class WoodShovel(Tool):
    material = G.WOODEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 269
    name = "Wooden Shovel"

class StoneShovel(Tool):
    material = G.STONE_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 273
    name = "Stone Shovel"

class IronShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256
    name = "Iron Shovel"

class EmeraldShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,1
    name = "Emerald Shovel"

class RubyShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,2
    name = "Ruby Shovel"

class SapphireShovel(Tool):
    material = G.IRON_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 256,3
    name = "Sapphire Shovel"

class DiamondShovel(Tool):
    material = G.DIAMOND_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 277
    name = "Diamond Shovel"

class GoldenShovel(Tool):
    material = G.GOLDEN_TOOL
    tool_type = G.SHOVEL
    max_stack_size = 1
    id = 284
    name = "Golden Shovel"

class Armor(Item):
    material = None
    defense_point = 0
    armor_type = None
    max_stack_size = 1

    def __init__(self):
        super(Armor, self).__init__()

class IronHelmet(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.HELMET
    id = 306
    name = "Iron Helmet"

class IronChestplate(Armor):
    material = G.IRON_TOOL
    defense_point = 3
    armor_type = G.CHESTPLATE
    id = 307
    name = "Iron Chestplate"

class IronLeggings(Armor):
    material = G.IRON_TOOL
    defense_point = 2.5
    armor_type = G.LEGGINGS
    id = 308
    name = "Iron Leggings"

class IronBoots(Armor):
    material = G.IRON_TOOL
    defense_point = 1
    armor_type = G.BOOTS
    id = 309
    name = "Iron Boots"

##Emerald Armor .. Pretty much re-textured Iron armor (from Tekkit)

#class EmeraldHelmet(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.HELMET
    #id = 306.1
    #name = "Emerald Helmet"

#class EmeraldChestplate(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 3
    #armor_type = globals.CHESTPLATE
    #id = 307.1
    #name = "Emerald Chestplate"

#class EmeraldLeggings(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 2.5
    #armor_type = globals.LEGGINGS
    #id = 308.1
    #name = "Emerald Leggings"

#class EmeraldBoots(Armor):
    #material = globals.IRON_TOOL
    #defense_point = 1
    #armor_type = globals.BOOTS
    #id = 309.1
    #name = "Emerald Boots"

coal_item = CoalItem()
diamond_item = DiamondItem()
stick_item = StickItem()
iron_ingot_item = IronIngotItem()
gold_ingot_item = GoldIngotItem()
flint_item = FlintItem()
wood_axe = WoodAxe()
stone_axe = StoneAxe()
iron_axe = IronAxe()
diamond_axe = DiamondAxe()
golden_axe = GoldenAxe()
emerald_axe = EmeraldAxe()
wood_pickaxe = WoodPickaxe()
stone_pickaxe = StonePickaxe()
iron_pickaxe = IronPickaxe()
diamond_pickaxe = DiamondPickaxe()
golden_pickaxe = GoldenPickaxe()
emerald_pickaxe = EmeraldPickaxe()
wood_shovel = WoodShovel()
stone_shovel = StoneShovel()
iron_shovel = IronShovel()
diamond_shovel = DiamondShovel()
golden_shovel = GoldenShovel()
emerald_shovel = EmeraldShovel()
iron_helmet = IronHelmet()
iron_chestplate = IronChestplate()
iron_leggings = IronLeggings()
iron_boots = IronBoots()
#emerald_helmet = EmeraldHelmet()
#emerald_chestplace = EmeraldChestplate()
#emerald_leggings = EmeraldLeggings()
#emerald_boots = EmeraldBoots()
yellowdye_item = YellowDyeItem()
ladder_item = LadderItem()
ruby_pickaxe = RubyPickaxe()
ruby_shovel = RubyShovel()
ruby_axe = RubyAxe()
sapphire_pickaxe = SapphirePickaxe()
sapphire_shovel = SapphireShovel()
sapphire_axe = SapphireAxe()
ladder_item = LadderItem()
reddye_item = RedDyeItem()
sugar_item = SugarItem()
paper_item = PaperItem()
