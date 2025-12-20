import sys
import math
import random
import time
from collections import deque
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

# Constants
TICKS_PER_SEC = 60
SECTOR_SIZE = 16
WALKING_SPEED = 5
FLYING_SPEED = 15
GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50
PLAYER_HEIGHT = 2
TEXTURE_PATH = 'texture.png'

# Helper functions
def cube_vertices(x, y, z, n):
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,
    ]

def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

GRASS = tex_coords((1,0),(0,1),(0,0))
SAND  = tex_coords((1,1),(1,1),(1,1))
BRICK = tex_coords((2,0),(2,0),(2,0))
STONE = tex_coords((2,1),(2,1),(2,1))
FACES = [(0,1,0),(0,-1,0),(-1,0,0),(1,0,0),(0,0,1),(0,0,-1)]

def normalize(position):
    return tuple(int(round(c)) for c in position)

def sectorize(position):
    x, y, z = normalize(position)
    return (x // SECTOR_SIZE, 0, z // SECTOR_SIZE)

# --- Model ---
class Model:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        try:
            self.group = pyglet.graphics.TextureGroup(pyglet.image.load(TEXTURE_PATH).get_texture())
        except Exception as e:
            print(f"Не удалось загрузить текстуру '{TEXTURE_PATH}': {e}")
            sys.exit(1)
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = deque()
        self._initialize()

    def _initialize(self):
        n = 20  # уменьшил размер мира для теста
        s = 1
        y = 0
        for x in range(-n, n+1):
            for z in range(-n, n+1):
                self.add_block((x,y-2,z), GRASS, immediate=False)
                self.add_block((x,y-3,z), STONE, immediate=False)
        # генерация холмов
        for _ in range(40):
            a = random.randint(-n, n)
            b = random.randint(-n, n)
            h = random.randint(1,3)
            for y in range(-1, -1 + h):
                for x in range(a-2,a+3):
                    for z in range(b-2,b+3):
                        self.add_block((x,y,z), random.choice([GRASS,SAND,BRICK]), immediate=False)

    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x+dx, y+dy, z+dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate and self.exposed(position):
            self.show_block(position)

    def remove_block(self, position, immediate=True):
        if position in self.world:
            del self.world[position]
        if position in self.sectors.get(sectorize(position), []):
            self.sectors[sectorize(position)].remove(position)
        if immediate and position in self.shown:
            self.hide_block(position)

    def show_block(self, position):
        if position in self.shown:
            return
        texture = self.world[position]
        self.shown[position] = texture
        vertex_data = cube_vertices(*position, 0.5)
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture))

    def hide_block(self, position):
        if position in self._shown:
            self._shown.pop(position).delete()
        if position in self.shown:
            del self.shown[position]

# --- Window ---
class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600, "Pyglet Game", resizable=True)
        self.exclusive = False
        self.flying = False
        self.strafe = [0,0]
        self.position = (0,0,0)
        self.rotation = (0,0)
        self.dy = 0
        self.inventory = [BRICK,GRASS,SAND]
        self.block = self.inventory[0]
        self.num_keys = [key._1,key._2,key._3]
        self.model = Model()
        self.label = pyglet.text.Label('', font_name='Arial', font_size=14,
            x=10, y=self.height-10, anchor_y='top', color=(0,0,0,255))
        self.reticle = None
        self.set_exclusive_mouse(True)
        pyglet.clock.schedule_interval(self.update, 1/TICKS_PER_SEC)

    def set_exclusive_mouse(self, exclusive):
        super().set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x-90)) * m
        dz = math.sin(math.radians(x-90)) * m
        return dx, dy, dz

    def get_motion_vector(self):
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            x_angle = math.radians(x + strafe)
            dx = math.cos(x_angle)
            dz = math.sin(x_angle)
            dy = 0.0
            if self.flying:
                dy = math.sin(math.radians(y))
            return dx, dy, dz
        return 0,0,0

    def update(self, dt):
        dx, dy, dz = self.get_motion_vector()
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        dx, dy, dz = dx*speed*dt, dy*speed*dt, dz*speed*dt
        if not self.flying:
            self.dy -= GRAVITY*dt
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy*dt
        x, y, z = self.position
        self.position = (x+dx, y+dy, z+dz)

    def on_draw(self):
        self.clear()
        self.set_3d()
        glColor3d(1,1,1)
        self.model.batch.draw()
        self.set_2d()
        self.label.text = f"Pos: {self.position}"
        self.label.draw()

    def set_2d(self):
        w, h = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        w, h = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, w/float(h), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y, z = self.position
        glRotatef(self.rotation[1], 1,0,0)
        glRotatef(self.rotation[0], 0,1,0)
        glTranslatef(-x,-y,-z)

    def on_key_press(self, symbol, modifiers):
        if symbol==key.W: self.strafe[0]-=1
        elif symbol==key.S: self.strafe[0]+=1
        elif symbol==key.A: self.strafe[1]-=1
        elif symbol==key.D: self.strafe[1]+=1
        elif symbol==key.SPACE and self.dy==0: self.dy=JUMP_SPEED
        elif symbol==key.TAB: self.flying=not self.flying
        elif symbol in self.num_keys:
            index = (symbol-self.num_keys[0])%len(self.inventory)
            self.block = self.inventory[index]

    def on_key_release(self, symbol, modifiers):
        if symbol==key.W: self.strafe[0]+=1
        elif symbol==key.S: self.strafe[0]-=1
        elif symbol==key.A: self.strafe[1]+=1
        elif symbol==key.D: self.strafe[1]-=1

# --- Setup ---
def setup_fog():
    glEnable(GL_FOG)
    color = (GLfloat*4)(0.5,0.69,1.0,1.0)
    glFogfv(GL_FOG_COLOR, color)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 10.0)
    glFogf(GL_FOG_END, 30.0)

def setup():
    glClearColor(0.5,0.69,1.0,1)
    glEnable(GL_CULL_FACE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()

# --- Main ---
def main():
    window = Window()
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
