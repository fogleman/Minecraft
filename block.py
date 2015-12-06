""" A block with texture """

texture_positions_map = {}
texture_positions_map['grass'] = ((1, 0), (0, 1), (0, 0))


class Block:

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
