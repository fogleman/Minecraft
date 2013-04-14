# Imports, sorted alphabetically.

# Python packages
from collections import deque, defaultdict
import os
import warnings

# Third-party packages
import pyglet
from pyglet.gl import *

# Modules from this project
from blocks import *
import globals as G


FACES = (
    ( 0,  1,  0),
    ( 0, -1,  0),
    (-1,  0,  0),
    ( 1,  0,  0),
    ( 0,  0,  1),
    ( 0,  0, -1),
)

FACES_WITH_DIAGONALS = FACES + (
    (-1, -1,  0),
    (-1,  0, -1),
    ( 0, -1, -1),
    ( 1,  1,  0),
    ( 1,  0,  1),
    ( 0,  1,  1),
    ( 1, -1,  0),
    ( 1,  0, -1),
    ( 0,  1, -1),
    (-1,  1,  0),
    (-1,  0,  1),
    ( 0, -1,  1),
)


def normalize_float(f):
    """
    This is faster than int(round(f)).  Nearly two times faster.
    Since it is run at least 500,000 times during map generation,
    and also in game logic, it has a major impact on performance.

    >>> normalize_float(0.2)
    0
    >>> normalize_float(-0.4)
    0
    >>> normalize_float(0.5)
    1
    >>> normalize_float(-0.5)
    -1
    >>> normalize_float(0.0)
    0
    """
    int_f = int(f)
    if f > 0:
        if f - int_f < 0.5:
            return int_f
        return int_f + 1
    if f - int_f > -0.5:
        return int_f
    return int_f - 1


def normalize(position):
    x, y, z = position
    return normalize_float(x), normalize_float(y), normalize_float(z)


def sectorize(position):
    x, y, z = normalize(position)
    x, y, z = (x / G.SECTOR_SIZE,
               y / G.SECTOR_SIZE,
               z / G.SECTOR_SIZE)
    return x, y, z


class TextureGroup(pyglet.graphics.Group):
    def __init__(self, path):
        super(TextureGroup, self).__init__()
        self.texture = pyglet.image.load(path).get_texture()

    def set_state(self):
        glBindTexture(self.texture.target, self.texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glEnable(self.texture.target)

    def unset_state(self):
        glDisable(self.texture.target)


class World(dict):
    spreading_mutations = {
        dirt_block: grass_block,
    }

    def __init__(self):
        super(World, self).__init__()
        self.batch = pyglet.graphics.Batch()
        self.transparency_batch = pyglet.graphics.Batch()
        self.group = TextureGroup(os.path.join('resources', 'textures', 'texture.png'))

        self.shown = {}
        self._shown = {}
        self.sectors = defaultdict(list)
        self.before_set = set()
        self.urgent_queue = deque()
        self.lazy_queue = deque()

        self.spreading_mutable_blocks = deque()
        self.spreading_time = 0.0

    def __delitem__(self, position):
        super(World, self).__delitem__(position)

        if position in self.spreading_mutable_blocks:
            try:
                self.spreading_mutable_blocks.remove(position)
            except ValueError:
                warnings.warn('Block %s was unexpectedly not found in the '
                              'spreading mutations; your save is probably '
                              'corrupted' % repr(position))

    def add_block(self, position, block, sync=True, force=True):
        if position in self:
            if not force:
                return
            self.remove_block(None, position, sync=sync)
        if block.id == furnace_block.id:
            self[position] = FurnaceBlock()
        else:
            self[position] = block
        self.sectors[sectorize(position)].append(position)
        if sync:
            if self.is_exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, player, position, sync=True, sound=True):
        if sound and player is not None:
            self[position].play_break_sound(player, position)
        del self[position]
        sector_position = sectorize(position)
        try:
            self.sectors[sector_position].remove(position)
        except ValueError:
            warnings.warn('Block %s was unexpectedly not found in sector %s;'
                          'your save is probably corrupted'
                          % (position, sector_position))
        if sync:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def neighbors_iterator(self, position, relative_neighbors_positions=FACES):
        x, y, z = position
        for dx, dy, dz in relative_neighbors_positions:
            yield x + dx, y + dy, z + dz

    def check_neighbors(self, position):
        for other_position in self.neighbors_iterator(position):
            if other_position not in self:
                continue
            if self.is_exposed(other_position):
                self.check_spreading_mutable(other_position,
                                             self[other_position])
                if other_position not in self.shown:
                    self.show_block(other_position)
            else:
                if other_position in self.shown:
                    self.hide_block(other_position)

    def check_spreading_mutable(self, position, block):
        x, y, z = position
        above_position = x, y + 1, z
        if above_position in self \
                or position in self.spreading_mutable_blocks \
                or not self.is_exposed(position):
            return
        if block in self.spreading_mutations and self.has_neighbors(
                position,
                is_in=(self.spreading_mutations[block],),
                diagonals=True):
            self.spreading_mutable_blocks.appendleft(position)

    def has_neighbors(self, position, is_in=None, diagonals=False,
                      faces=None):
        if faces is None:
            faces = FACES_WITH_DIAGONALS if diagonals else FACES
        for other_position in self.neighbors_iterator(
                position, relative_neighbors_positions=faces):
            if other_position in self:
                if is_in is None or self[other_position] in is_in:
                    return True
        return False

    def is_exposed(self, position):
        for other_position in self.neighbors_iterator(position):
            if other_position not in self or self[other_position].transparent:
                return True
        return False

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        dx, dy, dz = dx / m, dy / m, dz / m
        previous = ()
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self:
                return key, previous
            previous = key
            x, y, z = x + dx, y + dy, z + dz
        return None, None

    def hide_block(self, position, immediate=True):
        del self.shown[position]
        if immediate:
            self._hide_block(position)
        else:
            self.enqueue(self._hide_block, position)

    def _hide_block(self, position):
        self._shown.pop(position).delete()

    def show_block(self, position, immediate=True):
        block = self[position]
        self.shown[position] = block
        if immediate:
            self._show_block(position, block)
        else:
            self.enqueue(self._show_block, position, block)

    def _show_block(self, position, block):
    #    x, y, z = position
        # only show exposed faces
    #    index = 0
        vertex_data = block.get_vertices(*position)
        texture_data = block.texture_data
        count = len(texture_data) / 2
        # FIXME: Do something of what follows.
    #    for dx, dy, dz in []:  # FACES:
    #        if (x + dx, y + dy, z + dz) in self:
    #            count -= 8  # 4
    #            i = index * 12
    #            j = index * 8
    #            del vertex_data[i:i + 12]
    #            del texture_data[j:j + 8]
    #        else:
    #            index += 1

        # create vertex list
        batch = self.transparency_batch if block.transparent else self.batch
        self._shown[position] = batch.add(count, GL_QUADS, block.group or self.group,
                                          ('v3f/static', vertex_data),
                                          ('t2f/static', texture_data))

    def show_sector(self, sector, immediate=False):
        self.delete_opposite_task(self._hide_sector, sector)

        if immediate:
            self._show_sector(sector)
        else:
            self.enqueue(self._show_sector, sector, urgent=True)

    def _show_sector(self, sector):
        for position in self.sectors.get(sector, ()):
            if position not in self.shown and self.is_exposed(position):
                self.show_block(position)

    def hide_sector(self, sector, immediate=False):
        self.delete_opposite_task(self._show_sector, sector)

        if immediate:
            self._hide_sector(sector)
        else:
            self.enqueue(self._hide_sector, sector)

    def _hide_sector(self, sector):
        for position in self.sectors.get(sector, ()):
            if position in self.shown:
                self.hide_block(position)

    def change_sectors(self, after):
        before_set = self.before_set
        after_set = set()
        pad = G.VISIBLE_SECTORS_RADIUS
        x, y, z = after
        for dx in xrange(-pad, pad + 1):
            for dy in xrange(-2, 2):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    after_set.add((x + dx, y + dy, z + dz))
        for sector in (after_set - before_set):
            self.show_sector(sector)
        for sector in (before_set - after_set):
            self.hide_sector(sector)
        self.before_set = after_set

    def enqueue(self, func, *args, **kwargs):
        task = func, args, kwargs
        urgent = kwargs.pop('urgent', False)
        queue = self.urgent_queue if urgent else self.lazy_queue
        if task not in queue:
            queue.appendleft(task)

    def dequeue(self):
        queue = self.urgent_queue or self.lazy_queue
        func, args, kwargs = queue.pop()
        func(*args, **kwargs)

    def delete_opposite_task(self, func, *args, **kwargs):
        opposite_task = func, args, kwargs
        if opposite_task in self.lazy_queue:
            self.lazy_queue.remove(opposite_task)

    def process_queue(self, dt):
        if self.urgent_queue or self.lazy_queue:
            self.dequeue()

    def process_entire_queue(self):
        while self.urgent_queue or self.lazy_queue:
            self.dequeue()

    def content_update(self, dt):
        # Updates spreading
        # TODO: This is too simple
        self.spreading_time += dt
        if self.spreading_time >= G.SPREADING_MUTATION_DELAY:
            self.spreading_time = 0.0
            if self.spreading_mutable_blocks:
                position = self.spreading_mutable_blocks.pop()
                self.add_block(position,
                               self.spreading_mutations[self[position]])
