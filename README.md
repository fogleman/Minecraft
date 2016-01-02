# Minecraft

## Objective

Simple Minecraft-inspired demo written in Python and Pyglet.

http://www.youtube.com/watch?v=kC3lwK631X8

This is a long endeavor that already was forked more than 600 times in [many different directions](https://github.com/fogleman/Minecraft/network).

**Like this project?**

You might also like my other Minecraft clone written in C using modern OpenGL (GL shader language). It performs better, has better terrain generation and saves state to a sqlite database. See here:

https://github.com/fogleman/Craft

## Goals and Vision

I would like to see this project turn into an educational tool. Kids love Minecraft and Python is a great first language.
This is a good opportunity to get children excited about programming.

The code should become well commented and more easily configurable. It should be easy to make some simple changes
and see the results quickly.

I think it would be great to turn the project into more of a library / API... a Python package that you import and then use / configure to setup a world and run it. Something along these lines...

    import mc
    
    world = mc.World(...)
    world.set_block(x, y, z, mc.DIRT)
    mc.run(world)

The API could contain functionality for the following:

- Easily configurable parameters like gravity, jump velocity, walking speed, etc.
- Hooks for terrain generation.

## Two different approaches

[main.py](main.py) is the original code created by fogleman. It's a showcase of the power and simplicity of Python. Having only 2 files, main.py and texture.png, you should be all set to run a complete version of this Minecraft clone.

[mine.py](mine.py) is intended to be the fully functional API proposed in the *Goals and Vision* section. It was refactored to be more object-oriented and easier to maintain and expand. With this version you should be able to use a text-based rendered version of the world generated. Read more about that below on the *Into the future* section.

You can read details about the evolution of this code in the [history/README.md](https://github.com/ocarneiro/mine.py/tree/master/history) file.

## Roadmap

    - version 0.1.0 - commented, Python3, PEP8'd, working fork of fogleman's (done!)
    - version 0.1.1 - objected-oriented blocks definition (refactor)  (done!)
    - version 0.1.2 - replace unittest with pytest
    - version 0.1.5 - reorganize code into classes (Block, World, Player...)
    - version 0.2.0 - text-based (ASCII) playable version
    - version 0.3.0 - connection to a server
    - version 0.4.0 - most basic blocks visible (wood, water, raw stone...)
    - version 0.5.0 - first working mob (an ugly cow, maybe)
    - version 1.0.0 - Working gui

## How to Run

    git clone https://github.com/fogleman/Minecraft.git
    cd Minecraft
    pip install -r requirements.txt
    python main.py

## How to Play

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window

## Into the future

### Text UI approach

You can run this game using 

    python -i mine.py
 
And then explore some of the objects already created. You can see an ASCII representation of the generated world, for instance:

    >>> txtmap.draw(world)

And if you want to see the same map using as references other heights (y=2, for instance), you can type:

    >>> txtmap.draw(world, 2)
    >>> # or #
    >>> txtmap.draw(world, y=2)
 
It's been a lot of fun to play with text representations of the blocks, so you should see more commits in this direction in the near future.

### Client GUI approach

This could grow into a client gui to access Minecraft-compatible servers.

This software would connect to servers such as [cuberite](http://cuberite.org/) to provide them an interactive screen that ressembles Minecraft. It would use a middleware like [SpockBot](https://github.com/SpockBotMC/SpockBot) and generate the corresponding images.

It could work in an architecture such as this:

   Server (like cuberite)
         |
         |
   Middleware (like SpockBot)
         |
         |
    mine.py (this software)
