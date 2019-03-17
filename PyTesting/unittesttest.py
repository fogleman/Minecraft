import pytest
from pyFunc import addTwo

def plusFive (x):
	return x + 5

class testImport():
	assert addTwo(5) == 7
	assert addTwo(3) == 5

#class testUnits():
#	assert plusFive(3) == 8 
#       assert plusFive(2) == 87
