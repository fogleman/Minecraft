# mine.py (WIP)

## Objective

A python implementation from scratch of the popular infinite world game Minecraft. (Work in progress)

This is a long endeavor that already was forked more than 600 times in [many different directions](https://github.com/fogleman/Minecraft/network).

## My take on it

I think the original code created by fogleman is genius work! To make it a fully functional API as he proposed in his vision, however, it needs a little help. I'm working on refactoring it to allow a more object-oriented code structure. The idea here is to isolate the logic into units that could be reused by other modules or projects.

You can read details of what I found in the [history/README.md](https://github.com/ocarneiro/mine.py/tree/master/history) file.

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

    git clone https://github.com/ocarneiro/mine.py
    cd mine.py
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

    python -i main.py
    
And then explore some of the objects already created. You can see an ASCII representation of the generated world, for instance:

    >>> txtmap.draw(world)

And if you want to see the same map using as references other heights (y=2, for instance), you can type:

    >>> txtmap.draw(world, 2)
    >>> # or #
    >>> txtmap.draw(world, y=2)
    
It's been a lot of fun to play with text representations of the blocks, so you should see more commits in this direction in the near future.

### Client GUI approach

This could grow into a client gui to access Minecraft-compatible servers.

This software would connect to servers such as [cuberite](http://cuberite.org/) to provide them an interactive screen that ressembles Minecraft. It uses a middleware like [SpockBot](https://github.com/SpockBotMC/SpockBot) and generates images using code derived from [fogleman's Minecraft](https://github.com/fogleman/Minecraft).

It could work in an architecture such as this:

   Server (like cuberite)  
         |  
         |  
   Middleware (like SpockBot)  
         |  
         |  
    mine.py (this software)
