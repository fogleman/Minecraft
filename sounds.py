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

def play_sound(sound, player=None, position=None):
	pyglet.options['audio'] = ('openal', 'directsound', 'alsa', 'silent')
	sound_player = pyglet.media.ManagedSoundPlayer()
	pyglet.media.listener.volume = globals.EFFECT_VOLUME
	if position:
		sound_player.position = position
	if sound_player:
		pyglet.media.listener.position = player.position
	sound_player.queue(sound)
	sound_player.play()
	return sound_player