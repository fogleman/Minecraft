import pyglet
import os

def load_image(*args):
	return pyglet.image.load(os.path.join(*args))