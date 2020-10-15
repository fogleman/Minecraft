from codes import *


def place_block_update(position, world):
    """
    position : tuple of len 3
            The (x, y, z) position of the ben place block to update.
    """
    if (position[1] == 0) or (position[1] == 1):
        send_poi = position[0] -= 1, position[1], position[2]
        world[position[0] -= 1]
    world[]
    return


def remove_block_update(position, world):
    """
    position : tuple of len 3
            The (x, y, z) position of the ben remove block to update.
    """
    return
