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
from globals import *
from savingsystem import *
from controllers import *

terrain_options = {
    'plains': ('0', '2', '700'),  # type, hill_height, max_trees
    'mountains': ('5', '12', '4000'),
    'desert': ('2', '5', '50'),
    'island': ('3', '8', '700'),
    'snow': ('6', '4', '1500')
}

config_file = os.path.join(game_dir, 'game.cfg')
if not os.path.lexists(config_file):
    type, hill_height, max_trees = terrain_options['plains']
    config.add_section('World')
    config.set('World', 'type', str(type))  # 0=plains,1=dirt,2=desert,3=islands,4=sand,5=stone,6=snow
    config.set('World', 'hill_height', str(hill_height))  # height of the hills
    config.set('World', 'flat', '0')  # dont make mountains,  make a flat world
    config.set('World', 'size', '160')
    config.set('World', 'show_fog', '1')
    config.set('World', 'max_trees', str(max_trees))

    config.add_section('Controls')
    config.set('Controls', 'move_forward', str(key.W))
    config.set('Controls', 'move_backward', str(key.S))
    config.set('Controls', 'move_left', str(key.A))
    config.set('Controls', 'move_right', str(key.D))
    config.set('Controls', 'jump', str(key.SPACE))
    config.set('Controls', 'inventory', str(key.E))
    config.set('Controls', 'sound_up', str(key.PAGEUP))
    config.set('Controls', 'sound_down', str(key.PAGEDOWN))

    try:
        with open(config_file, 'wb') as handle:
            config.write(handle)
    except:
        print "Problem: Configuration file (%s) doesn't exist." % config_file
        sys.exit(1)
else:
    config.read(config_file)

####

class Window(pyglet.window.Window):
    def __init__(self, width, height, launch_fullscreen=False, show_gui=True, save=None, **kwargs):
        super(Window, self).__init__(width, height, **kwargs)
        self.exclusive = False
        self.reticle = None
        self.controller = None
        #self.controller = GameController(self, show_gui=show_gui, save=save)
        controller = MainMenuController(self, show_gui=show_gui, save=save)
        self.switch_controller(controller)
        if launch_fullscreen:
            self.set_fullscreen()
        pyglet.clock.schedule_interval(self.update, 1.0 / MAX_FPS)

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
            glColor3d(0, 0, 0)
            self.reticle.draw(GL_LINES)
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
    save_object = None
    global SAVE_FILENAME
    global DISABLE_SAVE
    global DRAW_DISTANCE
    global GAMEMODE
    GAMEMODE = options.gamemode
    SAVE_FILENAME = options.save
    DISABLE_SAVE = options.disable_save
    if options.disable_save and world_exists(game_dir, SAVE_FILENAME):
        save_object = open_world(game_dir, SAVE_FILENAME)
    if options.draw_distance == 'medium':
        DRAW_DISTANCE = 60.0 * 1.5
    elif options.draw_distance == 'long':
        DRAW_DISTANCE = 60.0 * 2.0

    if options.terrain:
        type, hill_height, max_trees = terrain_options[options.terrain]
        config.set('World', 'type', type)
        config.set('World', 'hill_height', hill_height)
        config.set('World', 'max_trees', max_trees)

    if options.hillheight:
        config.set('World', 'hill_height', str(options.hillheight))

    if options.worldsize:
        config.set('World', 'size', str(options.worldsize))

    if options.flat:
        config.set('World', 'flat', '1')

    if options.maxtrees:
        config.set('World', 'max_trees', str(options.maxtrees))

    if options.hide_fog:
        config.set('World', 'show_fog', '0')

    global TIME_RATE

    if options.fast:
        TIME_RATE /= 20

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

    with open(os.path.join(game_dir, 'seeds.txt'), 'a') as seeds:
        seeds.write(datetime.datetime.now().strftime(
            'Seed used the %d %m %Y at %H:%M:%S\n'))
        seeds.write('%s\n\n' % seed)

    # try:
        # window_config = Config(sample_buffers=1, samples=4) #, depth_size=8)  #, double_buffer=True) #TODO Break anti-aliasing/multisampling into an explicit menu option
        # window = Window(show_gui=options.show_gui, width=options.width, height=options.height, caption='pyCraftr', resizable=True, config=window_config, save=save_object)
    # except pyglet.window.NoSuchConfigException:
    window = Window(options.width, options.height, launch_fullscreen=options.fullscreen,
        show_gui=options.show_gui, save=save_object, caption=APP_NAME, resizable=True, vsync=False)

    pyglet.clock.set_fps_limit(MAX_FPS)
    pyglet.app.run()
    if options.disable_auto_save and options.disable_save:
        window.controller.save_to_file(compression=not options.nocompression)
    if options.save_config:
        try:
            with open(config_file, 'wb') as handle:
                config.write(handle)
        except:
            print "Problem: Write error."



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a Python made Minecraft clone.')
    
    display_group = parser.add_argument_group('Display options')
    display_group.add_argument("-width", type=int, default=850, help = "Set the window width.")
    display_group.add_argument("-height", type=int, default=480, help = "Set the window height.")
    display_group.add_argument("--show-gui", action="store_true", default=True, help = "Enabled by default.")
    display_group.add_argument("--hide-fog", action="store_true", default=False, help ="Hides the fog, see the whole landscape.")
    display_group.add_argument("-draw-distance", choices=['short', 'medium', 'long'], default='short', help =" How far to draw the map. Choose short, medium or long.")
    display_group.add_argument("-fullscreen", action="store_true", default=False, help = "Runs the game in fullscreen. Press 'Q' to exit the game.")
    
    game_group = parser.add_argument_group('Game options')
    game_group.add_argument("-terrain", choices=terrain_options.keys(), help = "Different terains. Choose grass, island, mountains,desert, plains")
    game_group.add_argument("-hillheight", type=int, help = "How high the hills are.")
    game_group.add_argument("-worldsize", type=int, help = "The width size of the world.")
    game_group.add_argument("-maxtrees", type=int, help = "How many trees and cacti should be made.")
    game_group.add_argument("--flat", action="store_true", default=False, help = "Generate a flat world.")
    game_group.add_argument("--fast", action="store_true", default=False, help = "Makes time progress faster then normal.")
    game_group.add_argument("-gamemode", type=int, default=1, help = "Set the Gamemode for player.  0 = Creative, 1 = Survival")
    
    save_group = parser.add_argument_group('Save options')
    save_group.add_argument("--disable-auto-save", action="store_false", default=True, help = "Do not save world on exit.")
    save_group.add_argument("-save", type=unicode, default=SAVE_FILENAME, help = "Type a name for the world to be saved as.")
    save_group.add_argument("--disable-save", action="store_false", default=True, help = "Disables saving.")
    save_group.add_argument("--save-config", action="store_true", default=False, help = "Saves the choices as the default config.")
    save_group.add_argument("-nocompression", action="store_true", default=False, help = "Disables compression for a smaller save file.")
    
    parser.add_argument("-seed", default=None)
    options = parser.parse_args()
    main(options)
