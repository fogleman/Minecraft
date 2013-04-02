# base class of players, mobs, TNT and so on
class Entity(object):
	def __init__(self, position, rotation, velocity = 0, health = 0):
		self.position = position
		self.rotation = rotation
		self.health = health
		self.velocity = 0

	
