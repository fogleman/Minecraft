import cython

#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

cdef tuple _GRAD3, _GRAD4, _SIMPLEX
cdef double _F2, _G2, _F3, _G3

cdef class BaseNoise:
    cdef tuple permutation
    cdef int period

    @cython.locals(perm=list, perm_right=int, i=int, j=int)
    cpdef object randomize(self, object period=?)

cdef class SimplexNoise(BaseNoise):

    @cython.locals(s=double, i=double, j=double, t=double, x0=double, y0=double,
                   i1=int, j1=int, x1=double, y1=double, x2=double, y2=double, 
                   perm=tuple, ii=int, jj=int, gi0=int, gi1=int, gi2=int, 
                   tt=double, g=tuple, noise=double)
    cpdef double noise2(self, double x, double y)
