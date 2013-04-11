import argparse
from binascii import hexlify
import datetime
import operator
import os
import cPickle as pickle
import random
import time

import pyglet
# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.window import key

#import kytten
from blocks import *
import globals
from savingsystem import *
from controllers import *

terrain_options = {
    'plains': ('0', '2', '700'),  # type, hill_height, max_trees
    'mountains': ('5', '12', '4000'),
    'desert': ('2', '5', '50'),
    'island': ('3', '8', '700'),
    'snow': ('6', '4', '1500')
}

config_file = os.path.join(globals.game_dir, 'game.cfg')
if not os.path.lexists(config_file):
    type, hill_height, max_trees = terrain_options['plains']
    globals.config.add_section('World')
    globals.config.set('World', 'type', str(type))  # 0=plains,1=dirt,2=desert,3=islands,4=sand,5=stone,6=snow
    globals.config.set('World', 'hill_height', str(hill_height))  # height of the hills
    globals.config.set('World', 'flat', 'false')  # dont make mountains, make a flat world
    globals.config.set('World', 'size', '64')
    globals.config.set('World', 'show_fog', 'true')
    globals.config.set('World', 'max_trees', str(max_trees))

    globals.config.add_section('Controls')
    globals.config.set('Controls', 'move_forward', str(key.W))
    globals.config.set('Controls', 'move_backward', str(key.S))
    globals.config.set('Controls', 'move_left', str(key.A))
    globals.config.set('Controls', 'move_right', str(key.D))
    globals.config.set('Controls', 'jump', str(key.SPACE))
    globals.config.set('Controls', 'inventory', str(key.E))
    globals.config.set('Controls', 'sound_up', str(key.PAGEUP))
    globals.config.set('Controls', 'sound_down', str(key.PAGEDOWN))

    try:
        with open(config_file, 'wb') as handle:
            globals.config.write(handle)
    except:
        print "Problem: Configuration file (%s) doesn't exist." % config_file
        sys.exit(1)
else:
    globals.config.read(config_file)

####

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
            if symbol == key.ESCAPE and not self.fullscreen:
                self.set_exclusive_mouse(False)
            elif symbol == key.Q and self.fullscreen:
                pyglet.app.exit() # for fullscreen

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

    if options.draw_distance == 'medium':
        globals.DRAW_DISTANCE = 60.0 * 1.5
    elif options.draw_distance == 'long':
        globals.DRAW_DISTANCE = 60.0 * 2.0

    if options.terrain:
        type, hill_height, max_trees = terrain_options[options.terrain]
        globals.config.set('World', 'type', type)
        globals.config.set('World', 'hill_height', hill_height)
        globals.config.set('World', 'max_trees', max_trees)

    if options.flat:
        globals.config.set('World', 'flat', 'true')

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
    if options.save_config:
        try:
            with open(config_file, 'wb') as handle:
                globals.config.write(handle)
        except:
            print "Problem: Write error."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a Python made Minecraft clone.')
    
    display_group = parser.add_argument_group('Display options')
    display_group.add_argument("--width", type=int, default=850, help="Set the window width.")
    display_group.add_argument("--height", type=int, default=480, help="Set the window height.")
    display_group.add_argument("--show-gui", action="store_true", default=True, help="Enabled by default.")
    display_group.add_argument("--draw-distance", choices=['short', 'medium', 'long'], default='short', help=" How far to draw the map. Choose short, medium or long.")
    display_group.add_argument("--fullscreen", action="store_true", default=False, help="Runs the game in fullscreen. Press 'Q' to exit the game.")
    
    game_group = parser.add_argument_group('Game options')
    game_group.add_argument("--terrain", choices=terrain_options.keys(), help="Different terrains. Choose grass, island, mountains,desert, plains")
    game_group.add_argument("--flat", action="store_true", default=False, help="Generate a flat world.")
    game_group.add_argument("--fast", action="store_true", default=False, help="Makes time progress faster then normal.")
    game_group.add_argument("--game-mode", choices=('survival', 'creative'), default=globals.GAME_MODE, help="Sets the game mode.")

    save_group = parser.add_argument_group('Save options')
    save_group.add_argument("--disable-auto-save", action="store_false", default=True, help="Do not save world on exit.")
    save_group.add_argument("--save", type=unicode, default=globals.SAVE_FILENAME, help="Type a name for the world to be saved as.")
    save_group.add_argument("--disable-save", action="store_false", default=True, help="Disables saving.")
    save_group.add_argument("--save-config", action="store_true", default=False, help="Saves the choices as the default config.")
    save_group.add_argument("--save-mode", type=int, default=2, help="0 = Uncompressed Pickle, 1 = Compressed Pickle, 2 = Flatfile Struct (smallest, fastest)")

    parser.add_argument("--seed", default=None)
    parser.add_argument("--motion-blur", action="store_true", default=False)
    options = parser.parse_args()
    main(options)
