class Entity(object):
    """
    Base class for players, mobs, TNT and so on.
    """
    def __init__(self, position, rotation, velocity = 0, health = 0):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.health = health
