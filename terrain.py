"""
Terrain generating algorithm
"""

# Imports, sorted alphabetically.

# Python packages
from math import sqrt
import random

# Third-party packages
# Nothing for now
from perlin import SimplexNoise

# Modules from this project
from blocks import *
from utils import FastRandom, fast_floor, fast_abs


# Improved Perlin Noise based on Improved Noise reference implementation by Ken Perlin
class PerlinNoise(object):
    def __init__(self, seed):
        rand = FastRandom(seed)

        self.perm = [ None ] * 512
        noise_tbl = [ None ] * 256

        self.PERSISTENCE = 2.1379201
        self.H = 0.836281
        self.OCTAVES = 9
        self.weights = [ None ] * self.OCTAVES
        self.regen_weight = True

        for i in range(0, 256):
            noise_tbl[i] = i

        for i in range(0, 256):
            j = rand.randint() % 256
            j = fast_abs(j)

            noise_tbl[i], noise_tbl[j] = noise_tbl[j], noise_tbl[i]

        for i in range(0, 256):
            self.perm[i] = self.perm[i + 256] = noise_tbl[i]

    def fade(self, t) :
        return t * t * t * (t * (t * 6 - 15) + 10)

    # linear interpolate
    def lerp(self, t, a, b):
        return a + t * (b - a)

    def grad(self, hash, x, y, z):
        h = hash & 15
        u = x if h < 8 else y
        if h < 4:
            v = y
        elif h == 12 or h ==14:
            v = x
        else:
            v = z
        return (u if (h & 1) == 0 else - u) + (v if (h & 2) == 0 else -v)

    def noise(self, x, y, z):
        X = int(fast_floor(x) & 255)
        Y = int(fast_floor(y) & 255)
        Z = int(fast_floor(z) & 255)

        x -= fast_floor(x)
        y -= fast_floor(y)
        z -= fast_floor(z)

        u = self.fade(x)
        v = self.fade(y)
        w = self.fade(z)

        A = self.perm[X] + Y
        AA = self.perm[A] + Z
        AB = self.perm[(A + 1)] + Z
        B = self.perm[(X + 1)] + Y
        BA = self.perm[B] + Z
        BB = self.perm[(B + 1)] + Z

        return self.lerp(w, self.lerp(v, self.lerp(u, self.grad(self.perm[AA], x, y, z),
                                self.grad(self.perm[BA], x - 1, y, z)),
                            self.lerp(u, self.grad(self.perm[AB], x, y - 1, z),
                                self.grad(self.perm[BB], x - 1, y - 1, z))),
                            self.lerp(v, self.lerp(u, self.grad(self.perm[(AA + 1)], x, y, z - 1),
                                self.grad(self.perm[(BA + 1)], x - 1, y, z - 1)),
                            self.lerp(u, self.grad(self.perm[(AB + 1)], x, y - 1, z - 1),
                                self.grad(self.perm[(BB + 1)], x - 1, y - 1, z - 1))))

    def fBm(self, x, y, z):
        total = 0.0

        if self.regen_weight:
            self.weights = [ None ] * self.OCTAVES
            for n in range(0, self.OCTAVES):
                self.weights[n] = self.PERSISTENCE ** (-self.H * n)

            regen_weight = False

        for n in range(0, self.OCTAVES):
            total += self.noise(x, y, z) * self.weights[n]

            x *= self.PERSISTENCE
            y *= self.PERSISTENCE
            z *= self.PERSISTENCE

        return total

    @property
    def octave(self):
        return self.OCTAVES

    @octave.setter
    def octave(self, value):
        self.OCTAVES = value
        self.regen_weight = True

CHUNK_X_SIZE = 80
CHUNK_Z_SIZE = 80
CHUNK_Y_SIZE = 256

# create a array with size x_size*y_size*z_size
def init_3d_list(x_size, y_size, z_size):
    # initialize block list
    xblks = {}
    for x in xrange(x_size):
        yblks = {}
        for y in xrange(y_size):
            zblks = {}
            for z in xrange(z_size):
                zblks[z] = None
            yblks[y] = zblks
        xblks[x] = yblks
    return xblks

class Chunk(object):
    def __init__(self, position, x_size=CHUNK_X_SIZE, y_size=CHUNK_Y_SIZE, z_size=CHUNK_Z_SIZE):
        self.x_pos, self.y_pos, self.z_pos = position
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.blocks = init_3d_list(x_size, y_size, z_size)

    def get_block(self, x, y, z):
        return self.blocks[x][y][z]

    def set_block(self, x, y, z, block):
        self.blocks[x][y][z] = block

    def world_block_xpos(self, x):
        return self.x_pos + x

    def world_block_ypos(self, y):
        return self.y_pos + y

    def world_block_zpos(self, z):
        return self.z_pos + z

SAMPLE_RATE_HOR = 4
SAMPLE_RATE_VER = 4

class TerrainGenerator(object):
    def __init__(self, seed):
        self.base_gen = PerlinNoise(seed)
        self.base_gen.octave = 8
        self.ocean_gen = PerlinNoise(seed + 11)
        self.ocean_gen.octave = 8
        self.river_gen = PerlinNoise(seed + 31)
        self.river_gen.octave = 8
        self.mount_gen = PerlinNoise(seed + 41)
        self.hill_gen = PerlinNoise(seed + 71)
        self.cave_gen = PerlinNoise(seed + 141)

    def set_seed(self, seed):
        self.base_gen = PerlinNoise(seed)
        self.base_gen.octave = 8
        self.ocean_gen = PerlinNoise(seed + 11)
        self.ocean_gen.octave = 8
        self.river_gen = PerlinNoise(seed + 31)
        self.river_gen.octave = 8
        self.mount_gen = PerlinNoise(seed + 41)
        self.hill_gen = PerlinNoise(seed + 71)
        self.cave_gen = PerlinNoise(seed + 141)

    def generate_chunk(self, chunk_x, chunk_y, chunk_z):
        c = Chunk(position=(chunk_x, chunk_y, chunk_z))

        # density map
        d_map = init_3d_list(c.x_size + 1, c.y_size + 1, c.z_size + 1)

        for x in range(0, c.x_size + SAMPLE_RATE_HOR, SAMPLE_RATE_HOR):
            for z in range(0, c.z_size + SAMPLE_RATE_HOR, SAMPLE_RATE_HOR):
                for y in range(0, c.y_size + SAMPLE_RATE_VER, SAMPLE_RATE_VER):
                    d_map[x][y][z] = self.density(c.world_block_xpos(x), y, c.world_block_zpos(z))
                    #print d_map[x][y][z]

        # interpolate the missing values
        self.tri_lerp_d_map(d_map)

        for x in range(0, c.x_size):
            for z in range(0, c.z_size):
                for y in range(0, c.y_size):
                    pass
                    #print d_map[x][y][z]

        for x in range(0, CHUNK_X_SIZE):
            for z in range(0, CHUNK_Z_SIZE):
                first_block = -1
                for y in range(CHUNK_Y_SIZE - 1, 0, -1):
                    if y == 0:
                        c.set_block(x, y, z, bed_block)
                        break

                    #if 0 < y <= 32:
                    #    c.set_block(x, y, z, water_block);

                    den = d_map[x][y][z]

                    if 0 <= den < 32:
                        if first_block == -1:
                            first_block = y

                        if self.cave_density(c.world_block_xpos(x), y, c.world_block_zpos(z)) > -0.7:
                            c = self.gen_outer_layer(x, y, z, first_block, c)
                        else:
                            c.set_block(x, y, z, air_block)

                        continue
                    elif den >= 32:

                        if first_block == -1:
                            first_block = y

                        if self.cave_density(c.world_block_xpos(x), y, c.world_block_zpos(z)) > -0.6:
                            c = self.gen_inner_layer(x, y, z, c)
                        else:
                            c.set_block(x, y, z, air_block)

                        continue

                    first_block = -1
        return c
 
    def gen_inner_layer(self, x, y, z, c):
        # Mineral generation should be here also
        c.set_block(x, y, z, stone_block)
        return c

    def gen_outer_layer(self, x, y, z, first_block, c):

        depth = int(first_block - y)

        if depth == 0 and 32 < y < 128:
            c.set_block(x, y, z, grass_block)
        elif depth > 32: 
            c.set_block(x, y, z, stone_block)
        else:
            c.set_block(x, y, z, dirt_block)

        return c

    def lerp(self, x, x1, x2, v00, v01):
        return (float(x2 - x) / float(x2 - x1)) * v00 + (float(x - x1) / float(x2 - x1)) * v01

    def tri_lerp(self,x, y, z, v000, v001, v010, v011, v100, v101, v110, v111, x1, x2, y1, y2, z1, z2):
        x00 = self.lerp(x, x1, x2, v000, v100)
        x10 = self.lerp(x, x1, x2, v010, v110)
        x01 = self.lerp(x, x1, x2, v001, v101)
        x11 = self.lerp(x, x1, x2, v011, v111)
        u = self.lerp(y, y1, y2, x00, x01)
        v = self.lerp(y, y1, y2, x10, x11)
        return self.lerp(z, z1, z2, u, v)

    def tri_lerp_d_map(self, d_map):
        for x in range(0, CHUNK_X_SIZE):
            for y in range(0, CHUNK_Y_SIZE):
                for z in range(0, CHUNK_Z_SIZE):
                    if not (x % SAMPLE_RATE_HOR == 0 and y % SAMPLE_RATE_VER == 0 and z % SAMPLE_RATE_HOR == 0):
                        offsetX = int((x / SAMPLE_RATE_HOR) * SAMPLE_RATE_HOR)
                        offsetY = int((y / SAMPLE_RATE_VER) * SAMPLE_RATE_VER)
                        offsetZ = int((z / SAMPLE_RATE_HOR) * SAMPLE_RATE_HOR)
                        d_map[x][y][z] = self.tri_lerp(x, y, z, d_map[offsetX][offsetY][offsetZ], d_map[offsetX][SAMPLE_RATE_VER + offsetY][offsetZ], d_map[offsetX][offsetY][offsetZ + SAMPLE_RATE_HOR], 
                                                                d_map[offsetX][offsetY + SAMPLE_RATE_VER][offsetZ + SAMPLE_RATE_HOR], d_map[SAMPLE_RATE_HOR + offsetX][offsetY][offsetZ], d_map[SAMPLE_RATE_HOR + offsetX][offsetY + SAMPLE_RATE_VER][offsetZ], 
                                                                d_map[SAMPLE_RATE_HOR + offsetX][offsetY][offsetZ + SAMPLE_RATE_HOR], d_map[SAMPLE_RATE_HOR + offsetX][offsetY + SAMPLE_RATE_VER][offsetZ + SAMPLE_RATE_HOR], offsetX, SAMPLE_RATE_HOR + offsetX, offsetY, 
                                                                SAMPLE_RATE_VER + offsetY, offsetZ, offsetZ + SAMPLE_RATE_HOR)

    def _clamp(self, a):
        if a > 1:
            return 1
        elif a < 0:
            return 0
        else:
            return a

    def density(self, x, y, z):
        height = self.base_terrain(x, z)
        ocean = self.ocean_terrain(x, z)
        river = self.rive_terrain(x, z)

        mountains = self.mount_density(x, y, z)
        hills = self.hill_density(x, y, z)

        flatten = self._clamp(((CHUNK_Y_SIZE - 16) - y) / int(CHUNK_Y_SIZE * 0.10))

        return -y + (((32.0 + height * 32.0) * self._clamp(river + 0.25) * self._clamp(ocean + 0.25)) + mountains * 1024.0 + hills * 128.0) * flatten

    def base_terrain(self, x, z):
        return self._clamp((self.base_gen.fBm(0.004 * x, 0, 0.004 * z) + 1.0) / 2.0)

    def ocean_terrain(self, x, z):
        return self._clamp(self.ocean_gen.fBm(0.0009 * x, 0, 0.0009 * z) * 8.0)

    def rive_terrain(self, x, z):
        return self._clamp((sqrt(fast_abs(self.river_gen.fBm(0.0008 * x, 0, 0.0008 * z))) - 0.1) * 7.0)
    
    def mount_density(self, x, y, z):
        ret = self.mount_gen.fBm(x * 0.002, y * 0.001, z * 0.002)
        return ret if ret > 0 else 0

    def hill_density(self, x, y, z):
        ret = self.hill_gen.fBm(x * 0.008, y * 0.006, z * 0.008) - 0.1
        return ret if ret > 0 else 0

    def cave_density(self, x, y, z):
        return self.cave_gen.fBm(x * 0.02, y * 0.02, z * 0.02)

class TerrainGeneratorSimple(object):
    """
    A simple and fast use of (Simplex) Perlin Noise to generate a heightmap
    Based on Jimx's work on the above TerrainGenerator class
    See http://code.google.com/p/fractalterraingeneration/wiki/Fractional_Brownian_Motion for more info
    """
    def __init__(self, world, seed):
        self.world = world
        rand = random.Random(seed)
        perm = range(255)
        rand.shuffle(perm)
        self.noise = SimplexNoise(permutation_table=perm).noise2
        #self.noise = PerlinNoise(seed).noise
        self.PERSISTENCE = 2.1379201 #AKA lacunarity
        self.H = 0.836281

        #Fun things to adjust
        self.OCTAVES = 9        #Higher linearly increases calc time; increases apparent 'randomness'
        self.height_range = 32  #If you raise this, you should shrink zoom_level equally
        self.zoom_level = 0.002 #Smaller will create gentler, softer transitions. Larger is more mountainy

        self.weights = [self.PERSISTENCE ** (-self.H * n) for n in xrange(self.OCTAVES)]
    def _clamp(self, a):
        if a > 1:
            return 1
        elif a < 0:
            return 0
        else:
            return a
    def get_height(self,x,z):
        """ Given block coordinates, returns a block coordinate height """
        x *= self.zoom_level
        z *= self.zoom_level
        y = 0
        for weight in self.weights:
            y += self.noise(x, z) * weight

            x *= self.PERSISTENCE
            z *= self.PERSISTENCE

        return int(self._clamp((y+1)/2)*self.height_range)
    def generate_sector(self, sector):
        #For ease of saving/loading, generates a whole region (4x4x4 sectors) at once
        world = self.world
        cx, cy, cz = world.savingsystem.sector_to_blockpos(sector)
        rx, ry, rz = cx/32*32, cy/32*32, cz/32*32

        #Create the sector so even if the worldgen says its air, it'll still prevent future generation attempts
        for secx in xrange(rx/8,rx/8+4):
            for secy in xrange(ry/8,ry/8+4):
                for secz in xrange(rz/8,rz/8+4):
                    world.sectors[(secx,secy,secz)] = []

        if 0 >= ry < 32:
            #The current terraingen doesn't build higher than 32.
            rytop = ry + 31
            world_init_block, self_get_height = world.init_block, self.get_height #Localize for speed
            for x in xrange(rx, rx+32):
                for z in xrange(rz, rz+32):
                    y = self_get_height(x,z)
                    if ry <= y <= rytop:
                        world_init_block((x, y, z), grass_block)