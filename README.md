# pyCraftr

![pyCraftr](https://raw.github.com/boskee/Minecraft/master/screenshot.png)

**Simple Minecraft-inspired demo written in Python and Pyglet.**

*http://www.youtube.com/watch?v=kC3lwK631X8*

## How to Run

    pip install pyglet
    git clone https://github.com/[current repository name]/Minecraft.git
    cd Minecraft
    python main.py

You may also need to install **AVBin library** (http://avbin.github.com/AVbin/Download.html), especially if you are on **Linux** machine. If you have **Windows** or **Linux** operating system, you will also need to install **OpenAL library** (http://connect.creativelabs.com/openal/default.aspx).

### Mac

On **Mac OS X**, you may have an issue with running **Pyglet in 64-bit mode**. Try running **Python in 32-bit mode** first:

    arch -i386 python main.py

If that doesn't work, set **Python to run in 32-bit mode by default**:

    defaults write com.apple.versioner.python Prefer-32-Bit -bool yes

This assumes you are **using the OS X default Python**. Works on **Lion 10.7 with the default Python 2.7**, and may work on other versions too. Please raise an issue if not.

Or try **Pyglet 1.2 alpha**, which **supports 64-bit mode**:

    pip install https://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz

### If you don't have pip or git

### Windows Pyglet builds
    See this website, and download the correct version for the OS.
    This is important to get this, as how it will have AVBin included with it.

    http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyglet
        For a 32 bit Windows Os, get the file named "pyglet-1.2alpha1.win32-py2.7.‌exe"
        For a 64 bit Windows Os, get the file named "pyglet-1.2alpha1.win-amd64-py2.7.‌exe"

For pip:

- **Mac or Linux**: install with `sudo easy_install pip` (Mac or Linux) or (Linux) find a package called something like 'python-pip' in your package manager.
- **Ubuntu**: install with `sudo apt-get install python-pip`
- **Windows**: [install Distribute then Pip](http://stackoverflow.com/a/12476379/992887) using the linked .MSI installers.

For git:

- **Mac**: install [Homebrew](http://mxcl.github.com/homebrew/) first, then `brew install git`.
- **Windows or Linux**: see [Installing Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) from the _Pro Git_ book.

*See the [wiki](https://github.com/fogleman/Minecraft/wiki) for this project to install Python, and other tips.*

## How to Play

### Moving

- **W**: forward
- **S**: back
- **A**: strafe left
- **D**: strafe right
- **Mouse**: look around
- **Space**: jump / (in flying mode) fly
- **Shift**: (in flying mode) fly down
- **Tab**: toggle flying mode

### Building

- **1 - 9**: Selecting item in inventory
- **Mouse left-click**: remove block
- **Mouse right-click**: create block

### GUI

- **B / F3**: Toggle UI
- **E**: Show inventory
- **V**: Saving (save filename in command-line arguments)
- **ENTER**: Move selected item to inventory / quick slots
- **Mouse left-click (in inventory)**: Pick up item and after second click put off last item
- **Mouse right-click** when not focused on block: Eat item

### Quitting

- **ESC** / **Q**: release mouse, then close window

## Better performance using Cython

For optimal performance, you can compile the code to C using Cython.

To do so, you have to install Cython and Python dev files
(`sudo apt-get install cython python-dev` under Ubuntu), then run
`python setup.py build_ext --inplace --force`.  You will have
to run this last command each time you update the game.

### Pyglet compilation

You can even automatically compile pyglet using Cython.  To do so, download
the pyglet source code and put the *pyglet* folder inside the game repository.
Compile the game as mentionned before, pyglet will be compiled and you should
have more FPS.

Note:
This compilation takes time and is not official.
