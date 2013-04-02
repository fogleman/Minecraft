from pyglet.window import key


__all__ = (
    'MOVE_FORWARD', 'MOVE_BACKWARDS', 'MOVE_LEFT', 'MOVE_RIGHT', 'JUMP', 'FLY',
    'INVENTORY_KEYS', 'RELEASE_MOUSE'
)


MOVE_FORWARD = key.W
MOVE_BACKWARDS = key.S
MOVE_LEFT = key.A
MOVE_RIGHT = key.D

JUMP = key.SPACE
FLY = key.TAB

INVENTORY_KEYS = (
    key._1, key._2, key._3, key._4, key._5,
    key._6, key._7, key._8, key._9, key._0
)

RELEASE_MOUSE = key.ESCAPE
