# PyCraft

---

### Getting started

You will need:
- A commandline terminal
- Python 3
- A text editor (e.g. Atom)
- The project source code (https://github.com/lukebrowell/Minecraft)
- Full OpenGL (The RaspberryPi-1 has OpenGL-ES which wont work here, and the RPi2/3 have a beta driver which I have not tested, for best results use a Mac or PC)

---
### Overview

The best way to learn to code, is to read code. This session introduces a stripped-down voxel world game, that looks a little like minecraft. It's been written in less than a thousand lines of code and we're going to start changing the way it works by changing just one line at a time and viewing the results.

---
## Excercises

---

### Activity 1

#### Setup

Please see the getting started guide for your machine

---
### Activity 2

#### The Flash

We want to make our in-game character move faster. Open the code in your text editor, read down the first page and see if you can guess which piece of code controls your character's speed.

Change it to a value not too different to the current and re-run the app from the commandline

e.g. py main.py

---
### Activity 3

#### Early Superman

In the early Superman graphic illustrations, Superman could not fly, instead he would jump between buildings. We want to make our character jump extra high. Read down the first page of code and see if you can guess what you will need to change to affect jump height.

Restart the game to see the effects.

---
### Activity 4
#### Fog of war

Batman uses cunning and special effects to confuse his adversaries. Hiding in the shadows and fog are one of his trademarks. Lets see if you can find the variables that control fog and dial it up.

Bonus activity - See if you can change the sky to be a darker shade.

Restart the game to see the effects.

---
### Activity 5
#### Graffiti 

The world we're using is far to clean to be a dystopian backdrop for our superheroes. Let see if we can add some graffiti to the voxels. Look in the folder, you should find a texture image, open it in sumo paint and use sumo paint to add your own tag to some of the blocks. 

Restart the game to see the effects.


---
### Activity 6
#### Add your own

The game stores the available block types, so you could extend it to have your own type. Remember to check for all the places where the block names are referenced by searching through your code. If you make a mistake, undo.

Restart the game to see the effects.

---

### Activity 7
#### Find the objects

The game is made up of objects. The objects have properties (things like the constants that you can change) and methods (things like your character's ability to jump). Skim through the code and see if you can find the methods that control how the game adds and removes blocks as you move around the game. Modify this code to create unusual behaviours.

---

### Project
#### Add a new feature to the game

It could be another block type, a new skin for all the textures or anthing else - you decide.