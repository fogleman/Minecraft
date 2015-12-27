""" Texture for gui rendering """

from pyglet.gl import *

texture_positions_map = {}
texture_positions_map['grass'] = ((1, 0), (0, 1), (0, 0))
texture_positions_map['sand'] = ((1, 1), (1, 1), (1, 1))
texture_positions_map['brick'] = ((2, 0), (2, 0), (2, 0))
texture_positions_map['stone'] = ((2, 1), (2, 1), (2, 1))


class BlockTexture:

    def __init__(self, block):
        self.block = block
        self.texture_positions = texture_positions_map[block.madeof]
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


class TextureGroup(pyglet.graphics.Group):

    def __init__(self, path):
        super(TextureGroup, self).__init__()
        self.texture = pyglet.image.load(path).get_texture()

    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

    def unset_state(self):
        glDisable(self.texture.target)
