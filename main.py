# from window import Window
# from pyglet import image
# from pyglet.gl import *  # noqa: F403
# from pyglet.graphics import TextureGroup
import window
from pyglet.gl import *  # noqa: F403

def main():
    userWindow = window.Window(width=1280, height=720, caption='Py Minecraft', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    userWindow.set_exclusive_mouse(False)
    userWindow.setup()
    pyglet.app.run() # noqa: F405

if __name__ == '__main__':
    main()
    
