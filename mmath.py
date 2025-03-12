from opensimplex import OpenSimplex
import random

gen = OpenSimplex(random.randrange(1, 10000))
def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2(nx, ny) / 2.0 + 0.5

def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def clamp(number, min, max):
    if number < min:
        return min
    elif number > max:
        return max
    else:
        return number