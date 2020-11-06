
import json
import pyglet
from pyglet import image
from pyglet.graphics import TextureGroup


def old_load_textures(textures):
    old_image = pyglet.image.load("texture.png").get_texture()
    return old_image


def load_textures(block_id, block_states, batch):
    pass
