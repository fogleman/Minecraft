# Minecraft

Simple Minecraft-inspired demo written in Python and Pyglet.

http://www.youtube.com/watch?v=kC3lwK631X8

## How to Run

    pip install pyglet
    git clone https://github.com/fogleman/Minecraft.git
    cd Minecraft
    python main.py

On Mac OS X, you may have an issue with running Pyglet in 64-bit mode. Try running Python in 32-bit mode first.

    arch -i386 python main.py

Or, try Pyglet 1.2 which supports 64-bit mode.

    pip install https://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz 

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
