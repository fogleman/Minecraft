# Minecraft

Simple Minecraft-inspired demo written in Python and Pyglet.

http://www.youtube.com/watch?v=kC3lwK631X8

## How to Run

    pip install pyglet
    git clone https://github.com/fogleman/Minecraft.git
    cd Minecraft
    python main.py

On Mac OS X, you may have an issue with running Pyglet in 64-bit mode. Try this...

    arch -i386 python main.py

## How to Play

Moving:

- W: forward
- S: back
- A: strafe left
- F: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

Building:
- selecting type of block to create:
    - 0: sand 
    - 1: grass 
    - 2: brick
- Mouse right-click: create block 
- Mouse left- click: remove block

Quitting:
- ESC: release mouse, then close window

