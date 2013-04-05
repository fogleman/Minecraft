import os
import cPickle as pickle

def get_default_filename(game_dir):
  return os.path.join(game_dir, 'save.dat')

def save_world(window, game_dir, filename=None):
  filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
  pickle.dump((window.model.world, window.model.sectors, window.strafe,
                         window.player, window.time_of_day),
                        open(filename, "wb"))

def world_exists(game_dir, filename):
  return os.path.lexists(os.path.join(game_dir, filename))

def open_world(game_dir, filename=None):
  filename = os.path.join(game_dir, filename) if filename else get_default_filename(game_dir)
  return pickle.load(open(filename, "rb"))
