
WORLD_SIZE = 160


class World:

    def __init__(self):
        # model is a dict with positions (x,y,z) as keys
        #   and blocks as values
        self.model = {}
        self.size = WORLD_SIZE
