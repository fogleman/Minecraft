import argparse
from binascii import hexlify
import datetime
from math import cos, sin, atan2, pi, fmod, radians
import operator
import os
import cPickle as pickle
import random
import time
from ConfigParser import ConfigParser

import pyglet
# Disable error checking for increased performance
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.window import key

# import kytten #unused, future potential reference
from blocks import *
from entity import *
from globals import *
from gui import *
from items import *
from inventory import *
from nature import *
from world import *
from savingsystem import *

SAVE_FILENAME = None

terrain_options = {
    'plains': ('0', '2', '700'),  # type, hill_height, max_trees
    'mountains': ('5', '12', '4000'),
    'desert': ('2', '5', '50'),
    'island': ('3', '8', '700'),
    'snow': ('6', '4', '1500')
}

game_dir = pyglet.resource.get_settings_path(APP_NAME)
if not os.path.exists(game_dir):
    os.makedirs(game_dir)

config = ConfigParser()
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

    try:
        with open(config_file, 'wb') as handle:
            config.write(handle)
    except:
        print "Problem: Configuration file (%s) doesn't exist." % config_file
        sys.exit(1)
else:
    config.read(config_file)


# Define a simple function to create GLfloat arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)


class Player(Entity):
    def __init__(self, position, rotation, flying=False):
        super(Player, self).__init__(position, rotation, health=10, attack_power=0.05)
        self.inventory = Inventory()
        self.quick_slots = Inventory(9)
        self.flying = flying
        initial_items = [bookshelf_block, furnace_block, brick_block, cobble_block,
                         lamp_block, glass_block, chest_block,
                         sandstone_block, melon_block]
        for item in initial_items:
            quantity = random.randint(1, 10)
            if random.choice((True, False)):
                self.inventory.add_item(item.id, quantity)
            else:
                self.quick_slots.add_item(item.id, quantity)

    def add_item(self, item_id):
        if self.quick_slots.add_item(item_id):
            return True
        elif self.inventory.add_item(item_id):
            return True
        return False


####

class ItemSelector(object):
    def __init__(self, width, height, player, model):
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)
        self.labels_group = pyglet.graphics.OrderedGroup(2)
        self.amount_labels = []
        self.model = model
        self.player = player
        self.max_items = 9
        self.current_index = 1
        self.icon_size = self.model.group.texture.width / 8  # 4

        image = pyglet.image.load(os.path.join('resources', 'textures', 'slots.png'))
        heart_image = pyglet.image.load(os.path.join('resources', 'textures', 'heart.png'))
        frame_size = image.height / 2
        self.frame = pyglet.sprite.Sprite(
            image.get_region(0, frame_size, image.width, frame_size),
            batch=self.batch, group=pyglet.graphics.OrderedGroup(0))
        self.active = pyglet.sprite.Sprite(
            image.get_region(0, 0, frame_size, frame_size), batch=self.batch,
            group=pyglet.graphics.OrderedGroup(2))
        self.hearts = []
        for i in range(0, 10):
            heart = pyglet.sprite.Sprite(
                heart_image.get_region(0, 0, heart_image.width, heart_image.width),
                batch=self.batch, group=pyglet.graphics.OrderedGroup(0))
            self.hearts.append(heart)
        self.current_block_label = None
        self.set_position(width, height)

    def change_index(self, change):
        self.set_index(self.current_index + change)

    def set_index(self, index):
        index = int(index)
        if self.current_index == index:
            return
        self.current_index = index
        if self.current_index >= self.max_items:
            self.current_index = 0
        elif self.current_index < 0:
            self.current_index = self.max_items - 1
        self.update_current()

    def update_items(self):
        self.icons = []
        for amount_label in self.amount_labels:
            amount_label.delete()
        self.amount_labels = []
        x = self.frame.x + 3
        items = self.player.quick_slots.get_items()
        items = items[:self.max_items]
        for item in items:
            if not item:
                x += (self.icon_size * 0.5) + 3
                continue
            block = BLOCKS_DIR[item.type]
            block_icon = self.model.group.texture.get_region(
                int(block.side_texture[0] * 8) * self.icon_size,
                int(block.side_texture[1] * 8) * self.icon_size, self.icon_size,
                self.icon_size)
            icon = pyglet.sprite.Sprite(block_icon, batch=self.batch,
                                        group=self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = self.frame.y + 3
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name='Arial', font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=block.amount_label_color, batch=self.batch,
                group=self.labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
        self.update_current()

    def update_current(self):
        if self.current_block_label:
            self.current_block_label.delete()
        if hasattr(self.get_current_block_item(False), 'quickslots_x') and hasattr(self.get_current_block_item(False), 'quickslots_y'):
            self.current_block_label = pyglet.text.Label(
                self.get_current_block_item(False).name, font_name='Arial', font_size=9,
                x=self.get_current_block_item(False).quickslots_x + 0.25 * self.icon_size, y=self.get_current_block_item(False).quickslots_y - 20, 
                anchor_x='center', anchor_y='bottom',
                color=(255, 255, 255, 255), batch=self.batch,
                group=self.labels_group)
        self.active.x = self.frame.x + (self.current_index * 35)

    def set_position(self, width, height):
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size * 0.5
        self.active.y = self.frame.y
        self.update_health()
        self.update_current()
        self.update_items()

    def update_health(self):
        hearts_to_show = self.player.health
        showed_hearts = 0
        for i, heart in enumerate(self.hearts):
            heart.x = self.frame.x + i * (20 + 2) + (self.frame.width - hearts_to_show * (20 + 2)) / 2 
            heart.y = self.icon_size * 1.0 + 12
            heart.opacity = 255
            if showed_hearts >= hearts_to_show:
                heart.opacity = 0
            showed_hearts += 1

    def get_current_block(self):
        item = self.player.quick_slots.at(self.current_index)
        if not item:
            return
        item_id = item.type
        if item_id >= ITEM_ID_MIN:
            return ITEMS_DIR[item_id]
        return BLOCKS_DIR[item_id]

    def get_current_block_item(self, remove=True):
        item = self.player.quick_slots.at(self.current_index)
        return item

    def get_current_block_item_and_amount(self, remove=True):
        item = self.player.quick_slots.at(self.current_index)
        if item:
            amount = item.amount
            if remove:
                self.player.quick_slots.remove_by_index(self.current_index,
                                                        quantity=item.amount)
            return item, amount
        return False

    def remove_current_block(self, quantity=1):
        self.player.quick_slots.remove_by_index(self.current_index, quantity=quantity)
        self.update_items()

    def toggle_active_frame_visibility(self):
        self.active.opacity = 0 if self.active.opacity == 255 else 255


class Model(World):
    def __init__(self, initialize=True):
        super(Model, self).__init__()
        if initialize:
            self.initialize()

    def initialize(self):
        world_size = config.getint('World', 'size')
        world_type = config.getint('World', 'type')
        hill_height = config.getint('World', 'hill_height')
        flat_world = config.getboolean('World', 'flat')
        self.max_trees = config.getint('World', 'max_trees')
        tree_chance = self.max_trees / float(world_size * (SECTOR_SIZE ** 3))
        n = world_size / 2  # 80
        s = 1
        y = 0

        worldtypes_grounds = (
            grass_block,
            dirt_block,
            (sand_block,) * 15 + (sandstone_block,) * 4,
            (water_block,) * 30 + (clay_block,) * 4,
            grass_block,
            (grass_block,) * 15 + (dirt_block,) * 3 + (stone_block,),
            snowgrass_block,
        )

        world_type_trees = (
            (OakTree, BirchTree),
            OakTree,
            Cactus,
            (OakTree, JungleTree, BirchTree, Cactus),
            (Cactus, BirchTree),
            (OakTree, BirchTree),
            (OakTree, BirchTree),
        )

        ore_type_blocks = (
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            gravel_block, gravel_block, gravel_block, gravel_block, gravel_block,
            gravel_block, gravel_block, gravel_block, gravel_block, gravel_block,
            coalore_block, coalore_block, coalore_block, coalore_block, coalore_block,
            ironore_block, ironore_block, ironore_block, ironore_block,
            goldore_block, goldore_block, goldore_block,
            diamondore_block, diamondore_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
            stone_block, stone_block, stone_block, stone_block, stone_block,
        )


        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):

                # Generation of the outside wall
                if x in (-n, n) or z in (-n, n):
                    for dy in xrange(-16, 10):  # was -2 ,6
                        self.init_block((x, y + dy, z), stone_block)
                    continue



                # Generation of the ground

                block = worldtypes_grounds[world_type]

                if isinstance(block, (tuple, list)):
                    block = random.choice(block)
                self.init_block((x, y - 2, z), block)
                for yy in xrange(-16, -2):
                    # ores and filler...
                    oblock = random.choice(ore_type_blocks)
                    self.init_block((x, yy , z), oblock)
                self.init_block((x, y - 16, z), bed_block)

                # Perhaps a tree
                if self.max_trees > 0:
                    showtree = random.random()
                    if showtree <= tree_chance:
                        tree_class = world_type_trees[world_type]
                        if isinstance(tree_class, (tuple, list)):
                            tree_class = random.choice(tree_class)
                        self.generate_tree((x, y - 2, z), tree_class)

        if flat_world:
            return

        o = n - 10 + hill_height - 6

        world_type_blocks = (
            grass_block,
            (dirt_block, sandstone_block),
            sand_block,
            (grass_block, sand_block),
            (grass_block, sand_block, dirt_block),
            stone_block,
            snowgrass_block,
        )

        # Hills generation
        # FIXME: This generation in two phases (ground then hills), leads to
        # hills overlaying trees.
        for _ in xrange(world_size / 2 + 40):  # (120):
            a = random.randint(-o, o)
            b = random.randint(-o, o)
            c = -1
            h = random.randint(1, hill_height)
            s = random.randint(4, hill_height + 2)
            d = 1
            block = world_type_blocks[world_type]
            if isinstance(block, (tuple, list)):
                block = random.choice(block)
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        if (x, y, z) in self:
                            continue

                        randomOre = random.randrange(1,100)
                        if randomOre <= 5:
                            oblock = random.choice(ore_type_blocks)
                            self.init_block((x, y +1 , z), block) #cover up the ore block top
                            self.init_block((x, y , z -1), block) #cover up the ore block back
                            self.init_block((x, y , z +1), block) #cover up the ore block front
                            self.init_block((x -1, y , z), block) #cover up the ore block left
                            self.init_block((x +1, y , z), block) #cover up the ore block right
                            self.init_block((x, y , z), oblock)
                        elif randomOre > 5:
                            self.init_block((x, y, z), block)

                        #self.init_block((x, y, z), block)


                        # Perhaps a tree
                        if self.max_trees > 0:
                            showtree = random.random()
                            if showtree <= tree_chance:
                                tree_class = world_type_trees[world_type]
                                if isinstance(tree_class, (tuple, list)):
                                    tree_class = random.choice(tree_class)
                                self.generate_tree((x, y, z), tree_class)

                s -= d

    def generate_tree(self, position, tree_class):
        x, y, z = position

        # Avoids a tree from touching another.
        if self.has_neighbors((x, y + 1, z), TREE_BLOCKS, diagonals=True):
            return

        # A tree can't grow on anything.
        if self[position] not in tree_class.grows_on:
            return

        tree_class.add_to_world(self, position)

        self.max_trees -= 1

    def init_block(self, position, block):
        # FIXME: This should be more complex than that, and use
        # self.spreading_mutations.
        if block == dirt_block:
            block = grass_block
        self.add_block(position, block, sync=False, force=False)


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        self.show_gui = kwargs.pop('show_gui', True)
        self.save = kwargs.pop('save', None)
        super(Window, self).__init__(*args, **kwargs)
        self.exclusive = False
        self.strafe = [0, 0]
        self.sector = None
        self.focus_block = Block(width=1.05, height=1.05)
        self.reticle = None
        self.time_of_day = 0.0
        self.count = 0
        self.clock = 6
        self.light_y = 1.0
        self.light_z = 1.0
        self.earth = vec(0.8, 0.8, 0.8, 1.0)
        self.white = vec(1.0, 1.0, 1.0, 1.0)
        self.ambient = vec(1.0, 1.0, 1.0, 1.0)
        self.polished = GLfloat(100.0)
        self.highlighted_block = None
        self.block_damage = 0
        self.crack = None
        self.crack_batch = pyglet.graphics.Batch()
        self.mouse_pressed = False
        self.dy = 0
        self.show_fog = False
        self.last_key = None
        self.sorted = False
        global config
        self.key_move_forward = config.getint('Controls', 'move_forward')
        self.key_move_backward = config.getint('Controls', 'move_backward')
        self.key_move_left = config.getint('Controls', 'move_left')
        self.key_move_right = config.getint('Controls', 'move_right')
        self.key_jump = config.getint('Controls', 'jump')
        self.key_inventory = config.getint('Controls', 'inventory')
        save_len = -1 if self.save is None else len(self.save)
        if self.save is None or save_len < 2:  # model and model.sectors
            self.model = Model()
            self.player = Player((0, 0, 0), (-20, 0))
        else:
            self.model = Model(initialize=False)
            for item in self.save[0]:
                self.model[item[0]] = item[1]
            self.model.sectors = self.save[1]
            if save_len > 2 and isinstance(self.save[2], list) \
                    and len(self.save[2]) == 2:
                self.strafe = self.save[2]
            if save_len > 3 and isinstance(self.save[3], Player):
                self.player = self.save[3]
            if save_len > 4 and isinstance(self.save[4], float):
                self.time_of_day = self.save[4]
        self.item_list = ItemSelector(self.width, self.height, self.player,
                                      self.model)
        self.inventory_list = InventorySelector(self.width, self.height,
                                                self.player, self.model)
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        self.show_inventory = False
        if self.show_gui:
            self.label = pyglet.text.Label(
                '', font_name='Arial', font_size=8, x=10, y=self.height - 10,
                anchor_x='left', anchor_y='top', color=(255, 255, 255, 255))
        pyglet.clock.schedule_interval(self.update, 1.0 / MAX_FPS)
        pyglet.clock.schedule_interval_soft(self.model.process_queue, 1.0 / MAX_FPS)

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        x, y = self.player.rotation
        y_r = radians(y)
        x_r = radians(x)
        m = cos(y_r)
        dy = sin(y_r)
        x_r -= HALF_PI
        dx = cos(x_r) * m
        dz = sin(x_r) * m
        return dx, dy, dz

    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.player.rotation
            y_r = radians(y)
            x_r = radians(x)
            strafe = atan2(*self.strafe)
            if self.player.flying:
                m = cos(y_r)
                dy = sin(y_r)
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    dy *= -1
                x_r += strafe
                dx = cos(x_r) * m
                dz = sin(x_r) * m
            else:
                dy = 0.0
                x_r += strafe
                dx = cos(x_r)
                dz = sin(x_r)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return dx, dy, dz

    def update_time(self):
        """
        The idle function advances the time of day.
        The day has 24 hours, from sunrise to sunset and from sunrise to
        second sunset.
        The time of day is converted to degrees and then to radians.
        """

        if not self.exclusive:
            return

        time_of_day = self.time_of_day if self.time_of_day < 12.0 \
            else 24.0 - self.time_of_day

        if time_of_day <= 2.5:
            self.time_of_day += 1.0 / TIME_RATE
            time_of_day += 1.0 / TIME_RATE
            self.count += 1
        else:
            self.time_of_day += 20.0 / TIME_RATE
            time_of_day += 20.0 / TIME_RATE
            self.count += 1.0 / 20.0
        if self.time_of_day > 24.0:
            self.time_of_day = 0.0
            time_of_day = 0.0

        side = len(self.model.sectors) * 2.0

        self.light_y = 2.0 * side * sin(time_of_day * HOUR_DEG * DEG_RAD)
        self.light_z = 2.0 * side * cos(time_of_day * HOUR_DEG * DEG_RAD)
        if time_of_day <= 2.5:
            ambient_value = 1.0
        else:
            ambient_value = 1 - (time_of_day - 2.25) / 9.5
        self.ambient = vec(ambient_value, ambient_value, ambient_value, 1.0)

        # Calculate sky colour according to time of day.
        sin_t = sin(pi * time_of_day / 12.0)
        global BACK_RED
        global BACK_GREEN
        global BACK_BLUE
        BACK_RED = 0.1 * (1.0 - sin_t)
        BACK_GREEN = 0.9 * sin_t
        BACK_BLUE = min(sin_t + 0.4, 0.8)

        if fmod(self.count / 2, TIME_RATE) == 0:
            if self.clock == 18:
                self.clock = 6
            else:
                self.clock += 1

    def update(self, dt):
        sector = sectorize(self.player.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            # When the world is loaded, show every visible sector.
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector

        self.model.content_update(dt)

        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)
        if self.mouse_pressed:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.player.position, vector)
            if block:
                if self.highlighted_block != block:
                    self.set_highlighted_block(block)

            if self.highlighted_block:
                hit_block = self.model[self.highlighted_block]
                if hit_block.hardness >= 0:
                    self.block_damage += self.player.attack_power
                    if self.block_damage >= hit_block.hardness:
                        self.model.remove_block(self.highlighted_block)
                        self.set_highlighted_block(None)
                        if hit_block.drop_id is not None \
                                and self.player.add_item(hit_block.drop_id):
                            self.item_list.update_items()
                            self.inventory_list.update_items()
                else:
                    self.set_highlighted_block(None)
        self.update_time()

    def _update(self, dt):
        # walking
        speed = 15 if self.player.flying else 5
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.player.flying:
            self.dy -= dt * 0.022  # g force, should be = jump_speed * 0.5 /
            # max_jump_height
            self.dy = max(self.dy, -0.5)  # terminal velocity
            dy += self.dy
        else:
            self.dy = max(self.dy, -0.5)  # terminal velocity
            dy += self.dy
            # collisions
        x, y, z = self.player.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), 2)
        self.player.position = (x, y, z)
        
    def set_highlighted_block(self, block):
        self.highlighted_block = block
        self.block_damage = 0
        if self.crack:
            self.crack.delete()
        self.crack = None

    def set_highlighted_block(self, block):
        self.highlighted_block = block
        self.block_damage = 0
        if self.crack:
            self.crack.delete()
        self.crack = None

    def save_to_file(self):
        if DISABLE_SAVE:
            if not options.nocompression:
                save_world(self, game_dir, SAVE_FILENAME)
            else:
                save_world(self, game_dir, SAVE_FILENAME, CLASSIC_SAVE_TYPE)

    def collide(self, position, height):
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    op = tuple(op)
                    if op not in self.model:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        return tuple(p)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if (self.exclusive or self.show_inventory) and scroll_y != 0:
            if not self.show_inventory:
                self.item_list.change_index(scroll_y * -1)
            else:
                self.inventory_list.change_index(scroll_y * -1)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.show_inventory:
            self.inventory_list.on_mouse_press(x, y, button, modifiers)
            return
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.player.position, vector)
            if button == pyglet.window.mouse.LEFT:
                if block:
                    self.mouse_pressed = True
                    self.set_highlighted_block(None)
            else:
                if previous:
                    hit_block = self.model[block]
                    if hit_block.density >= 1:
                        current_block = self.item_list.get_current_block()
                        if current_block is not None:
                            # if current block is an item,
                            # call its on_right_click() method to handle this event
                            if current_block.id >= ITEM_ID_MIN:
                                current_block.on_right_click()
                            else:
                                localx, localy, localz = map(operator.sub,previous,normalize(self.player.position))
                                if localx != 0 or localz != 0 or (localy != 0 and localy != -1):
                                    self.model.add_block(previous, current_block)
                                    self.item_list.remove_current_block()
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_release(self, x, y, button, modifiers):
        self.set_highlighted_block(None)
        self.mouse_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.show_inventory:
            self.inventory_list.on_mouse_motion(x, y, dx, dy)
            return
        if self.exclusive:
            m = 0.15
            x, y = self.player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.player.rotation = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.show_inventory:
                self.inventory_list.on_mouse_drag(x, y, dx, dy, button, modifiers)
                return
            if self.exclusive:
                self.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == self.key_move_forward:
            self.strafe[0] -= 1
        elif symbol == self.key_move_backward:
            self.strafe[0] += 1
        elif symbol == self. key_move_left:
            self.strafe[1] -= 1
        elif symbol == self.key_move_right:
            self.strafe[1] += 1
        elif symbol == self.key_jump:
            if self.player.flying:
                self.dy = 0.045  # jump speed
            elif self.dy == 0:
                self.dy = 0.016  # jump speed
        elif symbol == key.LSHIFT or symbol == key.RSHIFT:
            if self.player.flying:
                self.dy = -0.045  # inversed jump speed
        elif symbol == key.ESCAPE:
            if self.show_inventory:
                self.inventory_list.toggle_active_frame_visibility()
                self.show_inventory = not self.show_inventory
                self.set_exclusive_mouse(not self.show_inventory)
                self.item_list.update_items()
            else:
                self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.dy = 0
            self.player.flying = not self.player.flying
        elif symbol == key.B or symbol == key.F3:
            self.show_gui = not self.show_gui
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0])
            self.item_list.set_index(index)
        elif symbol == key.V:
            self.save_to_file()
        elif symbol == key.Q:
            if options.fullscreen == True:
                pyglet.app.exit() # for fullscreen
        elif symbol == key.M:
            if self.last_key == symbol and not self.sorted:
                self.player.quick_slots.sort()
                self.player.inventory.sort()
                self.sorted = True
            else:
                self.player.quick_slots.change_sort_mode()
                self.player.inventory.change_sort_mode()
                self.item_list.update_items()
                self.inventory_list.update_items()
        elif symbol == self.key_inventory:
            self.inventory_list.toggle_active_frame_visibility()
            self.show_inventory = not self.show_inventory
            self.set_exclusive_mouse(not self.show_inventory)
            self.item_list.update_items()
        elif symbol == key.ENTER:
            if self.show_inventory:
                current_block = self.inventory_list\
                    .get_current_block_item_and_amount()
                if current_block:
                    if not self.player.quick_slots.add_item(
                            current_block[0].id,
                            quantity=current_block[1]):
                        self.player.inventory.add_item(current_block[0].id,
                                                       quantity=current_block[
                                                           1])
            else:
                current_block = self.item_list\
                    .get_current_block_item_and_amount()
                if current_block:
                    if not self.player.inventory.add_item(
                            current_block[0].id, quantity=current_block[1]):
                        self.player.quick_slots.add_item(
                            current_block[0].id, quantity=current_block[1])
            self.item_list.update_items()
            self.inventory_list.update_items()
        self.last_key = symbol

    def on_key_release(self, symbol, modifiers):
        if symbol == self.key_move_forward:
            self.strafe[0] += 1
        elif symbol == self.key_move_backward:
            self.strafe[0] -= 1
        elif symbol == self.key_move_left:
            self.strafe[1] += 1
        elif symbol == self.key_move_right:
            self.strafe[1] -= 1
        elif (symbol == self.key_jump or symbol == key.LSHIFT
              or symbol == key.RSHIFT) and self.player.flying:
            self.dy = 0

    def on_resize(self, width, height):
        if self.reticle:
            self.reticle.delete()
        x, y = self.width / 2, self.height / 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(
            4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )
        if self.show_gui:
            self.label.y = height - 10
            self.item_list.set_position(width, height)
            self.inventory_list.set_position(width, height)

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width != 0:
            glOrtho(0, width, 0, height, -1, 1)
        else:
            glOrtho(0, 1, 0, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        width, height = self.get_size()
        if self.show_fog:
            glFogfv(GL_FOG_COLOR, vec(BACK_RED, BACK_GREEN, BACK_BLUE, 1.0))
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if width != float(height):
            gluPerspective(FOV, width / float(height), NEAR_CLIP_DISTANCE,
                           FAR_CLIP_DISTANCE)
        else:
            gluPerspective(FOV, 1, NEAR_CLIP_DISTANCE, FAR_CLIP_DISTANCE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rotation
        glRotatef(x, 0, 1, 0)
        x_r = radians(x)
        glRotatef(-y, cos(x_r), 0, sin(x_r))
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.9, 0.9, 0.9, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(0.9, 0.9, 0.9, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION,
                  vec(1.0, self.light_y, self.light_z, 1.0))
        glLightfv(GL_LIGHT1, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT2, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.earth)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.white)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.polished)

    def clear(self):
        glClearColor(BACK_RED, BACK_GREEN, BACK_BLUE, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        super(Window, self).clear()

    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.crack_batch.draw()
        self.draw_focused_block()
        self.set_2d()
        if self.show_gui:
            self.draw_label()
            if not self.show_inventory:
                self.item_list.batch.draw()
            if self.show_inventory:
                self.inventory_list.batch.draw()
                if self.inventory_list.selected_item_icon:
                    self.inventory_list.selected_item_icon.draw()
                if self.inventory_list.crafting_outcome_icon:
                    self.inventory_list.crafting_outcome_icon.draw()
        if self.exclusive:
            self.draw_reticle()

        pyglet.clock.tick()

    def draw_focused_block(self):
        glDisable(GL_LIGHTING)
        vector = self.get_sight_vector()
        position = self.model.hit_test(self.player.position, vector)[0]
        if position:
            hit_block = self.model[position]
            if hit_block.density >= 1:
                vertex_data = self.focus_block.get_vertices(*position)
                glColor3d(0, 0, 0)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                if self.block_damage == 0:
                    pass
                else:   # also show the cracks
                    crack_level = int(floor((self.block_damage / hit_block.hardness) * CRACK_LEVEL)) # range: [0, CRACK_LEVEL]
                    if crack_level > CRACK_LEVEL:
                        return
                    texture_data = crack_textures.texture_data[crack_level]
                    if self.crack:
                        self.crack.delete()
                    self.crack = self.crack_batch.add(24, GL_QUADS, self.model.group, ('v3f/static', vertex_data) ,
                                                                            ('t2f/static', texture_data))

    def draw_label(self):
        x, y, z = self.player.position
        self.label.text = '%.1f %02d (%.2f, %.2f, %.2f) %d / %d' \
            % (self.time_of_day if (self.time_of_day < 12.0)
               else (24.0 - self.time_of_day),
               pyglet.clock.get_fps(), x, y, z,
               len(self.model._shown), len(self.model))
        self.label.draw()

    def draw_reticle(self):
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)


def setup_fog(window):
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, vec(BACK_RED, BACK_GREEN, BACK_BLUE, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_DENSITY, 0.35)
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, DRAW_DISTANCE) # 80)
    window.show_fog = True


def setup():
    glClearColor(BACK_RED, BACK_GREEN, BACK_BLUE, 1)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def main(options):
    save_object = None
    global SAVE_FILENAME
    global DISABLE_SAVE
    global DRAW_DISTANCE
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
    if options.fullscreen == True:
        window = Window(
        fullscreen=True, caption=APP_NAME,
        resizable=True, save=save_object, vsync=False)
    elif options.fullscreen == False:
            window = Window(
        width=options.width, height=options.height, caption=APP_NAME,
        resizable=True, save=save_object, vsync=False)

    window.set_exclusive_mouse(True)
    setup()
    if config.getboolean('World', 'show_fog'):
        setup_fog(window)
    pyglet.clock.set_fps_limit(MAX_FPS)
    pyglet.app.run()
    if options.disable_auto_save and options.disable_save:
        window.save_to_file()
    if options.save_config:
        try:
            with open(config_file, 'wb') as handle:
                config.write(handle)
        except:
            print "Problem: Write error."



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play a Python made Minecraft clone.')
    parser.add_argument("-width", type=int, default=850, help = "Set the default Widht.")
    parser.add_argument("-height", type=int, default=480, help = "Set the default Height.")
    parser.add_argument("-terrain", choices=terrain_options.keys(), help = "Different terains. Choose grass, island, mountains,desert, plains")
    parser.add_argument("-hillheight", type=int, help = "How high the hills are.")
    parser.add_argument("-worldsize", type=int, help = "The width size of the world.")
    parser.add_argument("-maxtrees", type=int, help = "How many trees and cacti should be made.")
    parser.add_argument("-seed", default=None)
    parser.add_argument("--flat", action="store_true", default=False, help = "Generate a flat world.")
    parser.add_argument("--hide-fog", action="store_true", default=False, help ="Hides the fog, see the whole landscape.")
    parser.add_argument("--show-gui", action="store_true", default=True, help = "Enabled by default.")
    parser.add_argument("--disable-auto-save", action="store_false", default=True, help = "Do not save world on exit.")
    parser.add_argument("-draw-distance", choices=['short', 'medium', 'long'], default='short', help =" How far to draw the map. Choose short, medium or long.")
    parser.add_argument("-save", type=unicode, default=SAVE_FILENAME, help = "Type a name for the world to be saved as.")
    parser.add_argument("--disable-save", action="store_false", default=True, help = "Disables saving.")
    parser.add_argument("--fast", action="store_true", default=False, help = "Makes time progress faster then normal.")
    parser.add_argument("--save-config", action="store_true", default=False, help = "Saves the choices as the default config.")
    parser.add_argument("-fullscreen", action="store_true", default=False, help = "Runs the game in fullscreen. Press 'Q' to exit the game.")
    parser.add_argument("-nocompression", action="store_true", default=False, help = "Enables compression for a smaller save file.")
    options = parser.parse_args()
    main(options)
