import main

class World(main.Window):

  def add_block(x, y, z, texture):
    t = x, y, z
    textureToPass = texture
    if isinstance(texture, (basestring, int, float, long)):
      if isinstance(texture, basestring):
        texture.upper()
      if texture == "SAND" or texture == 1:
        textureToPass = main.SAND
      elif texture == "BRICK" or texture == 2:
        textureToPass = main.BRICK
      elif texture == "STONE" or texture == 3:
        textureToPass = main.STONE
      else:
        textureToPass = main.GRASS
    super.model.add_block(t, textureToPass)
  
  def remove_block(x, y, z):
    t = x, y, z
    super.model.remove_block(t)
  
  def set_block(x, y, z, texture):
    add_block(x, y, z, texture)
  
  def setFlying(fly):
    super.flying = fly
  
  #def setStrafe(forwardBack, leftRight):
    #World.strafe = [forwardBack, leftRight]
  
  def setPosition(x, y, z):
    super.position = (x, y, z)
  
  def setRotation(xz, ra):
    super.rotation = (xz, ra)

def run(world):
  if isinstance(world, (main.Window)):
    main.mainWindow(world)
