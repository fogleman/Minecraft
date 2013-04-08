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

def save_world(window, game_dir, world=None, save_type=COMPRESSED_SAVE_TYPE):
	if world is None: world = "world"
	if not os.path.exists(os.path.join(game_dir, world)):
		os.makedirs(os.path.join(game_dir, world))
	#window.model.items(), window.model.sectors
	#Non block related data
	save = (3,window.player, window.time_of_day)
	pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))

	blocks_save = (3,window.model.items(), window.model.sectors)
	pickle.dump(blocks_save, open(os.path.join(game_dir, world, "blocks.pkl"), "wb"))

def world_exists(game_dir, world=None):
	if world is None: world = "world"
	return os.path.lexists(os.path.join(game_dir, world))

def open_world(gamecontroller, game_dir, world=None):
	if world is None: world = "world"
	loaded_world = pickle.load(open(os.path.join(game_dir, world, "blocks.pkl"), "rb"))

	gamecontroller.model = Model(initialize=False)
	for item in loaded_world[0]:
		gamecontroller.model[item[0]] = item[1]
	gamecontroller.model.sectors = loaded_world[1]

	loaded_save = pickle.load(open(os.path.join(game_dir, world, "save.pkl"), "rb"))
	if loaded_save[0] == 3: #Version 3
		if isinstance(loaded_save[1], Player): gamecontroller.player = loaded_save[1]
		if isinstance(loaded_save[2], float):  gamecontroller.time_of_day = loaded_save[2]
