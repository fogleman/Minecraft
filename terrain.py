# Terrain generating algorithm

# use Perlin Noise 2D to generate a SMOOTH height map
# it's very fast, but the disadvantage is that it can't generate overhangs and caves

# TODO: Perlin Noise 3D

from math import cos, pi
from random import randint

# some prime numbers
X_FACTOR = 1069
Y_FACTOR = 4289
Z_FACTOR = 6343
SEED_FACTOR = 6079

PERSISTENCE = 1.5
OCTAVES = 13

# HeightMap.perlin_noise_2d(x, y) will return the height at (x, y)
class HeightMap(object):
	def __init__(self, seed, persistence = PERSISTENCE, octaves = OCTAVES):
		self.seed = seed
		self.persistence = persistence
		self.octaves = octaves

	# returns a random number between -1.0 and 1.0
	# noise(n) = 15731*n^3 + 789221*n + 1376312589
	def noise_2d(self, x, y):
		n = (X_FACTOR * x + Y_FACTOR * y + SEED_FACTOR * self.seed) & 2147483647
		n = (n >> 13) ^ n
		n = (n * (n * n * 15731 + 789221) + 1376312589) & 2147483647
		return 1 - float(n) / 1073741824

	def linear_interpolate(self, a, b, x):
		return a * (1 - x) + b * x

	# much smoother curves
	def cosine_interpolate(self, a, b, x):
		ft = x * pi
		f = (1 - cos(ft)) * 0.5

		return  a * (1 - f) + b * f

	def interpolate(self, a, b, x):
		return self.cosine_interpolate(a, b, x)

	def smooth_noise_2d(self, x, y):
		# corners
		# *-*
		# ---
		# *-*
		corners = ( self.noise_2d(x-1, y-1)+self.noise_2d(x+1, y-1)+self.noise_2d(x-1, y+1)+self.noise_2d(x+1, y+1) ) / 16
		# sides
		# -*-
		# *-*
		# -*-
		sides   = ( self.noise_2d(x-1, y)  +self.noise_2d(x+1, y)  +self.noise_2d(x, y-1)  +self.noise_2d(x, y+1) ) /  8
		center  =  self.noise_2d(x, y) / 4

		return corners + sides + center

	def interpolate_noise_2d(self, x, y):
		integer_x    = int(x)
		fractional_x = x - integer_x

		integer_y    = int(y)
		fractional_y = y - integer_y

		v1 = self.smooth_noise_2d(integer_x,     integer_y)
		v2 = self.smooth_noise_2d(integer_x + 1, integer_y)
		v3 = self.smooth_noise_2d(integer_x,     integer_y + 1)
		v4 = self.smooth_noise_2d(integer_x + 1, integer_y + 1)

		i1 = self.interpolate(v1 , v2 , fractional_x)
		i2 = self.interpolate(v3 , v4 , fractional_x)

		return self.interpolate(i1 , i2 , fractional_y)

	def perlin_noise_2d(self, x, y):
		total = 0
		p = self.persistence
		n = self.octaves - 1

		for i in range(0, n):
			frequency = 2 ** i
			amplitude = p ** i

			total = total + self.interpolate_noise_2d(x * frequency, y * frequency) * amplitude

		return total


# a test to generate a 16 * 16 height map
#hm = HeightMap(randint(0, 2147483647))
#for x in range(0, 15):
#	print('')
#	for y in range(0,15):
#		print('\t'),
#		print(abs(int(hm.perlin_noise_2d(x * 0.0001, y * 0.0001)))),
