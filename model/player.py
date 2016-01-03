""" Defines the character playing the game.
    What it's doing, where it's facing, what he's holding.
    """


class Player:

    def __init__(self):
        self.flying = False
        self.position = (0, 0, 0)
