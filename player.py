from __future__ import division

import sys
import mmath
import math
import inventory
import block
from model import Model
from states import GameState

from pyglet.gl import *  # noqa: F403
from pyglet.window import key, mouse

if sys.version_info[0] >= 3:
    xrange = range

class Player():
    def __init__(self, model: Model, window, statemachine, position = (80, 10, 80), *args, **kwargs):
        self.WALKING_SPEED = 5
        self.FLYING_SPEED = 15

        self.CurrentSpeed = 0

        self.GRAVITY = 20.0
        self.MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
        # To derive the formula for calculating jump speed, first solve
        #    v_t = v_0 + a * t
        # for the time at which you achieve maximum height, where a is the acceleration
        # due to gravity and v_t = 0. This gives:
        #    t = - v_0 / a
        # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
        #    s = s_0 + v_0 * t + (a * t^2) / 2
        self.JUMP_SPEED = math.sqrt(2 * self.GRAVITY * self.MAX_JUMP_HEIGHT)
        self.TERMINAL_VELOCITY = 50

        self.PLAYER_HEIGHT = 2
        
        self.inventory = inventory.Inventory()
        self.model = model
        self.window = window
        self.state_machine = statemachine
        self.window.push_handlers(self)
        
        # When flying gravity has no effect and speed is increased.
        self.flying = False
        
        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = position
        
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]
        
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        
        # Whether or not the window exclusively captures the mouse.
        self.exclusive = True
        
        # Velocity
        self.velocity = [0, 0, 0]
        
        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        
        # Running
        self.running = False
    
    def hit_test(self, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 8
        x, y, z = self.position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = mmath.normalize((x, y, z))
            if key != previous and key in self.model.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
    
    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)
    
    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """
        #print(self.strafe)
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
    
    
    
    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """

        if (self.state_machine.state == GameState.PLAYING):
            if self.exclusive:
                vector = self.get_sight_vector()
                selectedBlock, previous = self.hit_test(vector)
                if (button == mouse.RIGHT) or ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                    # ON OSX, control + left click = right click.
                    if previous:
                        self.model.add_block(previous, self.inventory.hotbar[self.inventory.index])
                elif button == pyglet.window.mouse.LEFT and selectedBlock:  # noqa: F405
                    texture = self.model.world[selectedBlock]
                    if texture != block.BEDROCK:
                        self.model.remove_block(selectedBlock)
                elif button == mouse.MIDDLE:
                    if previous:
                        texture = self.model.world[selectedBlock]
                        self.inventory.hotbar[self.inventory.index] = texture
        else:
            self.window.set_exclusive_mouse(True)
        if self.state_machine.state == GameState.PAUSED:
            # Pass the mouse press event only to widgets in the pause menu batch
            for widget in self.window.gui_widgets:
                if hasattr(widget, '_batch') and widget._batch == self.window.pause_menu_batch:
                    widget.on_mouse_press(x, y, button, modifiers)
        elif self.state_machine.state == GameState.MAIN_MENU:
            # Pass the mouse press event only to widgets in the main menu batch
            for widget in self.window.gui_widgets:
                if hasattr(widget, '_batch') and widget._batch == self.window.main_menu_batch:
                    widget.on_mouse_press(x, y, button, modifiers)
                    
    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if (self.state_machine.state == GameState.PLAYING):
            if self.exclusive:
                m = 0.15
                x, y = self.rotation
                x, y = x + dx * m, y + dy * m
                y = max(-90, min(90, y))
                self.rotation = (x, y)
        if self.state_machine.state == GameState.PAUSED:
            # Pass the mouse motion event to the GUI widgets
            for widget in self.window.gui_widgets:
                widget.on_mouse_motion(x, y, dx, dy)
        if self.state_machine.state == GameState.MAIN_MENU:
            # Pass the mouse motion event to the GUI widgets
            for widget in self.window.gui_widgets:
                widget.on_mouse_motion(x, y, dx, dy)
    
    def update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.
        """
        # walking
        speed = self.FLYING_SPEED if self.flying else self.WALKING_SPEED
        d = dt * speed * 2 if self.running else dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.velocity[1] -= dt * self.GRAVITY
            self.velocity[1] = max(self.velocity[1], -self.TERMINAL_VELOCITY)
            dy += self.velocity[1] * dt
        else:
            dy += self.velocity[1] * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.model.collide(self, (x + dx, y + dy, z + dz))
        self.position = (x, y, z)
    
    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.velocity[1] == 0:
                self.velocity[1] = self.JUMP_SPEED
        elif symbol == key.LSHIFT:
            if self.flying:
                self.velocity[1] = -self.JUMP_SPEED
        elif symbol == key.LCTRL:
            self.running = True
        elif symbol == key.ESCAPE:
            self.window.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory.hotbar)
            self.inventory.index = index

        if self.state_machine.state == GameState.PLAYING:
            if symbol == key.ESCAPE:
                self.window.set_exclusive_mouse(False)
                self.state_machine.change_state(GameState.PAUSED)
                return pyglet.event.EVENT_HANDLED
            if symbol == key.C:
                self.window.set_exclusive_mouse(True)
                self.state_machine.change_state(GameState.COMMAND_LINE)
        elif self.state_machine.state == GameState.PAUSED:
            if symbol == key.ESCAPE:
                self.window.set_exclusive_mouse(True)
                self.state_machine.change_state(GameState.PLAYING)
                return pyglet.event.EVENT_HANDLED
        elif self.state_machine.state == GameState.COMMAND_LINE:
            if symbol == key.BACKSPACE:
                self.command_text = self.window.command_text[:-1]
            elif symbol == key.ENTER: 
                self.window.process_command(self.window.command_text)
                self.state_machine.change_state(GameState.PLAYING)
                return pyglet.event.EVENT_HANDLED
    
    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.
        """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.LCTRL:
            self.running = False
        elif symbol == key.SPACE:
            if self.flying:
                self.velocity[1] = 0
        elif symbol == key.LSHIFT:
            if self.flying:
                self.velocity[1] = 0