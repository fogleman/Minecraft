# Minecraft

Simple Minecraft-inspired demo written in Python and Pyglet.

http://www.youtube.com/watch?v=kC3lwK631X8

## How to Run

    pip install pyglet
    git clone https://github.com/avelanarius/Minecraft.git
    cd Minecraft
    python main.py

### Mac

On Mac OS X, you may have an issue with running Pyglet in 64-bit mode. Try running Python in 32-bit mode first:

    arch -i386 python main.py

If that doesn't work, set Python to run in 32-bit mode by default:

    defaults write com.apple.versioner.python Prefer-32-Bit -bool yes 

This assumes you are using the OS X default Python.  Works on Lion 10.7 with the default Python 2.7, and may work on other versions too.  Please raise an issue if not.
    
Or try Pyglet 1.2 alpha, which supports 64-bit mode:  

    pip install https://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz 

### If you don't have pip or git

For pip:

- Mac or Linux: install with `sudo easy_install pip` (Mac or Linux) - or find a package called something like 'python-pip' in Linux and install in your package manager.
- Windows: [http://stackoverflow.com/a/12476379/992887](install Distribute then Pip) using the linked .MSI installers.

For git:

- Mac: install [Homebrew](http://mxcl.github.com/homebrew/) first, then `brew install git`.
- Windows or Linux: see [Installing Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) from the _Pro Git_ book.

See the [https://github.com/fogleman/Minecraft/wiki](wiki) for this project to install Python, and other tips.

## How to Play

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump / (in flying mode) fly
- Shift: (in flying mode) fly down
- Tab: toggle flying mode

### Building

- 1 - 9: Selecting item in inventory
- Mouse left-click: remove block
- Mouse right-click: create block

### GUI

- B / F3: Toggle UI
- V: Saving (save filename in command-line arguments)

### Quitting

- ESC: release mouse, then close window

### Command-line arguments
    usage: main.py [-h] [-width WIDTH] [-height HEIGHT] [-terrain TERRAIN]
                   [-hillheight HILLHEIGHT] [-flat FLAT] [--hide-fog] [--show-gui]
                   [--disable-auto-save] [-draw-distance {short,medium,long}]
                   [-save SAVE] [--disable-save]
    
    optional arguments:
      -h, --help            show this help message and exit
      -width WIDTH
      -height HEIGHT
      -terrain TERRAIN
      -hillheight HILLHEIGHT
      -flat FLAT
      --hide-fog
      --show-gui
      --disable-auto-save
      -draw-distance {short,medium,long}
      -save SAVE
      --disable-save