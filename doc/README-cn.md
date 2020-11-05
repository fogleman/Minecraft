[English]()

# 此文档为机翻+部分手动修改，有建议请发中文issue并标明[README-cn]

# Minecraft

以Python和Pyglet编写的受Minecraft启发的简单演示。

http://www.youtube.com/watch？v=kC3lwK631X8

这是皮申杰克元杰

**像这个项目？**

您可能也喜欢我的另一个Minecraft克隆，使用现代OpenGL（GL着色器语言）用C编写。它的性能更好，有更好的地形生成，并将状态保存到sqlite数据库中。请看这里：

https://github.com/fogleman/Craft

## 目标和愿景

我希望这个项目变成一个教育工具。孩子们喜欢Minecraft，Python是很棒的第一语言。

这是一个让孩子们对编程感到兴奋的好机会。

代码应该得到很好的注释，并且更容易配置。做一些简单的改变应该很容易

很快就能看到结果。

我认为把这个项目变成一个库/API会很棒。。。导入一个Python包，然后

使用/configure设置一个世界并运行它。沿着这些线索。。。

```python
import mc

world = mc.World(...)
world.set_block(x, y, z, mc.DIRT)
mc.run(world)
```

API可以包含以下功能：

-容易配置的参数，如重力，跳跃速度，步行速度等。

-地形生成挂钩。

##怎么跑

```shell
pip install pyglet
git clone https://github.com/fogleman/Minecraft.git
cd Minecraft
python main.py
```

### Mac

在Mac OS X上，在64位模式下运行Pyglet可能有问题。请先尝试在32位模式下运行Python：

```shell
arch -i386 python main.py
```

如果不起作用，请将Python默认设置为以32位模式运行：

```shell
defaults write com.apple.versioner.python Prefer-32-Bit -bool yes 
```

这假设您使用的是OSX默认Python。可以在Lion10.7上使用默认的Python2.7，也可以在其他版本上使用。如果没有，请提出问题。

或者试试Pyglet 1.2 alpha，它支持64位模式：

```shell
pip install https://pyglet.googlecode.com/files/pyglet-1.2alpha1.tar.gz 
```

### 如果你没有pip或git

对于pip：

-在Linux软件包中安装类似于Linux的pip或者类似于pip的软件包。

-Windows:[安装分发然后Pip](http://stackoverflow.com/a/12476379/992887)使用链接的.MSI安装程序。

对于git：

-Mac:安装[自制](homebrew网站http://mxhub.com/)首先，然后是“brew install git”。

-Windows或Linux：请参阅[安装Git](http://git-scm.com/book/en/Getting-Started-Installing-git)从你的专业博客上。

[见维基](https://github.com/fogleman/Minecraft/wiki)为这个项目安装Python等提示。

## 怎么玩

### 移动

-W：前进
-S：后退
-A：向左
-D：向右

-鼠标移动：看看周围
-空格：跳跃
-Tab：切换飞行模式

### 建筑

-选择要创建的块类型：
    -1:砖
    -2:草
    -3:沙子

-鼠标左键单击：删除块

-鼠标右键单击：创建块

### 退出

-释放鼠标，然后关闭窗口
