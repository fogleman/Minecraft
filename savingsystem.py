import os
import cPickle as pickle
import zlib
import cStringIO as StringIO

# Save types

CLASSIC_SAVE_TYPE = 0
COMPRESSED_SAVE_TYPE = 1

SAVE_TYPES = [CLASSIC_SAVE_TYPE, COMPRESSED_SAVE_TYPE] # last is always the newest

def get_default_filename(game_dir):
	return os.path.join(game_dir, 'save.dat')

def save_world(window, game_dir, filename=None, save_type=COMPRESSED_SAVE_TYPE):
	filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
	save = (window.model.world, window.model.sectors, window.strafe,
                         window.player, window.time_of_day)
	if save_type == COMPRESSED_SAVE_TYPE:
		save_string = zlib.compress(pickle.dumps(save), 9)
		pickle.dump((COMPRESSED_SAVE_TYPE, save_string),
	                        open(filename, "wb"))
	elif save_type == CLASSIC_SAVE_TYPE:
		pickle.dump(save, open(filename, "wb"))

def world_exists(game_dir, filename):
	filename = filename or get_default_filename(game_dir)
	return os.path.lexists(os.path.join(game_dir, filename))

def open_world(game_dir, filename=None):
	filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
	loaded_world = pickle.load(open(filename, "rb"))
	if loaded_world[0] == COMPRESSED_SAVE_TYPE:
		loaded_world = pickle.load(StringIO.StringIO(zlib.decompress(loaded_world[1])))
	return loaded_world
