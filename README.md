# Minecraft


This is a modded version of Fogleman's "Minecraft" which was created for an April Fools video.

https://github.com/fogleman/Minecraft

Video here: https://www.youtube.com/watch?v=S4EUQD9QIzc&lc=z23mubkgxpapjvhot04t1aokgeofqomvondp5x4qnz1abk0h00410


## How to Run

```shell
pip install pyglet
git clone https://github.com/Hopson97/Minecraft-In-5-Seconds.git
cd Minecraft-In-5-Seconds
python main.py
```

### Mac

On Mac OS X, you may have an issue with running Pyglet in 64-bit mode. Try running Python in 32-bit mode first:

```shell
arch -i386 python main.py
```

If that doesn't work, set Python to run in 32-bit mode by default:

```shell
defaults write com.apple.versioner.python Prefer-32-Bit -bool yes 
```

This assumes you are using the OS X default Python.  Works on Lion 10.7 with the default Python 2.7, and may work on other versions too.  Please raise an issue if not.
    
Or try Pyglet 1.2 alpha, which supports 64-bit mode:  

```shell
pip install https://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz 
```

### If you don't have pip or git

For pip:

- Mac or Linux: install with `sudo easy_install pip` (Mac or Linux) - or (Linux) find a package called something like 'python-pip' in your package manager.
- Windows: [install Distribute then Pip](http://stackoverflow.com/a/12476379/992887) using the linked .MSI installers.

For git:

- Mac: install [Homebrew](http://mxcl.github.com/homebrew/) first, then `brew install git`.
- Windows or Linux: see [Installing Git](http://git-scm.com/book/en/Getting-Started-Installing-Git) from the _Pro Git_ book.

See the [wiki](https://github.com/fogleman/Minecraft/wiki) for this project to install Python, and other tips.


[![Run on Repl.it](https://repl.it/badge/github/Hopson97/Minecraft-In-5-Seconds)](https://repl.it/github/Hopson97/Minecraft-In-5-Seconds)
