from __future__ import division

import math
import model
import player
import random
from states import GameState, StateMachine

#from collections import deque
from pyglet.gl import *  # noqa: F403


class Window(pyglet.window.Window):
    
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        # Initialize the state machine
        self.state_machine = StateMachine(GameState.MAIN_MENU)
        self.command_text = ""
        self.player_position = (0, 0, 0)  # Placeholder for player position
        
        self.command_text = ""
        self.player_position = (0, 0, 0)  # Placeholder for player position
        
        # Add states with their respective callbacks
        self.state_machine.add_state(
            GameState.MAIN_MENU,
            enter_callback=self.enter_main_menu,
            update_callback=self.update_main_menu
        )
        self.state_machine.add_state(
            GameState.PLAYING,
            enter_callback=self.enter_playing,
            update_callback=self.update_playing
        )
        self.state_machine.add_state(
            GameState.PAUSED,
            enter_callback=self.enter_paused,
            update_callback=self.update_paused
        )
        self.state_machine.add_state(
            GameState.COMMAND_LINE, 
            enter_callback=self.enter_command_mode, 
            exit_callback=self.exit_command_mode
        )
        self.state_machine.add_state(
            GameState.COMMAND_LINE, 
            enter_callback=self.enter_command_mode, 
            exit_callback=self.exit_command_mode
        )
        
        # Instance of the model that handles the world.
        self.model = model.Model()
        
        # Instance of the player that interacts with the world.
        self.player = player.Player(self.model, self, self.state_machine)

        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None
        
        self.gui_widgets = []

        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,  # noqa: F405
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))
        
        self.command_prompt_label = pyglet.text.Label(
            "Command: ",
            font_name="Arial",
            font_size=18,
            x=10, y=10,
            anchor_x="left", anchor_y="bottom",
            color=(255, 255, 255, 255)
        )

        self.create_main_menu()
        
        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / model.TICKS_PER_SEC)  # noqa: F405

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.state_machine.update(dt)  # Update the current state

        # Existing game logic
        self.model.process_queue()
        sector = model.sectorize(self.player.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in model.xrange(m):
            self.player.update(dt / m)

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.
        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)  # noqa: F405
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))  # noqa: F405
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Called by pyglet to draw the canvas.

        """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)  # noqa: F405
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()
        # Draw the background image first
        if self.state_machine.state == GameState.MAIN_MENU:
            self.background_sprite.draw()
        # Draw the UI elements (buttons, labels, etc.)
        if self.state_machine.state == GameState.MAIN_MENU:
            self.main_menu_batch.draw()
        elif self.state_machine.state == GameState.PAUSED:
            self.pause_menu_batch.draw()
        elif self.state_machine.state == GameState.COMMAND_LINE:
            self.command_batch.draw()
            
        elif self.state_machine.state == GameState.COMMAND_LINE:
            self.command_prompt_label.text = 'Command: ' + self.command_text
            self.command_batch.draw()
            self.command_prompt_label.draw()
            
    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        vector = self.player.get_sight_vector()
        block = self.player.hit_test(vector)[0]
        if block:
            x, y, z = block
            vertex_data = model.cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))  # noqa: F405
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # noqa: F405

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.player.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.draw()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)
    
    def setup_fog(self):
        """ Configure the OpenGL fog properties.
        """
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG) # noqa: F405
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1)) # noqa: F405
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE) # noqa: F405
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR) # noqa: F405
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, 20.0) # noqa: F405
        glFogf(GL_FOG_END, 60.0) # noqa: F405

    def setup(self):
        """ Basic OpenGL configuration.
        """
        # Set the color of "clear", i.e. the sky, in rgba.
        glClearColor(0.5, 0.69, 1.0, 1) # noqa: F405
        # Enable culling (not rendering) of back-facing facets -- facets that aren't
        # visible to you.
        glEnable(GL_CULL_FACE) # noqa: F405
        # Set the texture minification/magnification function to GL_NEAREST (nearest
        # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
        # "is generally faster than GL_LINEAR, but it can produce textured images
        # with sharper edges because the transition between texture elements is not
        # as smooth."
        self.setup_fog()

    def enter_main_menu(self):
        print("Entering Main Menu")
        self.create_main_menu()
        self.set_exclusive_mouse(False)
        # Unregister pause menu buttons (if necessary)
        for widget in self.gui_widgets:
            if widget._batch == self.pause_menu_batch:
                widget.enabled = False

    def update_main_menu(self, dt):
        # Handle input for the main menu (e.g., start game, quit)
        pass

    def enter_playing(self):
        print("Entering Playing State")
        self.set_exclusive_mouse(True)

    def update_playing(self, dt):
        # Handle game logic (e.g., player movement, block placement)
        pass
            
    def enter_paused(self):
        self.create_pause_menu()
        # Unregister main menu buttons (if necessary)
        for widget in self.gui_widgets:
            if widget._batch == self.main_menu_batch:
                widget.enabled = False

    def update_paused(self, dt):
        # Handle input for the pause menu (e.g., resume, quit)
        pass

    def create_pause_menu(self):
        # Create a container for the pause menu
        self.pause_menu_batch = pyglet.graphics.Batch()

        window_size = self.get_size()

        # Create images for the button states
        resume_depressed_image = pyglet.image.SolidColorImagePattern((100, 100, 100, 255)).create_image(150, 50)  # Gray
        resume_pressed_image = pyglet.image.SolidColorImagePattern((150, 150, 150, 255)).create_image(150, 50)  # Light gray
        quit_depressed_image = pyglet.image.SolidColorImagePattern((100, 100, 100, 255)).create_image(275, 50)  # Gray
        quit_pressed_image = pyglet.image.SolidColorImagePattern((150, 150, 150, 255)).create_image(275, 50)  # Light gray

        # Create a semi-transparent background
        self.background = pyglet.shapes.Rectangle(
            x=0, 
            y=0, 
            width=window_size[0], 
            height=window_size[1],
            color=(0, 0, 0), 
            batch=self.pause_menu_batch
        )
        self.background.opacity = 25

        # Create "PAUSED" label
        self.paused_label = pyglet.text.Label(
            "PAUSED",
            font_name="Arial",
            font_size=36,
            x=window_size[0] // 2,
            y=window_size[1] // 2 + 100,
            anchor_x="center",
            anchor_y="center",
            batch=self.pause_menu_batch
        )

        # Create "Resume" button
        self.resume_button = pyglet.gui.PushButton(
            x=window_size[0] // 2 - 75,
            y=window_size[1] // 2,
            pressed=resume_pressed_image,
            depressed=resume_depressed_image,
            batch=self.pause_menu_batch
        )
        self.resume_button_label = pyglet.text.Label(
            "Resume",
            font_name="Arial",
            font_size=24,
            x=self.resume_button.x + (self.resume_button.width // 2),
            y=self.resume_button.y + (self.resume_button.height // 2),
            anchor_x="center",
            anchor_y="center",
            batch=self.pause_menu_batch
        )
        self.resume_button.on_press = self.resume_button_pressed  # Set the callback

        # Create "Quit" button
        self.quittomain_button = pyglet.gui.PushButton(
            x=window_size[0] / 2 - 135,
            y=window_size[1] / 2 - 100,
            pressed=quit_pressed_image,
            depressed=quit_depressed_image,
            batch=self.pause_menu_batch,
        )
        self.quittomain_button_label = pyglet.text.Label(
            "Quit to Main Menu",
            font_name="Arial",
            font_size=24,
            x=self.quittomain_button.x + (self.quittomain_button.width // 2),
            y=self.quittomain_button.y + (self.quittomain_button.height // 2),
            anchor_x="center",
            anchor_y="center",
            batch=self.pause_menu_batch
        )
        self.quittomain_button.on_press = self.quittomain_button_pressed  # Set the callback

        # Add buttons to the GUI widgets list
        self.gui_widgets.extend([self.quittomain_button, self.resume_button])

    def resume_button_pressed(self):
        print("Resume button pressed")
        self.state_machine.change_state(GameState.PLAYING)

    def quittomain_button_pressed(self):
        self.state_machine.change_state(GameState.MAIN_MENU)

    def create_main_menu(self):
        # Create a container for the pause menu
        self.main_menu_batch = pyglet.graphics.Batch()

        window_size = self.get_size()

        # Create a semi-transparent background
        self.background_image = pyglet.image.load('MainMenu_background.jpg')
        self.background_sprite = pyglet.sprite.Sprite(self.background_image)
        self.background_sprite.scale_x = self.width / self.background_image.width
        self.background_sprite.scale_y = self.height / self.background_image.height

        # Create images for the button states
        resume_depressed_image = pyglet.image.SolidColorImagePattern((100, 100, 100, 255)).create_image(150, 50)  # Gray
        resume_pressed_image = pyglet.image.SolidColorImagePattern((150, 150, 150, 255)).create_image(150, 50)  # Light gray
        quit_depressed_image = pyglet.image.SolidColorImagePattern((100, 100, 100, 255)).create_image(275, 50)  # Gray
        quit_pressed_image = pyglet.image.SolidColorImagePattern((150, 150, 150, 255)).create_image(275, 50)  # Light gray

        self.splash_Text_label = pyglet.text.Label(
            "Now in Python!!!",
            font_name="Arial",
            font_size=36,
            x=window_size[0] // 2,
            y=window_size[1] // 2 + 100,
            anchor_x="center",
            anchor_y="center",
            batch=self.main_menu_batch
        )

        self.play_button = pyglet.gui.PushButton(
            x=window_size[0] // 2 - 75,
            y=window_size[1] // 2,
            pressed=resume_pressed_image,
            depressed=resume_depressed_image,
            batch=self.main_menu_batch
        )
        self.play_button_label = pyglet.text.Label(
            "Play",
            font_name="Arial",
            font_size=24,
            x=self.play_button.x + (self.play_button.width // 2),
            y=self.play_button.y + (self.play_button.height // 2),
            anchor_x="center",
            anchor_y="center",
            batch=self.main_menu_batch
        )
        self.play_button.on_press = self.play_button_pressed  # Set the callback

        # Create "Quit" button
        self.quit_button = pyglet.gui.PushButton(
            x=window_size[0] / 2 - 135,
            y=window_size[1] / 2 - 100,
            pressed=quit_pressed_image,
            depressed=quit_depressed_image,
            batch=self.main_menu_batch,
        )
        self.quit_button_label = pyglet.text.Label(
            "Quit to Desktop",
            font_name="Arial",
            font_size=24,
            x=self.quit_button.x + (self.quit_button.width // 2),
            y=self.quit_button.y + (self.quit_button.height // 2),
            anchor_x="center",
            anchor_y="center",
            batch=self.main_menu_batch
        )
        self.quit_button.on_press = self.quit_button_pressed  # Set the callback

        # Add buttons to the GUI widgets list
        self.gui_widgets.extend([self.quit_button, self.play_button])

    def play_button_pressed(self):
        print("Resume button pressed")
        self.state_machine.change_state(GameState.PLAYING)

    def quit_button_pressed(self):
            pyglet.app.exit()
            
    def enter_command_mode(self):
        self.command_text = ""
        self.create_command_line()
        print("Entered command mode. Type a command and press Enter.")

    def exit_command_mode(self):
        print("Exited command mode.")
        
    def create_command_line(self):
        # Create a container for the pause menu
        self.command_batch = pyglet.graphics.Batch()
        window_size = self.get_size()

        # Create a semi-transparent background
        self.background = pyglet.shapes.Rectangle(
            x=0, 
            y=0, 
            width=window_size[0], 
            height=window_size[1]/8,
            color=(0, 0, 0), 
            batch=self.command_batch
        )
        self.background.opacity = 25
        
        self.command_prompt_label = pyglet.text.Label(
            "Command: " + self.command_text,
            font_name="Arial",
            font_size=18,
            x=10, y=10,
            anchor_x="left", anchor_y="bottom",
            color=(255, 255, 255, 255),
            batch= self.command_batch
        )
        
    def on_text(self, text):
        """Handles text input in command mode."""
        if self.state_machine.state == GameState.COMMAND_LINE:
            self.command_text += text
            print(self.command_text)

    def process_command(self, command):
        """Processes player commands."""
        parts = command.split()
        if len(parts) == 4 and parts[0].lower() == "teleport":
            try:
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                self.player.position = (x, y, z)  # Move player
                print(f"Teleported to ({x}, {y}, {z})")
            except ValueError:
                print("Invalid coordinates!")
        else:
            print("Invalid command. Use: teleport x y z")
            
    def enter_command_mode(self):
        self.command_text = ""
        self.create_command_line()
        print("Entered command mode. Type a command and press Enter.")

    def exit_command_mode(self):
        print("Exited command mode.")
        
    def create_command_line(self):
        # Create a container for the pause menu
        self.command_batch = pyglet.graphics.Batch()
        window_size = self.get_size()

        # Create a semi-transparent background
        self.background = pyglet.shapes.Rectangle(
            x=0, 
            y=0, 
            width=window_size[0], 
            height=window_size[1]/8,
            color=(0, 0, 0), 
            batch=self.command_batch
        )
        self.background.opacity = 25
        
        
    def on_text(self, text):
        """Handles text input in command mode."""
        if self.state_machine.state == GameState.COMMAND_LINE:
            self.command_text += text
            print(self.command_text)

    def process_command(self, command):
        """Processes player commands."""
        parts = command.split()
        if len(parts) == 4 and parts[0].lower() == "teleport":
            try:
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                self.player.position = (x, y, z)  # Move player
                print(f"Teleported to ({x}, {y}, {z})")
            except ValueError:
                print("Invalid coordinates!")
        else:
            print("Invalid command. Use: teleport x y z")