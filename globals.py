from math import pi
from pyglet.resource import get_settings_path
import os
from ConfigParser import ConfigParser
import argparse

APP_NAME = 'pyCraftr'  # should I stay or should I go?

SECTOR_SIZE = 8
VISIBLE_SECTORS_RADIUS = 8
DRAW_DISTANCE = 60.0
FOV = 65.0  # TODO: add menu option to change FOV
NEAR_CLIP_DISTANCE = 0.1  # TODO: make min and max clip distance dynamic
FAR_CLIP_DISTANCE = 200.0  # Maximum render distance,
                           # ignoring effects of sector_size and fog
DISABLE_SAVE = True
TIME_RATE = 240 * 10  # Rate of change (steps per hour).
MAX_FPS = 60  # Maximum frames per second.
DEG_RAD = pi / 180.0
HALF_PI = pi / 2.0  # 90 degrees
SPREADING_MUTATION_DELAY = 4  # in seconds
TILESET_SIZE = 16  # The tileset therefore contains TILESET_SIZE ** 2 tiles.
GAMEMODE = 0 #0 = creative (no damage), 1 = Survival (take Damage

EFFECT_VOLUME = 1
MOTION_BLUR = False

SAVE_FILENAME = None

# Tool type
WOODEN_TOOL, STONE_TOOL, IRON_TOOL, DIAMOND_TOOL, GOLDEN_TOOL = range(5)
PICKAXE, AXE, SHOVEL, HOE, SWORD = range(5)
HELMET, CHESTPLATE, LEGGINGS, BOOTS = range(4)

config = ConfigParser()
LAUNCH_OPTIONS = argparse.Namespace()

game_dir = get_settings_path(APP_NAME)
if not os.path.exists(game_dir):
    os.makedirs(game_dir)
