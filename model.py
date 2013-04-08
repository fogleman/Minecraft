from world import *
from nature import *
import globals
from globals import *


class Model(World):
    def __init__(self, initialize=True):
        super(Model, self).__init__()
        if initialize:
            self.initialize()

        # Convert dirt to grass if no block or a transparent one is above.
        for position, block in ((p, b) for p, b in self.items()
                                if b is dirt_block):
            x, y, z = position
            above_position = x, y + 1, z
            if above_position not in self or self[above_position].transparent:
                self[position] = grass_block

    def initialize(self):
        world_size = config.getint('World', 'size')
        world_type = config.getint('World', 'type')
        hill_height = config.getint('World', 'hill_height')
        flat_world = config.getboolean('World', 'flat')
        self.max_trees = config.getint('World', 'max_trees')
        tree_chance = self.max_trees / float(world_size * (SECTOR_SIZE ** 3))
        n = world_size / 2  # 80
        s = 1
        y = 0

        worldtypes_grounds = (
            dirt_block,
            dirt_block,
            (sand_block,) * 15 + (sandstone_block,) * 4,
            (water_block,) * 30 + (clay_block,) * 4,
            dirt_block,
            (dirt_block,) * 15 + (dirt_block,) * 3 + (stone_block,),
            (snowgrass_block,) * 10 + (snow_block,) * 4,
        )

        world_type_trees = (
            (OakTree, BirchTree, WaterMelon, Pumpkin, YFlowers),
            (OakTree, WaterMelon, YFlowers),
            (Cactus, TallCactus,),
            (OakTree, JungleTree, BirchTree, Cactus, TallCactus, WaterMelon, YFlowers),
            (Cactus, BirchTree, TallCactus, YFlowers),
            (OakTree, BirchTree, Pumpkin, YFlowers),
            (OakTree, BirchTree, WaterMelon, YFlowers),
        )

        ore_type_blocks = (
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            gravel_block, gravel_block, gravel_block, gravel_block, gravel_block,
            gravel_block, gravel_block, gravel_block, gravel_block, gravel_block,
            coalore_block, coalore_block, coalore_block, coalore_block, coalore_block,
            ironore_block, ironore_block, ironore_block, ironore_block,
            goldore_block, goldore_block, goldore_block,
            diamondore_block, diamondore_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
        )

        #ore_type_blocks = (
            #(stone_block,) * 50 + (gravel_block,) * 10 + (coalore_block,) * 5 + (ironore_block,) * 4 + (goldore_block,) * 3 + (diamondore_block,) + (stone_block,) * 15,
        #)

        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):

                # Generation of the outside wall
                if x in (-n, n) or z in (-n, n):
                    for dy in xrange(-16, 10):  # was -2 ,6
                        self.init_block((x, y + dy, z), stone_block)
                    continue



                # Generation of the ground

                block = worldtypes_grounds[world_type]

                if isinstance(block, (tuple, list)):
                    block = random.choice(block)
                self.init_block((x, y - 2, z), block)
                for yy in xrange(-16, -2):
                    # ores and filler...
                    oblock = random.choice(ore_type_blocks)
                    self.init_block((x, yy , z), oblock)

                for yy in xrange(-18, -16):
                    self.init_block((x, yy , z), bed_block)

                # Perhaps a tree
                if self.max_trees > 0:
                    showtree = random.random()
                    if showtree <= tree_chance:
                        tree_class = world_type_trees[world_type]
                        if isinstance(tree_class, (tuple, list)):
                            tree_class = random.choice(tree_class)
                        self.generate_tree((x, y - 2, z), tree_class)

        if flat_world:
            return

        o = n - 10 + hill_height - 6

        world_type_blocks = (
            dirt_block,
            (dirt_block, sandstone_block),
            sand_block,
            (dirt_block, sand_block),
            (dirt_block,) * 2 + (sand_block,),
            stone_block,
            snowgrass_block,
        )

        # Hills generation
        # FIXME: This generation in two phases (ground then hills), leads to
        # hills overlaying trees.
        for _ in xrange(world_size / 2 + 40):  # (120):
            a = random.randint(-o, o)
            b = random.randint(-o, o)
            c = -1
            h = random.randint(1, hill_height)
            s = random.randint(4, hill_height + 2)
            d = 1
            block = world_type_blocks[world_type]
            if isinstance(block, (tuple, list)):
                block = random.choice(block)
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        if (x, y, z) in self:
                            continue

                        randomOre = random.randrange(1,100)
                        if randomOre <= 5:
                            oblock = random.choice(ore_type_blocks)
                            self.init_block((x, y +1 , z), block) #cover up the ore block top
                            self.init_block((x, y , z -1), block) #cover up the ore block back
                            self.init_block((x, y , z +1), block) #cover up the ore block front
                            self.init_block((x -1, y , z), block) #cover up the ore block left
                            self.init_block((x +1, y , z), block) #cover up the ore block right
                            self.init_block((x, y , z), oblock)
                        elif randomOre > 5:
                            self.init_block((x, y, z), block)

                        #self.init_block((x, y, z), block)

                        # Perhaps a tree
                        if self.max_trees > 0:
                            showtree = random.random()
                            if showtree <= tree_chance:
                                tree_class = world_type_trees[world_type]
                                if isinstance(tree_class, (tuple, list)):
                                    tree_class = random.choice(tree_class)
                                self.generate_tree((x, y, z), tree_class)

                s -= d

    def generate_tree(self, position, tree_class):
        x, y, z = position

        # Avoids a tree from touching another.
        if self.has_neighbors((x, y + 1, z), is_in=TREE_BLOCKS,
                              diagonals=True):
            return

        # A tree can't grow on anything.
        if self[position] not in tree_class.grows_on:
            return

        tree_class.add_to_world(self, position)

        self.max_trees -= 1

    def init_block(self, position, block):
        self.add_block(position, block, sync=False, force=False)
