import cython

#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

cdef class TerrainGeneratorBase(object):
	cdef public object seed

	cpdef object generate_sector(self, sector)

cdef class TerrainGenerator(TerrainGeneratorBase):
	cdef public:
		object base_gen
		object ocean_gen
		object river_gen
		object mount_gen
		object hill_gen
		object cave_gen
		object biome_gen

	cpdef object set_seed(self, object seed)

	cpdef object generate_chunk(self, object chunk_x, object chunk_y, object chunk_z)

	cpdef object gen_inner_layer(self, object x, object y, object z, object c)

	cpdef object gen_outer_layer(self, object x, object y, object z, object first_block, object c, object biome_type)

	cpdef object lerp(self, object x, object x1, object x2, object v00, object v01)

	cpdef object tri_lerp(self,object x, object y, object z, object v000, object v001,object v010, object v011, object v100, object v101, object v110, object v111, object x1, object x2,object  y1, y2, object z1, object z2)

	cpdef object tri_lerp_d_map(self, object d_map)

	cpdef double _clamp(self, double a)

	cpdef object density(self,object x, object y, object z)

	cpdef object base_terrain(self, object x, object y)

	cpdef object ocean_terrain(self, object x, object y)

	cpdef object rive_terrain(self, object x, object y)

	cpdef object mount_density(self, object x, object y, object z)

	cpdef object hill_density(self, object x, object y, object z)

	cpdef object cave_density(self, object x, object y, object z)


cdef class TerrainGeneratorSimple(TerrainGeneratorBase):
	cdef public:
		object world
		object rand
		object weights
		object noise
		bint skip_over
		double PERSISTENCE
		double H
		int OCTAVES
		int height_range
		int height_base
		int island_shore
		int water_level
		double zoom_level
		tuple lowlevel_ores
		tuple midlevel_ores
		tuple highlevel_ores
		tuple underwater_blocks
		tuple world_type_trees
		tuple world_type_plants
		tuple world_type_grass
		tuple island_type_grass
		tuple leaf_blocks

	cpdef double _clamp(self, double a)

	@cython.locals(y=double, weight=double)
	cpdef int get_height(self, double x, double z)

#	@cython.locals(islandheight=int, skip=bint, bx=int,
#					by=int, bz=int, bytop=int, x=double, z=double, y=int,
#					yy=int)
	cpdef object generate_sector(self, object sector)
