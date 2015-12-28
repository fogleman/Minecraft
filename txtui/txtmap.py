""" Draws an ascii version of the map"""


def draw(world, y=-1, x=0, z=0):

    for v in range(-10 + z, 10 + z):
        line = ''
        for h in range(-20 + x, 20 + x):
            key = (h, y, v)
            if key in world.model.keys():
                block = world.model[key]
                line += block.madeof[0]
            else:
                line += ' '
        print(line)
