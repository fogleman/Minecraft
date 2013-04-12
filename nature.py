import random
from blocks import *


class Trunk(object):
    block = None
    height_range = 4, 8

    def __init__(self, position, block=None, height_range=None):
        if block is not None:
            self.block = block
        if height_range is not None:
            self.height_range = height_range

        x, y, z = position

        self.height = random.randint(*self.height_range)
        self.blocks = {}
        for dy in range(1, self.height):
            self.blocks[(x, y + dy, z)] = self.block


class Tree(object):
    trunk_block = None
    leaf_block = None
    trunk_height_range = 4, 8
    grows_on = grass_block, dirt_block, snowgrass_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

        x, y, z = position
        height = trunk.height
        treetop = y + height

        # Leaves generation
        d = height / 3 + 1
        for xl in range(x - d, x + d):
            dx = abs(xl - x)
            for yl in range(treetop - d, treetop + d):
                for zl in range(z - d, z + d):
                    # Don't replace existing blocks
                    if (xl, yl, zl) in world:
                        continue
                    # Avoids orphaned leaves
                    if not world.has_neighbors((xl, yl, zl),
                                               (cls.trunk_block,
                                                cls.leaf_block)):
                        continue
                    dz = abs(zl - z)
                    # The farther we are (horizontally) from the trunk,
                    # the least leaves we can find.
                    if random.uniform(0, dx + dz) > 0.6:
                        continue
                    world.init_block((xl, yl, zl), cls.leaf_block)


class OakTree(Tree):
    trunk_block = oakwood_block
    leaf_block = oakleaf_block


class JungleTree(Tree):
    trunk_block = junglewood_block
    leaf_block = jungleleaf_block
    trunk_height_range = 8, 12


class BirchTree(Tree):
    trunk_block = birchwood_block
    leaf_block = birchleaf_block
    trunk_height_range = 5, 7



class Cactus(object):
    trunk_block = cactus_block
    trunk_height_range = 1, 4
    grows_on = sand_block, sandstone_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class TallCactus(object):
    trunk_block = tallcactus_block
    trunk_height_range = 1, 10
    grows_on = sand_block, sandstone_block, grass_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class WaterMelon(object):
    trunk_block = melon_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block, snowgrass_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class Pumpkin(object):
    trunk_block = pumpkin_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block, snowgrass_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class YFlowers(object):
    trunk_block = yflowers_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class Potato(object):
    trunk_block = potato_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class Carrot(object):
    trunk_block = carrot_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class Reed(object):
    trunk_block = yflowers_block
    trunk_height_range = 1, 2
    grows_on = sand_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

class Rose(object):
    trunk_block = rose_block
    trunk_height_range = 1, 2
    grows_on = grass_block, dirt_block

    @classmethod
    def add_to_world(cls, world, position):
        trunk = Trunk(position, block=cls.trunk_block,
                      height_range=cls.trunk_height_range)

        for item in trunk.blocks.items():
            world.init_block(*item)

TREES = (
    OakTree,
    JungleTree,
    BirchTree,
    Cactus,  # FIXME: A cactus isn't really a tree.
    TallCactus,
    WaterMelon,
    Pumpkin,
    YFlowers,
    Potato,
    Carrot,
    Reed,
    Rose,
)

TREE_BLOCKS = tuple(tree.trunk_block for tree in TREES)
