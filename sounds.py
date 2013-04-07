import globals
import pyglet.media
from os import path
pyglet.resource.path = [".","resources/sounds"] #Note: Pyglet uses /'s regardless of OS
pyglet.resource.reindex()

wood_break = pyglet.resource.media("wood_break.wav", streaming=False)
water_break = pyglet.resource.media("water_break.wav", streaming=False)
leaves_break = pyglet.resource.media("leaves_break.wav", streaming=False)
glass_break = pyglet.resource.media("glass_break.wav", streaming=False)
dirt_break = pyglet.resource.media("dirt_break.wav", streaming=False)
gravel_break = pyglet.resource.media("gravel_break.wav", streaming=False)
stone_break = pyglet.resource.media("stone_break.wav", streaming=False)
melon_break = pyglet.resource.media("melon_break.wav", streaming=False)
sand_break = pyglet.resource.media("sand_break.wav", streaming=False)

def play_sound(sound):
    player = pyglet.media.ManagedSoundPlayer()
    player.volume = globals.EFFECT_VOLUME
    player.queue(sound)
    player.play()
    return player