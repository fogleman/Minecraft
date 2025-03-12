from __future__ import division

import sys
import random
import time
import block
import mmath

from collections import deque
from pyglet import image
from pyglet.gl import *  # noqa: F403
from pyglet.graphics import TextureGroup



if sys.version_info[0] >= 3:
    xrange = range

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

TICKS_PER_SEC = 60

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

TEXTURE_PATH = 'Textures.png'

FACES = [
        ( 0, 1, 0),
        ( 0,-1, 0),
        (-1, 0, 0),
        ( 1, 0, 0),
        ( 0, 0, 1),
        ( 0, 0,-1),
    ]

def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = mmath.normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)

class Model(object):

    def __init__(self):
        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()  # noqa: F405

        # A TextureGroup manages an OpenGL texture.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}

        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}

        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()
        
        #A constant running list for placed teleport blocks in the world and their positions
        self.teleport_blocks = {}
        self.count = 0

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # noqa: F405
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) # noqa: F405

        self._initialize()

    def _initialize(self):
        """ Initialize the world by placing all the blocks.

        """
        n = 160  # 1/2 width and length of world
        h = 0 # y-level for bottom layer (bedrock)
        s = 1  # step size
        y = 0  # initial y height
        f = 4 # frequency
        a = (1, 0.5, 0.334) # amplitude layers
        exp = 2 # elevation exponent
        adj = 1.2 # adjustment to pre-power elevation value
        
        elevation = []
        for l in xrange(n*2):
            elevation.append([0] * n*2)
            for w in xrange(n):
                nx = w/n - 0.5
                ny = l/n - 0.5
                e = a[0] * mmath.noise(f * nx, f * ny)
                e += a[1] * mmath.noise((f * 2) * nx + 5.3, (f * 2) * ny + 9.1)
                e += a[2] * mmath.noise((f * 4) * nx + 17.8, (f * 4) * ny + 23.5)
                e = e / (a[0] + a[1] + a[2])
                elevation[l][w] = pow(e * adj, exp)

        
        for x in xrange(0, n, s):
            for z in xrange(0, n, s):
                y = int(elevation[z][x]*10)
                if y <= 0:
                    y = 1
                block_texture = self.set_environment(elevation[z][x])
                self.add_block((x, y, z), block_texture, immediate=False)
                
                # Add tree
                if block_texture == block.GRASS_BLOCK and random.random() < 0.01:
                    self.grow_tree((x, y, z))
                elif block_texture == block.SAND and random.random() < 0.005:
                    self.grow_cactus((x, y, z))
                
                # Add bottom of the map
                self.add_block((x, -h, z), block.BEDROCK, immediate=True)
                
                if y > 1:
                    # Fill below the surface
                    if block_texture == block.STONE:
                        for dy in xrange(h+1, y):
                            self.add_block((x, dy, z), block.STONE, immediate=False)
                    else:
                        midpoint = int(y / 2)
                        for dy in xrange(h+1, y):
                            if dy >= midpoint:
                                self.add_block((x, dy, z), block.DIRT, immediate=False)
                            else:
                                self.add_block((x, dy, z), block.STONE, immediate=False)
                
                # create outer walls.
                if x in (0, n-1) or z in (0, n-1):
                    for dy in xrange(-5, 18):
                        self.add_block((x, y + dy, z), block.STONE_SLAB, immediate=False)

    def set_environment(self, elevation):
        block_texture = block.STONE
        if (elevation < 0.1):
            block_texture = block.WATER_BLOCK
        elif (elevation < 0.2):
                block_texture = block.SAND
        elif (elevation < 0.6):
            block_texture = block.GRASS_BLOCK
        return block_texture
    
    def grow_tree(self, position):
        y = random.randrange(3, 6)
        for ty in xrange(1, y):
            self.add_block((position[0], position[1] + ty, position[2]), block.OAK_LOG, immediate=False)
        
        for tx in xrange(-2, 3, 1):
            for tz in xrange(-2, 3, 1):
                if tx in (1, -1) or tz in (1, -1):
                    self.add_block((position[0]+tx, position[1] + y, position[2]+tz), block.OAK_LEAF, immediate=False)
                elif tx == 0 or tz == 0:
                    self.add_block((position[0]+tx, position[1] + y, position[2]+tz), block.OAK_LEAF, immediate=False)
                self.add_block((position[0]+tx, position[1] + y + 1, position[2]+tz), block.OAK_LEAF, immediate=False)
        
        for tx in xrange(-1, 2, 1):
            for tz in xrange(-1, 2, 1):
                self.add_block((position[0]+tx, position[1] + y+2, position[2]+tz), block.OAK_LEAF, immediate=False)
                if tx == 0 or tz == 0:
                    self.add_block((position[0]+tx, position[1] + y+3, position[2]+tz), block.OAK_LEAF, immediate=False)

    def grow_cactus(self, position):
        for ty in xrange(1, random.randrange(2, 5)):
            self.add_block((position[0], position[1] + ty, position[2]), block.CACTUS, immediate=False)
    
    def exposed(self, position):
        """ Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.

        """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False
    
    def exposed_faces(self, position):
        """ Returns any exposed faces.
        """
        faces = []
        
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                faces.append((x + dx, y + dy, z + dz))
        return faces
        

    def add_block(self, position, texture, immediate=True):
        """ Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.

        """
        if (texture == block.NONE):
            return
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if texture == block.PORTAL:
            self.teleport_blocks[self.count] = position
            self.count += 1
            print("portal added to list at" + (str)(position) + (str)(self.count))
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.

        """
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        for index, valueP in list(self.teleport_blocks.items()):
            if valueP == position: #is value correct position of block to be removed
                del self.teleport_blocks[index]
                self.count -= 1
                print("teleporter removed at" + (str)(position) + (str)(self.count))
                break
        
         #Fix indexes of remaining items
        self.teleport_blocks = {i: pos for i, pos in enumerate(self.teleport_blocks.values())}
        
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        """ Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.

        """
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

    def show_block(self, position, immediate=True):
        """ Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.

        """
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        """ Private implementation of the `show_block()` method.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
            
        """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.

        """
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        """ Private implementation of the 'hide_block()` method.

        """
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
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
    
    def collide(self, player, position):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.0
        p = list(position)
        np = mmath.normalize(position)
        
        for face in FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                
                for dy in xrange(player.PLAYER_HEIGHT):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.world:
                        continue
                    
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        player.velocity[1] = 0
                    break
        for dx,dy,dz in FACES:       
            check_position = (p[0] + dx, p[1]-1, p[2] + dz)
            if check_position in self.teleport_blocks.values():
                self.teleport_player(player, check_position)
                return player.position  # return new position
            
        return tuple(p)
    
    def teleport_player(self, player, c_position): #teleports to next block in list
        if not self.teleport_blocks:
            return  # No teleport blocks exist

        # Find the current index of the block
        current_index = None
        for key, value in self.teleport_blocks.items():
            if value == c_position:
                current_index = key
                break

        if current_index is not None:
            next_index = (current_index + 1) % len(self.teleport_blocks)  # Cycle to next position
            next_position = self.teleport_blocks[next_index]
            player.position = (next_position[0] + 1, next_position[1] + 2,next_position[2])  # Teleport player (offset by 1 block on x and y)
            print(f"Teleported to " +(str)(next_position))

    def _enqueue(self, func, *args):
        """ Add `func` to the internal queue.

        """
        self.queue.append((func, args))

    def _dequeue(self):
        """ Pop the top function from the internal queue and call it.

        """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False

        """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """
        while self.queue:
            self._dequeue()