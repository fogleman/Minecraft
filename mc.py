import main

GRASS = main.GRASS
SAND = main.SAND
BRICK = main.BRICK
STONE = main.STONE

class World (main.Window):

  def __init__(self):
    main.Window.__init__(self, width=800, height=600, caption='Pyglet', resizable=True)
  
  def add_block(self, x, y, z, texture):
    position = (x, y - 1, z)
    if isinstance(texture, (str, int, float, long)):
      if isinstance(texture, str):
        texture = texture.upper()
      if texture == "SAND" or texture == 1:
        texture = SAND
      elif texture == "BRICK" or texture == 2:
        texture = BRICK
      elif texture == "STONE" or texture == 3:
        texture = STONE
      else:
        texture = GRASS
    self.model.add_block(position, texture)
  
  def remove_block(self, x, y, z):
    position = (x, y - 1, z)
    self.model.remove_block(position)
  
  def set_block(self, x, y, z, texture):
    self.add_block(x, y, z, texture)

def run(world):
  if isinstance(world, main.Window):
    main.main_window(world)
    
def normal_world():
  main.main()