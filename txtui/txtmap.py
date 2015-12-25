""" Draws an ascii version of the map"""


def draw_line(world):
    y = 0  # on the floor
    x = 0  # center x
    z = 0  # center z

    for v in range(-10, 10):
        line = ''
        for h in range(-20, 20):
            key = (h, y, v)
            if key in world.model.keys():
                block = world.model[key]
                line += block.madeof[0]
            else:
                line += ' '
        print(line)
