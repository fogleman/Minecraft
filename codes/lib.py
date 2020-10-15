from __future__ import division

import sys
import math
import random
import time
import os
import re

from collections import deque
from pyglet import image
# from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
from codes import *


def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x-n, y+n, z-n, x-n, y+n, z+n, x+n, y+n, z+n, x+n, y+n, z-n,  # top
        x-n, y-n, z-n, x+n, y-n, z-n, x+n, y-n, z+n, x-n, y-n, z+n,  # bottom
        x-n, y-n, z-n, x-n, y-n, z+n, x-n, y+n, z+n, x-n, y+n, z-n,  # left
        x+n, y-n, z+n, x+n, y-n, z-n, x+n, y+n, z-n, x+n, y+n, z+n,  # right
        x-n, y-n, z+n, x+n, y-n, z+n, x+n, y+n, z+n, x-n, y+n, z+n,  # front
        x+n, y-n, z-n, x-n, y-n, z-n, x-n, y+n, z-n, x+n, y+n, z-n,  # back
    ]


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


def get_TEXTURES(main_path):
    png_re = re.compile(r'.*\\.png')
    folder_re = re.compile(r'.*\\..*')
    main_lists = os.listdir(main_path)
    png_list = []
    folder_list = []
    for dir in main_lists():
        if png_re.match(dir):
            png_list.append(dir)
        elif not(folder_re.match(dir)):
            folder_list.append(dir)
    return

def folder_open(path, open_all=False, re_match=None):
    """
    path
    """
    main_lists = os.listdir(path)
    get_items = []
    for dir in main_lists():
        if (re_match) and (re_match.match(dir)):
            get_items.append(dir)
            continue
        if (open_all) and (not(re.search(r'.*\\..*', dir))):
            print(path, dir)
            open_path = path.join('\\', dir)
            print(open_path)
            folder_open(open_path, open_all=True, re_match=re_match)
        else:
            pass
    return get_items

