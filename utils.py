import pyglet
import os

def load_image(*args):
	return pyglet.image.load(os.path.join(*args))

def image_sprite(image, batch, group, x=0, y=0, width=None, height=None):
	width = width or image.width
	height = height or image.height
	if isinstance(group, int):
		group = pyglet.graphics.OrderedGroup(group)
	return pyglet.sprite.Sprite(image.get_region(x, y, width, height), batch=batch, group=group)