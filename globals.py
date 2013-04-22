"""
Global variables.

WARNING: Never use `from globals import *`!
Since these global variables are modified during runtime, using `import *`
would lead to unpredictable consequences.
"""

# Imports, sorted alphabetically.

# Python packages
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
import argparse
from math import pi
import os

# Third-party packages
import pyglet
from pyglet.resource import get_settings_path

# Modules from this project
# Nothing for now...


APP_NAME = 'pyCraftr'  # should I stay or should I go?

DEBUG = False


#
# Game modes
#

SURVIVAL_MODE = 'survival'
CREATIVE_MODE = 'creative'
GAME_MODE_CHOICES = (SURVIVAL_MODE, CREATIVE_MODE)
GAME_MODE = CREATIVE_MODE

FLAT_MODE = False


#
# User input
#

# Movement
MOVE_FORWARD_KEY = 'W'
MOVE_BACKWARD_KEY = 'S'
MOVE_LEFT_KEY = 'A'
MOVE_RIGHT_KEY = 'D'
JUMP_KEY = 'SPACE'
CROUCH_KEY = 'LSHIFT'
FLY_KEY = 'TAB'

# Action
INVENTORY_KEY = 'E'
INVENTORY_SORT_KEY = 'M'
INVENTORY_1_KEY = '1'
INVENTORY_2_KEY = '2'
INVENTORY_3_KEY = '3'
INVENTORY_4_KEY = '4'
INVENTORY_5_KEY = '5'
INVENTORY_6_KEY = '6'
INVENTORY_7_KEY = '7'
INVENTORY_8_KEY = '8'
INVENTORY_9_KEY = '9'
INVENTORY_10_KEY = '0'
TALK_KEY = 'T'
VALIDATE_KEY = 'ENTER'

# Settings
SOUND_UP_KEY = 'PAGEUP'
SOUND_DOWN_KEY = 'PAGEDOWN'
TOGGLE_HUD_KEY = 'F3'
SCREENCAP_KEY = 'F2'

# Various
SAVE_KEY = 'V'
ESCAPE_KEY = 'ESCAPE'

KEY_BINDINGS = dict(
    (k.lower()[:-4], v) for k, v in locals().items() if k[-4:] == '_KEY'
)


#
# Saves
#

DISABLE_SAVE = True
SAVE_FILENAME = None

PICKLE_SAVE_MODE = 'pickle'
PICKLE_COMPRESSED_SAVE_MODE = 'pickle_compressed'
FLATFILE_SAVE_MODE = 'flatfile'
REGION_SAVE_MODE = 'region'
SAVE_MODES = (
    PICKLE_SAVE_MODE, PICKLE_COMPRESSED_SAVE_MODE, FLATFILE_SAVE_MODE, REGION_SAVE_MODE
)
SAVE_MODE = REGION_SAVE_MODE


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

VERTEX_CUBE = 'cube'
VERTEX_CROSS = 'cross'
VERTEX_GRID = 'grid'
VERTEX_MODES = (
    VERTEX_CUBE,
    VERTEX_CROSS,
    VERTEX_GRID,
)

# items and blocks share a common id table
# ids of items should be >= ITEM_ID_MIN
ITEM_ID_MIN = 256

TIME_RATE = 240 * 10  # Rate of change (steps per hour).
SPREADING_MUTATION_DELAY = 4  # in seconds


#
# Terrain generation
#

TERRAIN_CHOICES = {  # hill_height & max_trees mandatory for the moment.
    'plains': {
        'hill_height': 2,
        'max_trees': 700,
    },
    'desert': {
        'hill_height': 5,
        'max_trees': 50,
    },
    'island': {
        'hill_height': 8,
        'max_trees': 700,
    },
    'mountains': {
        'hill_height': 12,
        'max_trees': 4000,
    },
    'snow': {
        'hill_height': 4,
        'max_trees': 1500,
    }
}
DEFAULT_TERRAIN_CHOICE = 'plains'
TERRAIN_CHOICE = DEFAULT_TERRAIN_CHOICE
TERRAIN = TERRAIN_CHOICES[DEFAULT_TERRAIN_CHOICE]

SEED = None
TREE_CHANCE = 0.006
WILDFOOD_CHANCE = 0.0005
GRASS_CHANCE = 0.05
#
# Biome
#
DESERT, PLAINS, MOUNTAINS, SNOW, FOREST = range(5)
OLD_BIOME = DEFAULT_TERRAIN_CHOICE
NEW_BIOME = 'plains'
# THE LARGER THE NUMBER, THE MORE TO WALK TO  ANEW BIOME
BIOME_BLOCK_TRIGGER = 80
BIOME_NEGATIVE_BLOCK_TRIGGER = -80
BIOME_BLOCK_COUNT = 0
#
# Graphical rendering
#

FULLSCREEN = False
WINDOW_WIDTH = 850  # Screen width (in pixels)
WINDOW_HEIGHT = 480  # Screen height (in pixels)

MAX_FPS = 60  # Maximum frames per second.
QUEUE_PROCESS_SPEED = 0.3 / MAX_FPS #Try shrinking this if chunk loading is laggy, higher loads chunks faster

VISIBLE_SECTORS_RADIUS = 8
DELOAD_SECTORS_RADIUS = 16

DRAW_DISTANCE_CHOICES = {
    'short': 60.0,
    'medium': 60.0 * 1.5,
    'long': 60.0 * 2.0
}
DEFAULT_DRAW_DISTANCE_CHOICE = 'short'
DRAW_DISTANCE_CHOICE = DEFAULT_DRAW_DISTANCE_CHOICE
DRAW_DISTANCE = DRAW_DISTANCE_CHOICES[DRAW_DISTANCE_CHOICE]

FOV = 65.0  # TODO: add menu option to change FOV
NEAR_CLIP_DISTANCE = 0.1  # TODO: make min and max clip distance dynamic
FAR_CLIP_DISTANCE = 200.0  # Maximum render distance,
                           # ignoring effects of sector_size

MOTION_BLUR = False

TEXTURE_PACK = 'default'

HUD_ENABLED = True


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
# Recipes
#

recipes = None
smelting_recipes = None


#
# Timer
#

TIMER_INTERVAL = 1
main_timer = None

#
# Global files & directories
#

game_dir = get_settings_path(APP_NAME)
if not os.path.exists(game_dir):
    os.makedirs(game_dir)

config = ConfigParser()
config_file = os.path.join(game_dir, 'game.cfg')
config.read(config_file)
LAUNCH_OPTIONS = argparse.Namespace()

ANCHOR_NONE   = 0
ANCHOR_LEFT   = 1
ANCHOR_TOP    = 1 << 1
ANCHOR_RIGHT  = 1 << 2
ANCHOR_BOTTOM = 1 << 3

ICONS_PATH = os.path.join('resources', 'textures', 'icons')
TEXTURES_PATH = os.path.join('resources', 'textures')
DEFAULT_FONT = 'ChunkFive Roman'


class InvalidChoice(Exception):
    pass


class InvalidKey(Exception):
    pass


def get_key(key_name):
    key_code = getattr(pyglet.window.key, key_name, None)
    if key_code is None:
        # Handles cases like pyglet.window.key._1
        key_code = getattr(pyglet.window.key, '_' + key_name, None)
        if key_code is None:
            raise InvalidKey('%s is not a valid key.' % key_name)
    return key_code
    

def get_or_update_config(section, option, default_value, conv=str, choices=()):
    user_value = False
    try:
        if conv is bool:
            user_value = config.getboolean(section, option)
        else:
            user_value = conv(config.get(section, option))
    except NoSectionError:
        config.add_section(section)
    except NoOptionError:
        pass
        
    if not user_value:
        user_value = default_value
    # If the option is already set:
    if choices and user_value not in choices:
        raise InvalidChoice('"%s" %s.%s must be in %s' %
                            (user_value, section, option, repr(tuple(choices))))
    config.set(section, option, str(user_value))
    return user_value


def initialize_config():
    #
    # General
    #
    global DEBUG, FULLSCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, DRAW_DISTANCE_CHOICE, DRAW_DISTANCE_CHOICES, DRAW_DISTANCE, MOTION_BLUR, TEXTURE_PACK

    general = 'General'

    DEBUG = get_or_update_config(
        general, 'debug', DEBUG, conv=bool)

    get_or_update_config(
        general, 'save_mode', SAVE_MODE, choices=SAVE_MODES)

    #
    # Graphics
    #

    graphics = 'Graphics'

    FULLSCREEN = get_or_update_config(
        graphics, 'fullscreen', FULLSCREEN, conv=bool)
    WINDOW_WIDTH = get_or_update_config(
        graphics, 'width', WINDOW_WIDTH, conv=int)
    WINDOW_HEIGHT = get_or_update_config(
        graphics, 'height', WINDOW_HEIGHT, conv=int)

    DRAW_DISTANCE_CHOICE = get_or_update_config(
        graphics, 'draw_distance', DRAW_DISTANCE_CHOICE,
        choices=DRAW_DISTANCE_CHOICES)
    DRAW_DISTANCE = DRAW_DISTANCE_CHOICES[DRAW_DISTANCE_CHOICE]

    MOTION_BLUR = get_or_update_config(
        graphics, 'motion_blur', MOTION_BLUR, conv=bool)

    TEXTURE_PACK = get_or_update_config(
        graphics, 'texture_pack', TEXTURE_PACK, conv=str)

    #
    # World
    #

    world = 'World'

    # TODO: This setting must be removed when terrain generation will improve.
    get_or_update_config(world, 'size', 64, conv=int)

    #
    # Controls
    #

    controls = 'Controls'

    # Adds missing keys to configuration file and converts to pyglet keys.
    for control, default_key_name in KEY_BINDINGS.items():
        key_name = get_or_update_config(controls, control, default_key_name)
        try:
            pyglet_key = get_key(key_name)
        except InvalidKey:
            pyglet_key = get_key(default_key_name)
            config.set(controls, control, default_key_name)
        globals()[control.upper() + '_KEY'] = pyglet_key

    #
    # Save config file
    #

    with open(config_file, 'wb') as handle:
        config.write(handle)

initialize_config()
