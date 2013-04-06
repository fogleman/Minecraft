import pyglet.media
from os import path

pyglet.resource.path = [path.join('resources', 'sounds')]
pyglet.resource.reindex()

wood_break = pyglet.resource.media('wood_break.wav', streaming=False)
water_break = pyglet.resource.media('water_break.wav', streaming=False)
