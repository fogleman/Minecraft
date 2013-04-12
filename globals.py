"""
Global variables.

WARNING: Never use `from globals import *`!
Since these global variables are modified during runtime, using `import *`
would lead to unpredictable consequences.
"""

# Python packages
import argparse
from ConfigParser import ConfigParser
from math import pi
import os
# Third-party packages
from pyglet.resource import get_settings_path


APP_NAME = 'pyCraftr'  # should I stay or should I go?


#
# Game modes
#

SURVIVAL_MODE = 'survival'
CREATIVE_MODE = 'creative'
GAME_MODE_CHOICES = (SURVIVAL_MODE, CREATIVE_MODE)
GAME_MODE = CREATIVE_MODE


#
# Saves
#

DISABLE_SAVE = True
SAVE_FILENAME = None

PICKLE_SAVE_MODE = 'pickle'
PICKLE_COMPRESSED_SAVE_MODE = 'pickle_compressed'
FLATFILE_SAVE_MODE = 'flatfile'
SAVE_MODES = (
    PICKLE_SAVE_MODE, PICKLE_COMPRESSED_SAVE_MODE, FLATFILE_SAVE_MODE
)
SAVE_MODE = FLATFILE_SAVE_MODE


#
# Game engine
#

SECTOR_SIZE = 8
TILESET_SIZE = 16  # The tileset therefore contains TILESET_SIZE ** 2 tiles.


#
# Game logic
#

BLOCKS_DIR = {}  # Block ID => block object
ITEMS_DIR = {}  # Item ID => item object
TIME_RATE = 240 * 10  # Rate of change (steps per hour).
SPREADING_MUTATION_DELAY = 4  # in seconds


#
# Terrain generation
#

TERRAIN_CHOICES = {
    'plains': {
        'hill_height': '2',
        'max_trees': '700',
    },
    'desert': {
        'hill_height': '5',
        'max_trees': '50',
    },
    'island': {
        'hill_height': '8',
        'max_trees': '700',
    },
    'mountains': {
        'hill_height': '12',
        'max_trees': '4000',
    },
    'snow': {
        'hill_height': '4',
        'max_trees': '1500',
    }
}
DEFAULT_TERRAIN_CHOICE = 'plains'


#
# Graphical rendering
#

WINDOW_WIDTH = 850  # Screen width (in pixels)
WINDOW_HEIGHT = 480  # Screen height (in pixels)

MAX_FPS = 60  # Maximum frames per second.

VISIBLE_SECTORS_RADIUS = 8

DRAW_DISTANCE_CHOICES = {
    'short': 60.0,
    'medium': 60.0 * 1.5,
    'long': 60.0 * 2.0
}
DEFAULT_DRAW_DISTANCE_CHOICE = 'short'
DRAW_DISTANCE = DRAW_DISTANCE_CHOICES[DEFAULT_DRAW_DISTANCE_CHOICE]

FOV = 65.0  # TODO: add menu option to change FOV
NEAR_CLIP_DISTANCE = 0.1  # TODO: make min and max clip distance dynamic
FAR_CLIP_DISTANCE = 200.0  # Maximum render distance,
                           # ignoring effects of sector_size and fog

MOTION_BLUR = False


#
# Sound
#

EFFECT_VOLUME = 1


#
# Tool types
#

WOODEN_TOOL, STONE_TOOL, IRON_TOOL, DIAMOND_TOOL, GOLDEN_TOOL = range(5)
PICKAXE, AXE, SHOVEL, HOE, SWORD = range(5)
HELMET, CHESTPLATE, LEGGINGS, BOOTS = range(4)


#
# Static aliases
#

DEG_RAD = pi / 180.0
HALF_PI = pi / 2.0  # 90 degrees


#
# Global files & directories
#

config = ConfigParser()
LAUNCH_OPTIONS = argparse.Namespace()

game_dir = get_settings_path(APP_NAME)
if not os.path.exists(game_dir):
    os.makedirs(game_dir)
