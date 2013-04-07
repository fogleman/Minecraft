import os
import cPickle as pickle
import zlib
import cStringIO as StringIO

# Modules from this project
from model import *
from player import *

# Save types
CLASSIC_SAVE_TYPE = 0
COMPRESSED_SAVE_TYPE = 1

SAVE_TYPES = [CLASSIC_SAVE_TYPE, COMPRESSED_SAVE_TYPE] # last is always the newest

def get_default_filename(game_dir):
	return os.path.join(game_dir, 'save.dat')

def save_world(window, game_dir, filename=None, save_type=COMPRESSED_SAVE_TYPE):
	filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
	save = (window.model.items(), window.model.sectors, window.player, window.time_of_day)
	if save_type == COMPRESSED_SAVE_TYPE:
		save_string = zlib.compress(pickle.dumps(save), 9)
		pickle.dump((COMPRESSED_SAVE_TYPE, save_string),
	                        open(filename, "wb"))
	elif save_type == CLASSIC_SAVE_TYPE:
		pickle.dump(save, open(filename, "wb"))

def world_exists(game_dir, filename):
	filename = filename or get_default_filename(game_dir)
	return os.path.lexists(os.path.join(game_dir, filename))

def open_world(gamecontroller, game_dir, filename=None):
	filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
	loaded_world = pickle.load(open(filename, "rb"))
	if loaded_world[0] == COMPRESSED_SAVE_TYPE:
		loaded_world = pickle.load(StringIO.StringIO(zlib.decompress(loaded_world[1])))

	save_len = len(loaded_world)

	gamecontroller.model = Model(initialize=False)
	for item in loaded_world[0]:
		gamecontroller.model[item[0]] = item[1]
	gamecontroller.model.sectors = loaded_world[1]
	if save_len > 2 and isinstance(loaded_world[2], Player):
		gamecontroller.player = loaded_world[2]
	if save_len > 3 and isinstance(loaded_world[3], float):
		gamecontroller.time_of_day = loaded_world[3]
