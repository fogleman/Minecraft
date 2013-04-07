from pyglet.gl import *
from math import cos, sin, radians

class Camera3D(object):
    def __init__(self, target=None):
        self.target = target
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.x_rotation = 0.0
        self.y_rotation = 0.0

    def rotate(self, x, y):
        self.x_rotation = x
        self.y_rotation = y

    def update(self):
        if self.target:
            self.x, self.y, self.z = self.target.position

    def transform(self):
        glRotatef(self.x_rotation, 0, 1, 0)
        x_r = radians(self.x_rotation)
        glRotatef(-self.y_rotation, cos(x_r), 0, sin(x_r))
        glTranslatef(-self.x, -self.y, -self.z)
