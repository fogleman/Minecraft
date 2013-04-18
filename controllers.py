# Imports, sorted alphabetically.

# Python packages
from math import cos, sin, pi, fmod
import operator
from binascii import hexlify
import datetime

# Third-party packages
from pyglet.gl import *

# Modules from this project
from cameras import *
from commands import CommandParser, CommandException
import globals as G
from gui import *
from model import *
from player import *
from savingsystem import *
from commands import CommandParser, COMMAND_HANDLED, COMMAND_ERROR_COLOR, CommandException, UnknownCommandException
from utils import init_resources
from views import *


def vec(*args):
    """Creates GLfloat arrays of floats"""
    return (GLfloat * len(args))(*args)


class Controller(object):
    def __init__(self, window):
        self.window = window
        self.current_view = None
        init_resources()

    def setup(self):
        pass

    def update(self, dt):
        if self.current_view:
            self.current_view.update(dt)
        
    def switch_view(self, new_view):
        if self.current_view:
            self.current_view.pop_handlers()
            self.current_view = None
        self.current_view = new_view
        self.current_view.add_handlers()

    def set_2d(self):
        width, height = self.window.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def push_handlers(self):
        self.window.push_handlers(self)
        self.setup()

    def pop_handlers(self):
        if self.current_view:
            self.current_view.pop_handlers()
        self.window.pop_handlers()

class MainMenuController(Controller):
    def setup(self):
        self.switch_view(MainMenuView(self))

    def start_game_func(self):
        self.window.switch_controller(GameController(self.window))
        return pyglet.event.EVENT_HANDLED

    def new_game_func(self):
        if G.DISABLE_SAVE:
            remove_world(G.game_dir, G.SAVE_FILENAME)
        self.window.switch_controller(GameController(self.window))
        return pyglet.event.EVENT_HANDLED

    def exit_game_func(self):
        pyglet.app.exit()
        return pyglet.event.EVENT_HANDLED

    def game_options_func(self):
        self.switch_view(OptionsView(self))
        return pyglet.event.EVENT_HANDLED

    def main_menu_func(self):
        self.switch_view(MainMenuView(self))
        return pyglet.event.EVENT_HANDLED

    def controls_func(self):
        self.switch_view(ControlsView(self))
        return pyglet.event.EVENT_HANDLED

class GameController(Controller):
    def __init__(self, window):
        super(GameController, self).__init__(window)
        self.sector = None
        self.time_of_day = 0.0
        self.count = 0
        self.clock = 6
        self.light_y = 1.0
        self.light_z = 1.0
        self.bg_red = 0.0
        self.bg_green = 0.0
        self.bg_blue = 0.0
        self.hour_deg = 15.0
        self.highlighted_block = None
        self.block_damage = 0
        self.crack = None
        self.mouse_pressed = False
        self.last_key = None
        self.sorted = False

    def update(self, dt):
        sector = sectorize(self.player.position)
        if sector != self.sector:
            self.model.change_sectors(sector)
            # When the world is loaded, show every visible sector.
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector

        self.model.content_update(dt)

        m = 8
        df = min(dt, 0.2)
        for _ in xrange(m):
            self.player.update(df / m, self)
        if self.mouse_pressed:
            vector = self.player.get_sight_vector()
            block, previous = self.model.hit_test(self.player.position, vector,
                                                  self.player.attack_range)
            if block:
                if self.highlighted_block != block:
                    self.set_highlighted_block(block)
            else:
                self.set_highlighted_block(None)

            if self.highlighted_block:
                hit_block = self.model[self.highlighted_block]
                if hit_block.hardness >= 0:

                    multiplier = 1
                    current_item = self.item_list.get_current_block()
                    if current_item is not None:
                        if isinstance(current_item, Tool):  # tool
                            if current_item.tool_type == hit_block.digging_tool:
                                multiplier = current_item.multiplier

                    self.block_damage += self.player.attack_power * dt * multiplier
                    if self.block_damage >= hit_block.hardness:
                        self.model.remove_block(self.player,
                                                self.highlighted_block)
                        self.set_highlighted_block(None)
                        if hit_block.drop_id is not None \
                                and self.player.add_item(hit_block.drop_id):
                            self.item_list.update_items()
                            self.inventory_list.update_items()
        self.update_time()
        self.camera.update(dt)

    def setup(self):
        glClearColor(self.bg_red, self.bg_green, self.bg_blue, 1)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.1)
        glEnable(GL_BLEND)
        glEnable(GL_LINE_SMOOTH)

        if G.FOG_ENABLED:
            glEnable(GL_FOG)
            glFogfv(GL_FOG_COLOR, vec(self.bg_red, self.bg_green, self.bg_blue, 1))
            glHint(GL_FOG_HINT, GL_DONT_CARE)
            glFogi(GL_FOG_MODE, GL_LINEAR)
            glFogf(GL_FOG_DENSITY, 0.35)
            glFogf(GL_FOG_START, 20.0)
            glFogf(GL_FOG_END, G.DRAW_DISTANCE)  # 80)

        self.focus_block = Block(width=1.05, height=1.05)
        self.earth = vec(0.8, 0.8, 0.8, 1.0)
        self.white = vec(1.0, 1.0, 1.0, 1.0)
        self.ambient = vec(1.0, 1.0, 1.0, 1.0)
        self.polished = GLfloat(100.0)
        self.crack_batch = pyglet.graphics.Batch()

        if G.DISABLE_SAVE and world_exists(G.game_dir, G.SAVE_FILENAME):
            open_world(self, G.game_dir, G.SAVE_FILENAME)
        else:
            seed = G.LAUNCH_OPTIONS.seed
            if seed is None:
                # Generates pseudo-random number.
                try:
                    seed = long(hexlify(os.urandom(16)), 16)
                except NotImplementedError:
                    import time
                    seed = long(time.time() * 256)  # use fractional seconds
                # Then convert it to a string so all seeds have the same type.
                seed = str(seed)

                print('No seed set, generated random seed: ' + seed)
            G.SEED = seed
            random.seed(seed)

            with open(os.path.join(G.game_dir, 'seeds.txt'), 'a') as seeds:
                seeds.write(datetime.datetime.now().strftime(
                    'Seed used the %d %m %Y at %H:%M:%S\n'))
                seeds.write('%s\n\n' % seed)

            self.model = Model()
            self.player = Player((0,self.model.terraingen.get_height(0,0)+2,0), (-20, 0),
                                 game_mode=G.GAME_MODE)
            self.save_to_file() #So the hardcoded spawn sectors aren't overwritten by the worldgen
        print('Game mode: ' + self.player.game_mode)
        self.item_list = ItemSelector(self, self.player, self.model)
        self.inventory_list = InventorySelector(self, self.player, self.model)
        self.item_list.on_resize(self.window.width, self.window.height)
        self.inventory_list.on_resize(self.window.width, self.window.height)
        self.text_input = TextWidget(self.window, '',
                                     0, 0,
                                     self.window.width,
                                     visible=False,
                                     font_name='Arial')
        self.text_input.push_handlers(on_toggled=self.on_text_input_toggled, key_released=self.text_input_callback)
        self.chat_box = TextWidget(self.window, '',
                                   0, self.text_input.y + self.text_input.height + 50,
                                   self.window.width / 2, height=min(300, self.window.height / 3),
                                   visible=False, multi_line=True, readonly=True,
                                   font_size=14,
                                   font_name='Arial',
                                   background_color=(64,64,64,200))
        self.command_parser = CommandParser()
        self.camera = Camera3D(target=self.player)
        if G.HUD_ENABLED:
            self.label = pyglet.text.Label(
                '', font_name='Arial', font_size=8, x=10, y=self.window.height - 10,
                anchor_x='left', anchor_y='top', color=(255, 255, 255, 255))
        pyglet.clock.schedule_interval_soft(self.model.process_queue,
                                            1.0 / G.MAX_FPS)

    def update_time(self):
        """
        The idle function advances the time of day.
        The day has 24 hours, from sunrise to sunset and from sunrise to
        second sunset.
        The time of day is converted to degrees and then to radians.
        """

        if not self.window.exclusive:
            return

        time_of_day = self.time_of_day if self.time_of_day < 12.0 \
            else 24.0 - self.time_of_day

        if time_of_day <= 2.5:
            self.time_of_day += 1.0 / G.TIME_RATE
            time_of_day += 1.0 / G.TIME_RATE
            self.count += 1
        else:
            self.time_of_day += 20.0 / G.TIME_RATE
            time_of_day += 20.0 / G.TIME_RATE
            self.count += 1.0 / 20.0
        if self.time_of_day > 24.0:
            self.time_of_day = 0.0
            time_of_day = 0.0

        side = len(self.model.sectors) * 2.0

        self.light_y = 2.0 * side * sin(time_of_day * self.hour_deg
                                        * G.DEG_RAD)
        self.light_z = 2.0 * side * cos(time_of_day * self.hour_deg
                                        * G.DEG_RAD)
        if time_of_day <= 2.5:
            ambient_value = 1.0
        else:
            ambient_value = 1 - (time_of_day - 2.25) / 9.5
        self.ambient = vec(ambient_value, ambient_value, ambient_value, 1.0)

        # Calculate sky colour according to time of day.
        sin_t = sin(pi * time_of_day / 12.0)
        self.bg_red = 0.1 * (1.0 - sin_t)
        self.bg_green = 0.9 * sin_t
        self.bg_blue = min(sin_t + 0.4, 0.8)

        if fmod(self.count / 2, G.TIME_RATE) == 0:
            if self.clock == 18:
                self.clock = 6
            else:
                self.clock += 1

    def set_highlighted_block(self, block):
        self.highlighted_block = block
        self.block_damage = 0
        if self.crack:
            self.crack.delete()
        self.crack = None

    def save_to_file(self):
        if G.DISABLE_SAVE:
            save_world(self, G.game_dir, G.SAVE_FILENAME)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.window.exclusive:
            vector = self.player.get_sight_vector()
            block, previous = self.model.hit_test(self.player.position, vector, self.player.attack_range)
            if button == pyglet.window.mouse.LEFT:
                if block:
                    self.mouse_pressed = True
                    self.set_highlighted_block(None)
            else:
                if previous:
                    hit_block = self.model[block]

                    # show craft table gui
                    if hit_block.id == craft_block.id:
                        self.inventory_list.mode = 1
                        self.inventory_list.toggle(False)
                        return

                    if hit_block.id == furnace_block.id:
                        self.inventory_list.mode = 2
                        self.inventory_list.set_furnace(hit_block)
                        self.inventory_list.toggle(False)
                        return

                    if hit_block.density >= 1:
                        current_block = self.item_list.get_current_block()
                        if current_block is not None:
                            # if current block is an item,
                            # call its on_right_click() method to handle this event
                            if current_block.id >= G.ITEM_ID_MIN:
                                current_block.on_right_click()
                            else:
                                localx, localy, localz = map(operator.sub,previous,normalize(self.player.position))
                                if localx != 0 or localz != 0 or (localy != 0 and localy != -1):
                                    self.model.add_block(previous, current_block)
                                    self.item_list.remove_current_block()
                elif self.item_list.get_current_block() and self.item_list.get_current_block().regenerated_health != 0 and self.player.health < self.player.max_health:
                    self.player.change_health(self.item_list.get_current_block().regenerated_health)
                    self.item_list.get_current_block_item().change_amount(-1)
                    self.item_list.update_health()
                    self.item_list.update_items()
        else:
            self.window.set_exclusive_mouse(True)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.window.exclusive:
            self.set_highlighted_block(None)
            self.mouse_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.window.exclusive:
            m = 0.15
            x, y = self.player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.player.rotation = (x, y)
            self.camera.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == G.TOGGLE_HUD_KEY:
            G.HUD_ENABLED = not G.HUD_ENABLED
        elif symbol == G.SAVE_KEY:
            self.save_to_file()
        elif symbol == G.INVENTORY_SORT_KEY:
            if self.last_key == symbol and not self.sorted:
                self.player.quick_slots.sort()
                self.player.inventory.sort()
                self.sorted = True
            else:
                self.player.quick_slots.change_sort_mode()
                self.player.inventory.change_sort_mode()
                self.item_list.update_items()
                self.inventory_list.update_items()
        elif symbol == G.INVENTORY_KEY:
            self.set_highlighted_block(None)
            self.mouse_pressed = False
            self.inventory_list.toggle()
        elif symbol == G.SOUND_UP_KEY:
            G.EFFECT_VOLUME = min(G.EFFECT_VOLUME + .1, 1)
        elif symbol == G.SOUND_DOWN_KEY:
            G.EFFECT_VOLUME = max(G.EFFECT_VOLUME - .1, 0)
        self.last_key = symbol

    def on_key_release(self, symbol, modifiers):
        if symbol == G.TALK_KEY:
            self.toggle_text_input()
            return pyglet.event.EVENT_HANDLED

    def on_resize(self, width, height):
        if G.HUD_ENABLED:
            self.label.y = height - 10
        self.text_input.resize(x=0, y=0, width=self.window.width)
        self.chat_box.resize(x=0, y=self.text_input.y + self.text_input.height + 50,
                             width=self.window.width / 2, height=min(300, self.window.height/3))

    def set_3d(self):
        width, height = self.window.get_size()
        if G.FOG_ENABLED:
            glFogfv(GL_FOG_COLOR, vec(self.bg_red, self.bg_green, self.bg_blue, 1.0))
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(G.FOV, width / float(height),
                       G.NEAR_CLIP_DISTANCE,
                       G.FAR_CLIP_DISTANCE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.transform()
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
        glClearColor(self.bg_red, self.bg_green, self.bg_blue, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.model.transparency_batch.draw()
        self.crack_batch.draw()
        self.draw_focused_block()
        self.set_2d()
        if G.HUD_ENABLED:
            self.draw_label()
            self.item_list.draw()
            self.inventory_list.draw()
        self.text_input.draw()
        self.chat_box.draw()

    def show_cracks(self, hit_block, vertex_data):
        if self.block_damage:  # also show the cracks
            crack_level = int(CRACK_LEVELS * self.block_damage
                              / hit_block.hardness)  # range: [0, CRACK_LEVELS[
            if crack_level >= CRACK_LEVELS:
                return
            texture_data = crack_textures.texture_data[crack_level]
            count = len(texture_data) / 2
            if self.crack:
                self.crack.delete()
            self.crack = self.crack_batch.add(count, GL_QUADS, self.model.group,
                                              ('v3f/static', vertex_data),
                                              ('t2f/static', texture_data))

    def draw_focused_block(self):
        glDisable(GL_LIGHTING)
        vector = self.player.get_sight_vector()
        position = self.model.hit_test(self.player.position, vector, self.player.attack_range)[0]
        if position:
            hit_block = self.model[position]
            if hit_block.density >= 1:
                self.focus_block.width = hit_block.width * 1.05
                self.focus_block.height = hit_block.height * 1.05
                vertex_data = self.focus_block.get_vertices(*position)

                if hit_block.hardness > 0.0:
                    self.show_cracks(hit_block, vertex_data)

                glColor3d(0, 0, 0)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        x, y, z = self.player.position
        self.label.text = 'Time:%.1f Inaccurate FPS:%02d (%.2f, %.2f, %.2f) Blocks Shown: %d / %d sector_queue:%d'\
                          % (self.time_of_day if (self.time_of_day < 12.0)
               else (24.0 - self.time_of_day),
               pyglet.clock.get_fps(), x, y, z,
               len(self.model._shown), len(self.model), len(self.model.sector_queue))
        self.label.draw()

    def write_line(self, text, **kwargs):
        self.chat_box.write_line(text, **kwargs)

    def text_input_callback(self, symbol, modifier):
        if symbol == G.VALIDATE_KEY:
            txt = self.text_input.text.replace('\n', '')
            try:
                ex = self.command_parser.execute(txt, controller=self, user=self.player, world=self.model)
                if ex != COMMAND_HANDLED:
                    # Not a command
                    self.write_line("> %s" % txt, color=(255, 255, 255, 255))
                self.text_input.clear()
            except CommandException, e:
                error = str(e)
                self.write_line(error, color=COMMAND_ERROR_COLOR)
            return pyglet.event.EVENT_HANDLED

    def on_text_input_toggled(self):
        self.chat_box.toggle()
        if self.chat_box.visible:
            self.chat_box.focused = True # Allow scrolling
            self.window.push_handlers(self.chat_box)
        else:
            self.chat_box.focused = False
            self.window.remove_handlers(self.chat_box)

    def toggle_text_input(self):
        self.text_input.toggle()
        if self.text_input.visible:
            self.player.velocity = 0
            self.player.strafe = [0, 0]
            self.window.push_handlers(self.text_input)
            self.text_input.focus()
        else:
            self.window.remove_handlers(self.text_input)

    def push_handlers(self):
        self.setup()
        self.window.push_handlers(self.camera)
        self.window.push_handlers(self.player)
        self.window.push_handlers(self)
        self.window.push_handlers(self.item_list)
        self.window.push_handlers(self.inventory_list)

    def pop_handlers(self):
        self.window.pop_handlers()
        self.window.pop_handlers()
        self.window.pop_handlers()
        self.window.pop_handlers()
        self.window.pop_handlers()

    def on_close(self):
        self.save_to_file()
