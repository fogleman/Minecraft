import block

class Inventory:
    def __init__(self, *args, **kwargs):
        self.hotbar = [block.PORTAL, block.STONE, block.SPRUCE_WOOD_PLANK, block.BIRCH_WOOD_PLANK, block.JUNGLE_WOOD_PLANK, block.ACACIA_WOOD_PLANK, block.DARK_OAK_WOOD_PLANK]
        self.index = 0