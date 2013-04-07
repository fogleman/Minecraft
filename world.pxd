import cython


@cython.locals(int_f=int)
cpdef int normalize_float(float f)


@cython.locals(x=float, y=float, z=float)
cpdef tuple normalize(tuple position)


@cython.locals(x=int, y=int, z=int)
cpdef tuple sectorize(tuple position)


@cython.locals(spreading_mutations=dict)
cdef class World(dict):
    cdef public object batch
    cdef public object group
    cdef public dict exposed
    cdef public dict shown
    cdef public dict _shown
    cdef public object sectors
    cdef public object urgent_queue, lazy_queue
    cdef public tuple spreading_mutation_classes
    cdef public double spreading_time

    cpdef object add_block(self, tuple position, object block,
                           bint sync=?, bint force=?)

    cpdef object remove_block(self, object player, tuple position, bint sync=?, bint sound=?)

    # Generators are not handled by Cython for the moment.
    # @cython.locals(x=float, y=float, z=float,
    #                dx=float, dy=float, dz=float)
    # cpdef object neighbors_iterator(self, tuple position,
    #                                 tuple relative_neighbors_positions=?)

    @cython.locals(other_position=tuple)
    cpdef object check_neighbors(self, tuple position)

    @cython.locals(faces=tuple, other_position=tuple)
    cpdef bint has_neighbors(self, tuple position,
                             object type=?,bint diagonals=?)

    @cython.locals(other_position=tuple)
    cpdef bint is_exposed(self, tuple position)

    @cython.locals(m=int, _=int,
                   x=float, y=float, z=float,
                   dx=float, dy=float, dz=float,
                   previous=tuple, key=tuple)
    cpdef tuple hit_test(self, tuple position, tuple vector,
                         int max_distance=?)

    cpdef object hide_block(self, tuple position, bint immediate=?)

    cpdef object _hide_block(self, tuple position)

    @cython.locals(position=tuple)
    cpdef object show_blocks(self)

    @cython.locals(block=object)
    cpdef object show_block(self, tuple position, bint immediate=?)

    @cython.locals(x=float, y=float, z=float,
                   index=int, count=int,
                   vertex_data=cython.list, texture_data=cython.list,
                   dx=float, dy=float, dz=float,
                   i=int, j=int)
    cpdef object _show_block(self, tuple position, object block)

    cpdef object show_sector(self, tuple sector, bint immediate=?)

    @cython.locals(position=tuple)
    cpdef object _show_sector(self, tuple sector)

    cpdef object hide_sector(self, tuple sector, bint immediate=?)

    @cython.locals(position=tuple)
    cpdef object _hide_sector(self, tuple sector)

    @cython.locals(before_set=set, after_set=set, pad=int,
                   dx=int, dy=int, dz=int,
                   x=int, y=int, z=int,
                   show=set, hide=set, sector=tuple)
    cpdef object change_sectors(self, tuple before, tuple after)

    @cython.locals(queue=object)
    cpdef object dequeue(self)

    cpdef object process_queue(self, double dt)

    cpdef object process_entire_queue(self)

    @cython.locals(position=tuple, block=object)
    cpdef object content_update(self, double dt)
