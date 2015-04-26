import mc

world = mc.normal_world()
print(world.max_jump_height)
print(world.jump_speed)
world.set_max_jump_height(10)
print(world.max_jump_height)
print(world.jump_speed)
