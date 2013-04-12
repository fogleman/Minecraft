import pyglet
import os

def load_image(*args):
	path = os.path.join(*args)
	return pyglet.image.load(os.path.join(*args)) if os.path.isfile(path) else None

def image_sprite(image, batch, group, x=0, y=0, width=None, height=None):
	if image == None or batch == None or group == None:
		return None
	width = width or image.width
	height = height or image.height
	if isinstance(group, int):
		group = pyglet.graphics.OrderedGroup(group)
	return pyglet.sprite.Sprite(image.get_region(x, y, width, height), batch=batch, group=group)

def hidden_image_sprite(*args, **kwargs):
	sprite = image_sprite(*args, **kwargs)
	if sprite:
		sprite.visible = False
	return sprite