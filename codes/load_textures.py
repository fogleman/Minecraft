
import json
import pyglet
from pyglet import image
from pyglet.graphics import TextureGroup


def old_l_t(textures):
    """
    old_l_t stand for old_load_textuers
    """
    old_image = pyglet.image.load("texture.png").get_texture()
    return old_image


def l_t(block_id, block_states):
    """
    l_t stand for load_textures
    """
    pass
