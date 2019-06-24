# Installing Minecraft for python!
If you want to install minecraft for python you are going to need some tools:
* git (a versioning software used for storing different versions of a program)
* A text editor (Visual Studio code, Vim, Emacs, Idle) that is used for modifying the code of the game
* Python the programming language used for creating this version of Minecraft
* Pyglet a special addon for Python.

----
## Installing Python:
To install python you need to download the installer from: [https://www.python.org/](https://www.python.org/)

![PICTURE OF PYTHON WEBSITE](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/PythonWebsite.PNG)

To install python we need to select the correct version for your computer.
Click on the `Downloads` button and you will be taken to a webpage that will select the correct version for you.
Click the `Download Python 3.6.5` button and it will automatically download the correct version for your operating system.
![PICTURE OF PYTHON DOWNLOADS PAGE](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/PythonDownloadButton.PNG)
You should be able to click through and agree to any agreements that are presented. If at any point you are asked if you would like to add the `Python PATH variable` click `YES`.
Once the installer has downloaded you can double click on it and the installer will open.

After the installer has completed close it.

---
## Installing Pyglet:
`Pyglet` is the special module used by python to allow the program to do all the maths needed to draw on the screen.
To install `Pyglet` we need to use a special part of python called `pip` which is the system that allows python to install additional modules.
You may have used a module in python such as `random` or `time` the only difference between `Pyglet` and `random` is that random comes pre-installed with python

To install `Pyglet` we need to open up a command prompt so `press the windows key (the one in the bottom left of the keyboard) and type cmd then open command prompt`
now a window should pop up

![image of cmd](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/CMDopenInDir.PNG)

Now type `python -m pip install pyglet` and press enter the computer will then collect the files for pyglet and install them to python for you.

![image of pyglet installing](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/InstallingPyglet.PNG)

---
## Installing Visual Studio Code:
If we want to modify a python file we need a program that can open those files and add to them
this is called a text editor / IDE Programmers use IDEs to help us ensure that we write code that is easy to use and to reduce the number of bugs.
Have you ever had a problem with a program and it turns out that all you did was mistype a word? IDEs sometimes help avoid that.

We are going to install `Visual Studio Code` because it is a useful tool that is free and easily accessible to everyone.
First you are going to need to download the installer from [https://code.visualstudio.com/](https://code.visualstudio.com/) there will be a large button
that says `Download for Windows` or `Download for mac`

![Image of Download button](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/VSCDL.PNG)

Click that link and allow the installer to download.
Next open the installer and just keep clicking next, it will install in the correct directory, be sure to agree to any agreements that are provided.

After you have finished installing Visual Studio Code should have opened.
![picture of visual studio code](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/VSCInstalled.PNG)
---
## Installing Git `Windows Only`:
Now we are going to install Git. Git is a piece of `Version Control Software` that programmers use to help them make sure that everyone who is working on a program has the correct version of the code
Git also allows the programmer to revert any changes that they have made if they perhaps break something or if they decide that they don't want to use the code that they have created.

First step in installing Git is to download it from [www.git-scm.com/download](www.git-scm.com/download) you will land on a page that will provide you with a download button

![Image of download button](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/GitDownload.PNG)

Click on that download button and allow the installer to download.

Now that the installer has downloaded you can launch it and click through the installer being sure to agree to any agreements provided.

---
## Downloading the source code for Minecraft:

Now we are going to use the Git that we just installed to download the source code for this version of Minecraft.

First we need to decide where we are going to download these files to. I suggest the desktop because it will be easily accessible.
Now Open that place in the file explorer

![Image of file explorer](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/DirOpenInFE.PNG)

In the top bar type `CMD` this will open up a command prompt in the current directory.
![IMAGE OF CURRENT DIR]()

Next type `git clone https://github.com/lukebrowell.com/minecraft` and press enter. Git will now collect the files from the website and store them on your system.
them on your computer.

You should now have a folder called `minecraft` the program files are in there.


So type `cd minecraft` in the command prompt window you can now type `python main.py` and the python version of Minecraft will open.

![Minecraft running](https://github.com/ScottHarwoodTech/Installing-MinecraftPy/blob/master/Images/Python%20running.PNG)
