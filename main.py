#!/usr/bin/env python

# Imports, sorted alphabetically.

# Python packages
from ConfigParser import NoSectionError, NoOptionError
import argparse
import os
import random
import time

# Third-party packages
import pyglet
# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
from pyglet.gl import *

# Modules from this project
from controllers import *
import globals as G
from timer import Timer


class InvalidChoice(Exception):
    pass


def get_or_update_config(section, option, default_value, conv=str, choices=()):
    try:
        if conv is bool:
            user_value = G.config.getboolean(section, option)
        else:
            user_value = conv(G.config.get(section, option))
    except NoSectionError:
        G.config.add_section(section)
    except NoOptionError:
        pass
    else:
        # If the option is already set:
        if choices and user_value not in choices:
            raise InvalidChoice('%s.%s must be in %s' %
                                (section, option, repr(tuple(choices))))
        return user_value
    G.config.set(section, option, str(default_value))
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
    #
    # General
    #

    general = 'General'

    G.DEBUG = get_or_update_config(
        general, 'debug', G.DEBUG, conv=bool)

    get_or_update_config(
        general, 'save_mode', G.SAVE_MODE, choices=G.SAVE_MODES)

    #
    # Graphics
    #

    graphics = 'Graphics'

    G.FULLSCREEN = get_or_update_config(
        graphics, 'fullscreen', G.FULLSCREEN, conv=bool)
    G.WINDOW_WIDTH = get_or_update_config(
        graphics, 'width', G.WINDOW_WIDTH, conv=int)
    G.WINDOW_HEIGHT = get_or_update_config(
        graphics, 'height', G.WINDOW_HEIGHT, conv=int)

    G.DRAW_DISTANCE_CHOICE = get_or_update_config(
        graphics, 'draw_distance', G.DRAW_DISTANCE_CHOICE,
        choices=G.DRAW_DISTANCE_CHOICES)
    G.DRAW_DISTANCE = G.DRAW_DISTANCE_CHOICES[G.DRAW_DISTANCE_CHOICE]

    G.FOG_ENABLED = get_or_update_config(
        graphics, 'fog_enabled', G.FOG_ENABLED, conv=bool)

    G.MOTION_BLUR = get_or_update_config(
        graphics, 'motion_blur', G.MOTION_BLUR, conv=bool)

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
    for control, default_key_name in G.KEY_BINDINGS.items():
        key_name = get_or_update_config(controls, control, default_key_name)
        try:
            pyglet_key = get_key(key_name)
        except InvalidKey:
            pyglet_key = get_key(default_key_name)
            G.config.set(controls, control, default_key_name)
        setattr(G, control.upper() + '_KEY', pyglet_key)

    #
    # Save config file
    #

    with open(G.config_file, 'wb') as handle:
        G.config.write(handle)


class Window(pyglet.window.Window):
    def __init__(self, **kwargs):
        kwargs.update(
            caption=G.APP_NAME,
        )
        super(Window, self).__init__(
            G.WINDOW_WIDTH, G.WINDOW_HEIGHT, **kwargs)
        self.exclusive = False
        self.reticle = None
        self.controller = None
        controller = MainMenuController(self)
        self.switch_controller(controller)
        if G.FULLSCREEN:
            self.set_fullscreen()
        self.total_fps = 0.0
        self.iterations = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / G.MAX_FPS)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def update(self, dt):
        self.controller.update(dt)
        self.total_fps += pyglet.clock.get_fps()
        self.iterations += 1

    def switch_controller(self, new_controller):
        if self.controller:
            self.controller.pop_handlers()
        self.controller = new_controller
        self.controller.push_handlers()

    def on_key_press(self, symbol, modifiers):
        if self.exclusive:
            if symbol == G.ESCAPE_KEY and not self.fullscreen:
                self.set_exclusive_mouse(False)
            elif symbol == key.Q and self.fullscreen:  # FIXME: Better fullscreen mode.
                pyglet.app.exit()  # for fullscreen

    def on_draw(self):
        if self.exclusive:
            self.reticle.draw(GL_LINES)
            if G.MOTION_BLUR:
                glAccum(GL_MULT, 0.65)
                glAccum(GL_ACCUM, 0.35)
                glAccum(GL_RETURN, 1.0)

    def on_resize(self, width, height):
        if self.reticle:
            self.reticle.delete()
        x, y = width / 2, height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(
            4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def on_close(self):
        print('Average FPS: %f' % (self.total_fps / self.iterations))
        super(Window, self).on_close()


def main(options):
    G.GAME_MODE = options.game_mode
    G.SAVE_FILENAME = options.save
    G.DISABLE_SAVE = options.disable_save
    for name, val in options._get_kwargs():
        setattr(G.LAUNCH_OPTIONS, name, val)

    G.TERRAIN_CHOICE = options.terrain
    G.TERRAIN = G.TERRAIN_CHOICES[options.terrain]

    G.FLAT_MODE = options.flat

    if options.fast:
        G.TIME_RATE /= 20

    # try:
        # window_config = Config(sample_buffers=1, samples=4) #, depth_size=8)  #, double_buffer=True) #TODO Break anti-aliasing/multisampling into an explicit menu option
        # window = Window(resizable=True, config=window_config)
    # except pyglet.window.NoSuchConfigException:
    window = Window(resizable=True, vsync=False)

    G.main_timer = Timer()
    pyglet.clock.schedule_interval(G.main_timer.schedule, G.TIMER_INTERVAL)
    pyglet.app.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a Python made Minecraft clone.')

    game_group = parser.add_argument_group('Game options')
    game_group.add_argument("--terrain", choices=G.TERRAIN_CHOICES, default=G.DEFAULT_TERRAIN_CHOICE)
    game_group.add_argument("--flat", action="store_true", default=False, help="Generate a flat world.")
    game_group.add_argument("--fast", action="store_true", default=False, help="Makes time progress faster then normal.")
    game_group.add_argument("--game-mode", choices=G.GAME_MODE_CHOICES, default=G.GAME_MODE)

    save_group = parser.add_argument_group('Save options')
    save_group.add_argument("--disable-auto-save", action="store_false", default=True, help="Do not save world on exit.")
    save_group.add_argument("--save", default=G.SAVE_FILENAME, help="Type a name for the world to be saved as.")
    save_group.add_argument("--disable-save", action="store_false", default=True, help="Disables saving.")

    parser.add_argument("--seed", default=None)

    options = parser.parse_args()
    initialize_config()
    main(options)
