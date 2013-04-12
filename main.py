from ConfigParser import NoSectionError, NoOptionError
import argparse
from binascii import hexlify
import datetime
import os
import random
import time

import pyglet
# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
from pyglet.gl import *

#import kytten
from blocks import *
import globals
from savingsystem import *
from controllers import *


def safe_add_to_config(section, option, default_value):
    try:
        user_value = globals.config.get(section, option)
    except NoSectionError:
        globals.config.add_section(section)
    except NoOptionError:
        pass
    else:
        # If no exception (meaning that the option is already set), do nothing.
        return user_value
    globals.config.set(section, option, default_value)
    return default_value


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


def initialize_config():
    safe_add_to_config('World', 'flat', 'false')  # dont make mountains, make a flat world
    safe_add_to_config('World', 'size', '64')
    safe_add_to_config('World', 'show_fog', 'true')

    # Adds missing keys to configuration file and converts to pyglet keys.
    for control, default_key_name in globals.KEY_BINDINGS.items():
        key_name = safe_add_to_config('Controls', control, default_key_name)
        try:
            pyglet_key = get_key(key_name)
        except InvalidKey:
            pyglet_key = get_key(default_key_name)
            globals.config.set('Controls', control, default_key_name)
        setattr(globals, control.upper() + '_KEY', pyglet_key)

    with open(globals.config_file, 'wb') as handle:
        globals.config.write(handle)


class Window(pyglet.window.Window):
    def __init__(self, width, height, launch_fullscreen=False, show_gui=True,**kwargs):
        super(Window, self).__init__(width, height, **kwargs)
        self.exclusive = False
        self.reticle = None
        self.controller = None
        controller = MainMenuController(self, show_gui=show_gui)
        self.switch_controller(controller)
        if launch_fullscreen:
            self.set_fullscreen()
        pyglet.clock.schedule_interval(self.update, 1.0 / globals.MAX_FPS)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def update(self, dt):
        self.controller.update(dt)
        
    def switch_controller(self, new_controller):
        if self.controller:
            self.controller.pop_handlers()
        self.controller = new_controller
        self.controller.push_handlers()

    def on_key_press(self, symbol, modifiers):
        if self.exclusive:
            if symbol == globals.ESCAPE_KEY and not self.fullscreen:
                self.set_exclusive_mouse(False)
            elif symbol == key.Q and self.fullscreen:  # FIXME: Better fullscreen mode.
                pyglet.app.exit()  # for fullscreen

    def on_draw(self):
        if self.exclusive:
            self.reticle.draw(GL_LINES)
            if globals.MOTION_BLUR:
                glAccum(GL_MULT, 0.65)
                glAccum(GL_ACCUM, 0.35)
                glAccum(GL_RETURN, 1.0)
        pyglet.clock.tick()

    def on_resize(self, width, height):
        if self.reticle:
            self.reticle.delete()
        x, y = width / 2, height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(
            4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )


def main(options):
    globals.GAME_MODE = options.game_mode
    globals.SAVE_FILENAME = options.save
    globals.MOTION_BLUR = options.motion_blur
    globals.DISABLE_SAVE = options.disable_save
    for name, val in options._get_kwargs():
        setattr(globals.LAUNCH_OPTIONS, name, val)

    globals.DRAW_DISTANCE = globals.DRAW_DISTANCE_CHOICES[options.draw_distance]

    globals.TERRAIN_CHOICE = options.terrain
    globals.TERRAIN = globals.TERRAIN_CHOICES[options.terrain]

    if options.flat:
        safe_add_to_config('World', 'flat', 'true')

    if options.fast:
        globals.TIME_RATE /= 20

    seed = options.seed
    if seed is None:
        # Generates pseudo-random number.
        try:
            seed = long(hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            import time
            seed = long(time.time() * 256)  # use fractional seconds
        # Then convert it to a string so all seeds have the same type.
        seed = str(seed)

        print('Random seed: ' + seed)

    random.seed(seed)

    with open(os.path.join(globals.game_dir, 'seeds.txt'), 'a') as seeds:
        seeds.write(datetime.datetime.now().strftime(
            'Seed used the %d %m %Y at %H:%M:%S\n'))
        seeds.write('%s\n\n' % seed)

    # try:
        # window_config = Config(sample_buffers=1, samples=4) #, depth_size=8)  #, double_buffer=True) #TODO Break anti-aliasing/multisampling into an explicit menu option
        # window = Window(show_gui=options.show_gui, width=options.width, height=options.height, caption='pyCraftr', resizable=True, config=window_config, save=save_object)
    # except pyglet.window.NoSuchConfigException:
    window = Window(
        options.width, options.height, launch_fullscreen=options.fullscreen,
        show_gui=options.show_gui, caption=globals.APP_NAME, resizable=True,
        vsync=False)

    pyglet.clock.set_fps_limit(globals.MAX_FPS)
    pyglet.app.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a Python made Minecraft clone.')

    display_group = parser.add_argument_group('Display options')
    display_group.add_argument("--width", type=int, default=globals.WINDOW_WIDTH, help="Set the window width.")
    display_group.add_argument("--height", type=int, default=globals.WINDOW_HEIGHT, help="Set the window height.")
    display_group.add_argument("--show-gui", action="store_true", default=True, help="Enabled by default.")
    display_group.add_argument("--draw-distance", choices=globals.DRAW_DISTANCE_CHOICES, default=globals.DEFAULT_DRAW_DISTANCE_CHOICE, help="How far to draw the map.")
    display_group.add_argument("--fullscreen", action="store_true", default=False, help="Runs the game in fullscreen. Press 'Q' to exit the game.")
    
    game_group = parser.add_argument_group('Game options')
    game_group.add_argument("--terrain", choices=globals.TERRAIN_CHOICES, default=globals.DEFAULT_TERRAIN_CHOICE)
    game_group.add_argument("--flat", action="store_true", default=False, help="Generate a flat world.")
    game_group.add_argument("--fast", action="store_true", default=False, help="Makes time progress faster then normal.")
    game_group.add_argument("--game-mode", choices=globals.GAME_MODE_CHOICES, default=globals.GAME_MODE)

    save_group = parser.add_argument_group('Save options')
    save_group.add_argument("--disable-auto-save", action="store_false", default=True, help="Do not save world on exit.")
    save_group.add_argument("--save", default=globals.SAVE_FILENAME, help="Type a name for the world to be saved as.")
    save_group.add_argument("--disable-save", action="store_false", default=True, help="Disables saving.")
    save_group.add_argument("--save-mode", choices=globals.SAVE_MODES, default=globals.SAVE_MODE, help="Flatfile Struct (flatfile) is the smallest and fastest")

    parser.add_argument("--seed", default=None)
    parser.add_argument("--motion-blur", action="store_true", default=False)

    options = parser.parse_args()
    initialize_config()
    main(options)
