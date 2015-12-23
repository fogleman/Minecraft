""" A block with texture """

texture_positions_map = {}
texture_positions_map['grass'] = ((1, 0), (0, 1), (0, 0))
texture_positions_map['sand'] = ((1, 1), (1, 1), (1, 1))
texture_positions_map['brick'] = ((2, 0), (2, 0), (2, 0))
texture_positions_map['stone'] = ((2, 1), (2, 1), (2, 1))


class Block:
    """ Represents a block made of one out of different materials available.
    This class should contain info to be used by different renderers.
    As it is now, it has texture information only used by the gui version. """

    def __init__(self, madeof='grass'):
        self.madeof = madeof
        self.texture_positions = texture_positions_map[madeof]
        self.texture = self.tex_coords(*self.texture_positions)

    def tex_coord(self, x, y, n=4):
        m = 1.0 / n
        dx = x * m
        dy = y * m
        return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

    def tex_coords(self, top, bottom, side):
        top = self.tex_coord(*top)
        bottom = self.tex_coord(*bottom)
        side = self.tex_coord(*side)
        result = []
        result.extend(top)
        result.extend(bottom)
        result.extend(side * 4)
        return result


GRASS = Block('grass')
BRICK = Block('brick')
SAND = Block('sand')
STONE = Block('stone')
