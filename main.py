from pyglet.gl import *
from pyglet.window import key
import math
import random
import time
from ctypes import c_float

SECTOR_SIZE = 16

def cube_vertices(x, y, z, n):
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n, # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n, # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n, # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n, # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n, # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n, # back
    ]

def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

class TextureGroup(pyglet.graphics.Group):
    def __init__(self, data):
        super(TextureGroup, self).__init__()
        self.texture = pyglet.image.load('texture.png').get_texture()
    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)
    def unset_state(self):
        glDisable(self.texture.target)

def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def sectorize(position):
    x, y, z = normalize(position)
    x, y, z = x / SECTOR_SIZE, y / SECTOR_SIZE, z / SECTOR_SIZE
    return (x, 0, z)

class Model(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(TEXTURE_DATA)
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = []
        self.initialize()
    def initialize(self):
        n = 80
        s = 1
        y = 0
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                self.init_block((x, y - 2, z), GRASS)
                self.init_block((x, y - 3, z), STONE)
                if x in (-n, n) or z in (-n, n):
                    for dy in xrange(-2, 3):
                        self.init_block((x, y + dy, z), STONE)
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o)
            b = random.randint(-o, o)
            c = -1
            h = random.randint(1, 6)
            s = random.randint(4, 8)
            d = 1
            t = random.choice([GRASS, SAND, BRICK])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.init_block((x, y, z), t)
                s -= d
    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False
    def init_block(self, position, texture):
        self.add_block(position, texture, False)
    def add_block(self, position, texture, sync=True):
        if position in self.world:
            self.remove_block(position, sync)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if sync:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)
    def remove_block(self, position, sync=True):
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if sync:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)
    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)
    def show_blocks(self):
        for position in self.world:
            if position not in self.shown and self.exposed(position):
                self.show_block(position)
    def show_block(self, position, immediate=True):
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self.enqueue(self._show_block, position, texture)
    def _show_block(self, position, texture):
        x, y, z = position
        # only show exposed faces
        index = 0
        count = 24
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        for dx, dy, dz in []:#FACES:
            if (x + dx, y + dy, z + dz) in self.world:
                count -= 4
                i = index * 12
                j = index * 8
                del vertex_data[i:i + 12]
                del texture_data[j:j + 8]
            else:
                index += 1
        # create vertex list
        self._shown[position] = self.batch.add(count, GL_QUADS, self.group, 
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))
    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self.enqueue(self._hide_block, position)
    def _hide_block(self, position):
        self._shown.pop(position).delete()
    def show_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)
    def hide_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)
    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]: # xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)
    def enqueue(self, func, *args):
        self.queue.append((func, args))
    def dequeue(self):
        func, args = self.queue.pop(0)
        func(*args)
    def process_queue(self):
        start = time.clock()
        while self.queue and time.clock() - start < 1 / 60.0:
            self.dequeue()
    def process_entire_queue(self):
        while self.queue:
            self.dequeue()

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.exclusive = False
        self.flying = False
        self.strafe = [0, 0]
        self.position = (0, 0, 0)
        self.rotation = (0, 0)
        self.sector = None
        self.reticle = None
        self.dy = 0
        self.model = Model()
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18, 
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top', 
            color=(0, 0, 0, 255))
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)
    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
    def get_sight_vector(self):
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)
    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            if self.flying:
                m = math.cos(math.radians(y))
                dy = math.sin(math.radians(y))
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    dy *= -1
                dx = math.cos(math.radians(x + strafe)) * m
                dz = math.sin(math.radians(x + strafe)) * m
            else:
                dy = 0.0
                dx = math.cos(math.radians(x + strafe))
                dz = math.sin(math.radians(x + strafe))
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
    def update(self, dt):
        self.model.process_queue()
        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)
    def _update(self, dt):
        # walking
        speed = 15 if self.flying else 5
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            self.dy -= dt / 4
            self.dy = max(self.dy, -0.5)
            dy += self.dy
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), 2)
        self.position = (x, y, z)
    def collide(self, position, height):
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES: # check all surrounding blocks
            for i in xrange(3): # check each dimension independently
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height): # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    op = tuple(op)
                    if op not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        return tuple(p)
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        return
        x, y, z = self.position
        dx, dy, dz = self.get_sight_vector()
        d = scroll_y * 10
        self.position = (x + dx * d, y + dy * d, z + dz * d)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.position, vector)
            if button == pyglet.window.mouse.LEFT:
                if block:
                    texture = self.model.world[block]
                    if texture != STONE:
                        self.model.remove_block(block)
            else:
                if previous:
                    self.model.add_block(previous, BRICK)
        else:
            self.set_exclusive_mouse(True)
    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = 0.065
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
    def on_key_release(self, symbol, modifiers):
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
    def on_resize(self, width, height):
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width / 2, self.height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )
    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def set_3d(self):
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)
    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()
    def draw_label(self):
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z, 
            len(self.model._shown), len(self.model.world))
        self.label.draw()
    def draw_reticle(self):
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)

def setup_fog():
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (c_float * 4)(0.53, 0.81, 0.98, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_DENSITY, 0.35)
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)

def setup():
    glClearColor(0.53, 0.81, 0.98, 1)
    glEnable(GL_CULL_FACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()

def main():
    window = Window(width=800, height=600, caption='Pyglet', resizable=True)
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()

TEXTURE_DATA = (
    "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"
    "gg=="
)

if __name__ == '__main__':
    main()
