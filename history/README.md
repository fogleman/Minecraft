It all started with [fogleman](https://github.com/fogleman/Minecraft). He built a beautiful clone of Minecraft using pyglet. It grew really nicely, but it didn't run on Python 3.

[ProgVal](https://github.com/ProgVal/Minecraft/tree/python3) solved that on a branch called "python3". That's what [ocarneiro](https://github.com/ocarneiro/mine.py) has forked, but he had no plans on working with python2, so he merged that into his master branch.

Trying to avoid [trademark issues](https://github.com/fogleman/Minecraft/issues/23), ocarneiro decided to change the name of the repo to "mine.py", as suggested on the original issue #23.

![](issue23-TrademarkIssues.png)

Trying to move the code further into fogleman's vision, ocarneiro was thinking how to build a detached world server API. But then he remembered [dockercraft](https://github.com/docker/dockercraft), which is a Minecraft-based Docker instances visualizer.

Dockercraft uses a FOSS (free and open source software) Minecraft-compatible server called [cuberite](http://cuberite.org/), so there's no need to reinvent the wheel here! How about plugging **mine.py**(this software) into cuberite? Let's see how it goes...

Turns out there's a lot of existing clients [documented here](http://wiki.vg/Client_List). It seems reasonable to use one of them to connect cuberite and mine.py.
