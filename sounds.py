import pyglet.media
from os import path
pyglet.resource.path = [".","resources/sounds"] #Note: Pyglet uses /'s regardless of OS
pyglet.resource.reindex()

wood_break = pyglet.resource.media("wood_break.wav", streaming=False)
water_break = pyglet.resource.media("water_break.wav", streaming=False)
leaves_break = pyglet.resource.media("leaves_break.wav", streaming=False)