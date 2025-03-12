def tex_coord(x, y, w=32, h=16):
    """ Return the bounding vertices of the texture square.

    """
    width = 1.0 / w
    height = 1.0 / h
    dx = x * width
    dy = y * height
    return dx, dy, dx + width, dy, dx + width, dy + height, dx, dy + height

def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

NONE = None
#Row 1
STONE = tex_coords((19, 15), (19, 15), (19, 15))
GRASS_BLOCK = tex_coords((2, 15), (18, 14), (10, 15))
DIRT = tex_coords((18, 14), (18, 14), (18, 14))
PODZOL = tex_coords((19, 14), (18, 14), (20, 14))
COBBLESTONE = tex_coords((26, 15), (26, 15), (26, 15))
OAK_WOOD_PLANK = tex_coords((21, 14), (21, 14), (21, 14))
SPRUCE_WOOD_PLANK = tex_coords((22, 14), (22, 14), (22, 14))
BIRCH_WOOD_PLANK = tex_coords((23, 14), (23, 14), (23, 14))
JUNGLE_WOOD_PLANK = tex_coords((24, 14), (24, 14), (24, 14))
ACACIA_WOOD_PLANK = tex_coords((25, 14), (25, 14), (25, 14))
DARK_OAK_WOOD_PLANK = tex_coords((26, 14), (26, 14), (26, 14))
#Row 2
BRICK = tex_coords((29, 14), (29, 14), (29, 14))
BEDROCK = tex_coords((0, 14), (0, 14), (0, 14))
SAND = tex_coords((5, 14), (5, 14), (5, 14))
CACTUS = tex_coords((15, 10), (15, 10), (16, 10))
#Row 5
LAMP = tex_coords((25, 7), (25, 7), (25, 7))
PORTAL = tex_coords((26, 6), (26, 6), (26, 6))

STONE_SLAB = tex_coords((27, 14),(27, 14),(28, 14))

WATER_BLOCK = tex_coords((0, 1),(0, 1),(0, 1))

OAK_LOG = tex_coords((4, 12), (4, 12), (3, 12))
OAK_LEAF = tex_coords((7, 10), (7, 10), (7, 10))