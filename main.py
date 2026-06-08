import math
import random
import time
from collections import deque

import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

TICKS_PER_SEC = 60
SECTOR_SIZE = 16
WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50
PLAYER_HEIGHT = 2


def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n. """
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,
    ]


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square. """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side. """
    top_coords = tex_coord(*top)
    bottom_coords = tex_coord(*bottom)
    side_coords = tex_coord(*side)
    result = []
    result.extend(top_coords)
    result.extend(bottom_coords)
    result.extend(side_coords * 4)
    return result


TEXTURE_PATH = 'texture.png'

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
BEDROCK = tex_coords((2, 1), (2, 1), (2, 1))

OAK_LOG = tex_coords((3, 2), (3, 2), (3, 1))
OAK_PLANKS = tex_coords((3, 0), (3, 0), (3, 0))
OAK_LEAVES = tex_coords((2, 2), (2, 2), (2, 2))
STONE = tex_coords((1, 2), (1, 2), (1, 2))

FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block containing that position. """
    x, y, z = position
    return int(round(x)), int(round(y)), int(round(z))


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`. """
    x, y, z = normalize(position)
    return x // SECTOR_SIZE, 0, z // SECTOR_SIZE


class Model:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        self.world = {}
        self.shown = {}
        self.shown_batch_items = {}
        self.sectors = {}
        self.queue = deque()
        self._initialize()

    def _initialize(self):
        """ Initialize the world by placing all the blocks and trees. """
        n = 80
        s = 1
        y = 0

        for x in range(-n, n + 1, s):
            for z in range(-n, n + 1, s):
                self.add_block((x, y - 2, z), GRASS, immediate=False)
                self.add_block((x, y - 3, z), STONE, immediate=False)
                self.add_block((x, y - 4, z), STONE, immediate=False)
                self.add_block((x, y - 5, z), BEDROCK, immediate=False)
                if x in (-n, n) or z in (-n, n):
                    for dy in range(-5, 3):
                        self.add_block((x, y + dy, z), BEDROCK, immediate=False)

        o = n - 10
        for _ in range(120):
            a = random.randint(-o, o)
            b = random.randint(-o, o)
            c = -1
            h = random.randint(1, 6)
            side_len = random.randint(4, 8)
            d = 1
            t = random.choice([GRASS, SAND, BRICK])
            for y_pos in range(c, c + h):
                for x in range(a - side_len, a + side_len + 1):
                    for z in range(b - side_len, b + side_len + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (side_len + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y_pos, z), t, immediate=False)
                side_len -= d

        for x in range(-n + 4, n - 4, 5):
            for z in range(-n + 4, n - 4, 5):
                if random.random() < 0.25:
                    surface_y = 10
                    while surface_y > -5:
                        if (x, surface_y, z) in self.world:
                            break
                        surface_y -= 1

                    if (x, surface_y, z) in self.world and self.world[(x, surface_y, z)] == GRASS:
                        tree_height = random.randint(4, 6)
                        for dy in range(1, tree_height + 1):
                            self.add_block((x, surface_y + dy, z), OAK_LOG, immediate=False)

                        leaf_bottom = surface_y + tree_height - 2
                        for dy in range(leaf_bottom, leaf_bottom + 4):
                            for dx in range(-2, 3):
                                for dz in range(-2, 3):
                                    if dy >= leaf_bottom + 2 and (abs(dx) > 1 or abs(dz) > 1):
                                        continue
                                    if abs(dx) == 2 and abs(dz) == 2:
                                        continue
                                    if dx == 0 and dz == 0 and dy <= surface_y + tree_height:
                                        continue
                                    leaf_pos = (x + dx, dy, z + dz)
                                    if leaf_pos not in self.world:
                                        self.add_block(leaf_pos, OAK_LEAVES, immediate=False)

    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. Returns hit block and previous block. """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in range(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        """ Returns False if given `position` is surrounded on all 6 sides by blocks, True otherwise. """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        """ Add a block with the given `texture` and `position` to the world. """
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`. """
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        """ Check all blocks surrounding `position` and ensure their visual state is current. """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """ Show the block at the given `position`. """
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self.render_block(position, texture)
        else:
            self.enqueue(self.render_block, position, texture)

    def render_block(self, position, texture):
        """ Render the block into the batch queue. """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        self.shown_batch_items[position] = self.batch.add(
            24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data)
        )

    def hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. """
        self.shown.pop(position)
        if immediate:
            self.unrender_block(position)
        else:
            self.enqueue(self.unrender_block, position)

    def unrender_block(self, position):
        """ Remove the block from the render batch. """
        self.shown_batch_items.pop(position).delete()

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are drawn to the canvas. """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are removed from the canvas. """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in range(-pad, pad + 1):
            for dy in [0]:
                for dz in range(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def enqueue(self, func, *args):
        """ Add `func` to the internal queue. """
        self.queue.append((func, args))

    def dequeue(self):
        """ Pop the top function from the internal queue and call it. """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks to maintain smooth framerates. """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self.dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks. """
        while self.queue:
            self.dequeue()


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclusive = False
        self.flying = False
        self.strafe = [0, 0]
        self.position = (0, 0, 0)
        self.rotation = (0, 0)
        self.sector = None
        self.reticle = None
        self.dy = 0


        self.inventory = [GRASS, SAND, STONE, OAK_LOG, OAK_LEAVES, OAK_PLANKS, BRICK]
        self.block = self.inventory[0]

        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0
        ]
        self.model = Model()
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
                                       x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
                                       color=(0, 0, 0, 255))
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def set_exclusive_mouse(self, exclusive):
        """ Capture the mouse into the window and hide the OS cursor completely. """
        super().set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
        self.set_mouse_visible(not exclusive)

    def get_sight_vector(self):
        """ Returns the current line of sight vector. """
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return dx, dy, dz

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the player. """
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(self.strafe[0], self.strafe[1]))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    dy *= -1
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return dx, dy, dz

    def update(self, dt):
        """ Main game event loop scheduled to run continuously. """
        self.model.process_queue()

        # Aggressive mouse lock: Keep mouse centered and hidden while in game mode
        if self.exclusive:
            self.set_mouse_position(self.width // 2, self.height // 2)

        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt / m)

    def _update(self, dt):
        """ Update player position, check collisions, and apply physics. """
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        if not self.flying:
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

    def collide(self, position, height):
        """ Checks if the player is colliding with any blocks in the world. """
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:
            for i in range(3):
                if not face[i]:
                    continue
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        self.dy = 0
                    break
        return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Triggered when a mouse button is pressed. Used for block interaction or resuming. """
        if not self.exclusive:
            self.set_exclusive_mouse(True)
            return

        vector = self.get_sight_vector()
        block, previous = self.model.hit_test(self.position, vector)
        if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
            if previous:
                self.model.add_block(previous, self.block)
        elif button == pyglet.window.mouse.LEFT and block:
            texture = self.model.world[block]
            if texture != BEDROCK:
                self.model.remove_block(block)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Controls the camera view based on mouse movement. """
        if self.exclusive:
            m = 0.15
            rot_x, rot_y = self.rotation
            rot_x, rot_y = rot_x + dx * m, rot_y + dy * m
            rot_y = max(-90.0, min(90.0, rot_y))
            self.rotation = (rot_x, rot_y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """ Controls the camera view even while holding a mouse button (e.g., placing/breaking blocks). """
        if self.exclusive:
            m = 0.15
            rot_x, rot_y = self.rotation
            rot_x, rot_y = rot_x + dx * m, rot_y + dy * m
            rot_y = max(-90.0, min(90.0, rot_y))
            self.rotation = (rot_x, rot_y)

    def on_key_press(self, symbol, modifiers):
        """ Handles keyboard inputs (movement, jumping, block selection). """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
            return pyglet.event.EVENT_HANDLED
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]

    def on_key_release(self, symbol, modifiers):
        """ Resets movement flags when movement keys are released. """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1

    def on_resize(self, width, height):
        """ Re-calculates UI elements when the window is resized. """
        self.label.y = height - 10
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(
            4, ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        """ Configure OpenGL to draw 2D elements like the UI and crosshair. """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw the 3D world. """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Primary rendering function called by Pyglet. """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()

        if self.exclusive:
            self.draw_focused_block()

        self.draw_viewmodel()

        self.set_2d()
        self.draw_label()

        if self.exclusive:
            self.draw_reticle()
        else:
            self.draw_pause_screen()

        self.draw_hotbar()

    def draw_viewmodel(self):
        """ Draw the currently selected block in the bottom right corner (Hand). """
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(65.0, self.width / float(self.height), 0.1, 60.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glClear(GL_DEPTH_BUFFER_BIT)

        glTranslatef(0.6, -0.5, -1.5)
        glRotatef(-30, 1, 0, 0)
        glRotatef(45, 0, 1, 0)

        texture_data = list(self.block)
        vertex_data = cube_vertices(0, 0, 0, 0.25)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.model.group.texture.id)

        glColor3d(1, 1, 1)
        pyglet.graphics.draw(24, GL_QUADS,
                             ('v3f/static', vertex_data),
                             ('t2f/static', texture_data)
                             )

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_hotbar(self):
        """ Draw the 2D Hotbar at the bottom of the screen. """
        glDisable(GL_DEPTH_TEST)
        slot_size = 40
        padding = 10
        total_width = len(self.inventory) * (slot_size + padding) - padding
        start_x = (self.width - total_width) // 2
        y_pos = 20

        glDisable(GL_TEXTURE_2D)

        for i in range(len(self.inventory)):
            x = start_x + i * (slot_size + padding)

            if self.inventory[i] == self.block:
                glColor4f(1.0, 1.0, 1.0, 0.8)
            else:
                glColor4f(0.0, 0.0, 0.0, 0.5)

            pyglet.graphics.draw(4, GL_QUADS,
                                 ('v2f', [x, y_pos, x + slot_size, y_pos, x + slot_size, y_pos + slot_size, x,
                                          y_pos + slot_size])
                                 )

            if self.inventory[i] == self.block:
                glColor4f(0.2, 0.2, 0.2, 0.8)
                bx, by, bs = x + 2, y_pos + 2, slot_size - 4
                pyglet.graphics.draw(4, GL_QUADS,
                                     ('v2f', [bx, by, bx + bs, by, bx + bs, by + bs, bx, by + bs])
                                     )

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.model.group.texture.id)
        glColor3d(1, 1, 1)

        for i, tex in enumerate(self.inventory):
            x = start_x + i * (slot_size + padding) + slot_size / 2
            y_center = y_pos + slot_size / 2

            t_coords = tex[16:24]
            s = slot_size * 0.7 / 2
            vx = [x - s, y_center - s, x + s, y_center - s, x + s, y_center + s, x - s, y_center + s]

            pyglet.graphics.draw(4, GL_QUADS,
                                 ('v2f', vx),
                                 ('t2f', t_coords)
                                 )

    def draw_focused_block(self):
        """ Draws a wireframe outline around the block the player is currently looking at. """
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        """ Displays FPS and debug info in the top left corner. """
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model.shown_batch_items), len(self.model.world))
        self.label.draw()

    def draw_reticle(self):
        """ Draw the central aiming crosshair. """
        glDisable(GL_TEXTURE_2D)
        glLineWidth(2.0)
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)

    def draw_pause_screen(self):
        """ Draw a semi-transparent overlay and PAUSED text when the game is paused. """
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(0.0, 0.0, 0.0, 0.6)
        pyglet.graphics.draw(4, GL_QUADS,
                             ('v2f', [0, 0, self.width, 0, self.width, self.height, 0, self.height])
                             )

        label = pyglet.text.Label('GAME PAUSED', font_name='Arial', font_size=40, bold=True,
                                  x=self.width // 2, y=self.height // 2 + 20,
                                  anchor_x='center', anchor_y='center',
                                  color=(255, 255, 255, 255))

        sub_label = pyglet.text.Label('Click anywhere to resume', font_name='Arial', font_size=16,
                                      x=self.width // 2, y=self.height // 2 - 30,
                                      anchor_x='center', anchor_y='center',
                                      color=(200, 200, 200, 255))
        label.draw()
        sub_label.draw()


def setup_fog():
    """ Configure OpenGL depth fog to hide block pop-in distances. """
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)


def setup():
    """ Prepare OpenGL states for rendering our 3D world and 2D UI. """
    glClearColor(0.5, 0.69, 1.0, 1)
    glEnable(GL_CULL_FACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    setup_fog()


def main():
    window = Window(width=800, height=600, caption='Pyglet Minecraft Clone', resizable=True)
    window.set_exclusive_mouse(False)
    setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()