import pytest

from main import cube_vertices
from main import tex_coord
from main import Model
from main import normalize 

m = Model()

#Test the verticies and bounds, why is this useful?
class mainTests():
    position = (10,10,10)
    
    assert normalize(position) == (10,10,10)
    assert normalize(position) != (11,9,10)
    
    position = (1,-1,100)
    
    assert normalize(position) == (1,-1,100)
    assert normalize(position) != (1,1,100)
    
    #test that the cube is defined correctly
        #x,y,z,n
        #x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        #x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        #x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        #x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        #x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        #x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
        
    assert cube_vertices(1,1,1,1) ==  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                                       0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
                                       0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
                                       2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
                                       0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
                                       2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
    assert cube_vertices(1,0,0,1) !=  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                                       0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
                                       0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
                                       2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
                                       0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
                                       2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
    assert cube_vertices(1,1,1,0) !=  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                                       0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
                                       0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
                                       2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
                                       0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
                                       2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
    
    #dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m
    #Test that bounds of the square are correct
    assert tex_coord(1,1, n=4) == (.25, .25, .5, .25, .5, .5, .25, .5)
    assert tex_coord(2,1, n=4) != (.25, .25, .5, .25, .5, .5, .25, .5)
    assert tex_coord(1,2, n=4) != (.25, .25, .5, .25, .5, .5, .25, .5)
    assert tex_coord(2,1, n=4) == (.5, .25, .75, .25, .75, .5, .5, .5)
    assert tex_coord(8,2, n=4) != (.25, .25, .5, .25, .5, .5, .25, .5)
    assert tex_coord(2,24, n=4) != (.5, .25, .75, .25, .75, .5, .5, .5)
    assert tex_coord(1,1, n=4) != (1, 1, 2, 1, 2, 2, 1, 2)
    assert tex_coord(3,2, n=4) == (.75, .5, 1, .5, 1, .75, .75, .75)
    assert tex_coord(3,-2, n=4) == (.75, -.5, 1, -.5, 1, -.25, .75, -.25)
    assert tex_coord(-3,-2, n=4) != (.75, -.5, 1, -.5, .1, -.25, .75, -.25)
    assert tex_coord(8,8, n=4) != (2, 2, 2.25, 2, 2.25, 2.25, 2, 2.26)
    assert tex_coord(8,8, n=4) == (2, 2, 2.25, 2, 2.25, 2.25, 2, 2.25)

    position = (1,0,8)
    
    assert normalize(position) == (1,0,8)
    assert normalize(position) != (1,0,8.25)
    
    position = (-.25,-1,12)
    
    assert normalize(position) != (-.25,-1,12)
    assert normalize(position) != (.25,1,1)
        #x,y,z,n
        #x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        #x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        #x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        #x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        #x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        #x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
        
    assert cube_vertices(0,0,0,0) ==  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert cube_vertices(2,3,4,5) ==  [-3, 8, -1, -3, 8, 9, 7, 8, 9, 7, 8, -1,
                                       -3, -2, -1, 7, -2, -1, 7, -2, 9, -3, -2, 9,
                                       -3, -2, -1, -3, -2, 9, -3, 8, 9, -3, 8, -1,
                                       7, -2, 9, 7, -2, -1, 7, 8, -1, 7, 8, 9,
                                       -3, -2, 9, 7, -2, 9, 7, 8, 9, -3, 8, 9, 
                                       7, -2, -1, -3, -2, -1, -3, 8, -1, 7, 8, -1]
    assert cube_vertices(5,0,0,0) !=  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                                       0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
                                       0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
                                       2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
                                       0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
                                       2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
    assert cube_vertices(-1,1,1,1) !=  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                                       0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
                                       0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
                                       2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
                                       0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
                                       2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
    assert cube_vertices(2,3,4,-5) !=  [-3, 8, -1, -3, 8, 9, 7, 8, 9, 7, 8, -1,
                                       -3, -2, -1, 7, -2, -1, 7, -2, 9, -3, -2, 9,
                                       -3, -2, -1, -3, -2, 9, -3, 8, 9, -3, 8, -1,
                                       7, -2, 9, 7, -2, -1, 7, 8, -1, 7, 8, 9,
                                       -3, -2, 9, 7, -2, 9, 7, 8, 9, -3, 8, 9, 
                                       7, -2, -1, -3, -2, -1, -3, 8, -1, 7, 8, -1]
