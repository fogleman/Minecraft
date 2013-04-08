class Entity(object):
    """
    Base class for players, mobs, TNT and so on.
    """
    def __init__(self, position, rotation, velocity=0, health=0, max_health=0,
                 attack_power=0, sight_range=0, attack_range=0):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.health = health
        self.max_health = max_health
        # Attack power in hardness per second.  We will probably need to change
        # that later to include equiped weapon etc.
        self.attack_power = attack_power
        # Sight range is currently unusued - we probably want
        # it to check if monsters can see player
        self.sight_range = sight_range
        self.attack_range = attack_range
