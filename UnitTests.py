import pytest

from main import cube_vertices
from main import tex_coord
from main import Model

m = Model()

#Test the verticies and bounds, why is this useful?
class mainTests():
	position = (10,10,10)
	#test that the cube is defined correctly
	assert cube_vertices(1,1,1,1) ==  [0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
									   0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2,
									   0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0,
									   2, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2,
									   0, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 
									   2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0]
	
	#Test that bounds of the square are correct
	assert tex_coord(1,1, n=4) == (.25, .25, .5, .25, .5, .5, .25, .5)

	#Other tests here
	assert m.show_block(position) == () 