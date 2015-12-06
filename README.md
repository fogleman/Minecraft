# mine.py (WIP)

A client gui to access Minecraft-compatible servers. (Work-in-progress)

This software connects to servers such as [cuberite](http://cuberite.org/) to provide them an interactive screen that ressembles Minecraft. It uses a middleware like [SpockBot](https://github.com/SpockBotMC/SpockBot) and generates images using code derived from [fogleman's Minecraft](https://github.com/fogleman/Minecraft).

This is the proposed architecture:

   Server (like cuberite)  
         |  
         |  
   Middleware (like SpockBot)  
         |  
         |  
    mine.py (this software)

## Roadmap

    - version 0.1.0 - commented, Python3, PEP8'd, working fork of fogleman's
    - version 0.1.1 - objected-oriented blocks definition (refactor)
    - version 0.1.2 - replace unittest with pytest
    - version 0.2.0 - reorganize code into classes (Block, World, Player...)
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
