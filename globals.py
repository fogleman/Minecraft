from math import pi


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
HOUR_DEG = 15.0
BACK_RED = 0.0  # 0.53
BACK_GREEN = 0.0  # 0.81
BACK_BLUE = 0.0  # 0.98
HALF_PI = pi / 2.0  # 90 degrees
SPREADING_MUTATION_DELAY = 10  # in seconds
TERRAINMAP_BLOCK_SIZE = 8
