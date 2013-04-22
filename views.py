# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
# Nothing for now...

# Modules from this project
import globals as G
import os
from gui import *
from savingsystem import *


class View(pyglet.event.EventDispatcher):
    def __init__(self, controller):
        super(View, self).__init__()
        
        self.controller = controller
        self.batch = pyglet.graphics.Batch()

    def setup(self):
        pass

    def add_handlers(self):
        self.setup()
        self.controller.window.push_handlers(self)

    def pop_handlers(self):
        self.controller.window.set_mouse_cursor(None)
        self.controller.window.pop_handlers()
    
    def update(self, dt):
        pass

    def clear(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def on_mouse_press(self, x, y, button, modifiers):
        self.dispatch_event('on_mouse_click', x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        cursor = None
        for button in self.buttons:
            if button.highlighted:
                button.highlighted = False
                button.draw()
            if button.hit_test(x, y):
                button.highlighted = True
                button.draw()
                cursor = self.controller.window.get_system_mouse_cursor(pyglet.window.Window.CURSOR_HAND)
        self.controller.window.set_mouse_cursor(cursor)

    def on_draw(self):
        self.clear()
        glColor3d(1, 1, 1)
        self.controller.set_2d()
        self.batch.draw()
        
View.register_event_type('on_mouse_click')
        
        
class MainMenuView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        image = frame_image
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(backdrop, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
#            open_world(self, G.game_dir, G.SAVE_FILENAME)
        self.buttons = []
        if G.DISABLE_SAVE \
                and world_exists(G.game_dir, G.SAVE_FILENAME):
            self.continue_game = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Continue...", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
            self.continue_game.push_handlers(on_click=self.controller.start_game_func)
            self.buttons.append(self.continue_game)
            
        self.new_game = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="New game", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.new_game.push_handlers(on_click=self.controller.new_game_func)
        self.buttons.append(self.new_game)
        self.game_options = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Options...", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.game_options.push_handlers(on_click=self.controller.game_options_func)
        self.buttons.append(self.game_options)
        self.exit_game = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Exit game", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.exit_game.push_handlers(on_click=self.controller.exit_game_func)
        self.buttons.append(self.exit_game)
        self.label = Label(G.APP_NAME, font_name='ChunkFive Roman', font_size=50, x=width/2, y=self.frame.y + self.frame.height,
            anchor_x='center', anchor_y='top', color=(255, 255, 255, 255), batch=self.batch,
            group=self.labels_group)
            
        self.on_resize(width, height)

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x, self.background.y = 0, 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        self.label.y = self.frame.y + self.frame.height - 55
        self.label.x = width / 2
        button_x, button_y = 0, self.frame.y + (self.frame.height) / 2 + 10
        for button in self.buttons:
            button_x = self.frame.x + (self.frame.width - button.width) / 2
            button.position = button_x, button_y
            button_y -= button.height + 10
        
        
class OptionsView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        image = frame_image
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(backdrop, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        self.button_return = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_return.push_handlers(on_click=self.controller.main_menu_func)
        self.controls_button = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Controls...", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.controls_button.push_handlers(on_click=self.controller.controls_func)
        self.textures_button = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Textures", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.textures_button.push_handlers(on_click=self.controller.textures_func)
        self.buttons = [self.controls_button, self.textures_button, self.button_return]
            
        self.on_resize(width, height)

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x, self.background.y = 0, 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        button_x = self.frame.x + (self.frame.width - self.controls_button.width) / 2
        button_y = self.frame.y + (self.frame.height - self.controls_button.height) / 2 + 10
        self.controls_button.position = button_x, button_y
        button_y -= self.controls_button.height + 20
        self.textures_button.position = button_x, button_y
        button_y -= self.textures_button.height + 20
        self.button_return.position = button_x, button_y
        
        
class ControlsView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        image = frame_image
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(backdrop, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        self.buttons = []
        self.key_buttons = []
        key_buttons = ['move_backward', 'move_forward', 'move_left', 'move_right']
        for identifier in key_buttons:
            button = ToggleButton(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption=pyglet.window.key.symbol_string(getattr(G, identifier.upper() + '_KEY')), batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
            button.id = identifier
            self.buttons.append(button)
            self.key_buttons.append(button)
        self.button_return = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_return.push_handlers(on_click=self.controller.game_options_func)
        self.buttons.append(self.button_return)
            
        self.on_resize(width, height)

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x, self.background.y = 0, 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        default_button_x = button_x = self.frame.x + 30
        button_y = self.frame.y + (self.frame.height) / 2 + 10
        i = 0
        for button in self.key_buttons:
            button.position = button_x, button_y
            if i%2 == 0:
                button_x += button.width + 20
            else:
                button_x = default_button_x
                button_y -= button.height + 20
            i += 1
        button_x = self.frame.x + (self.frame.width - self.button_return.width) / 2
        self.button_return.position = button_x, button_y

    def on_key_press(self, symbol, modifiers):
        active_button = None
        for button in self.buttons:
            if isinstance(button, ToggleButton) and button.toggled:
                active_button = button
                break
                
        if not active_button:
            return
            
        active_button.caption = pyglet.window.key.symbol_string(symbol)
        active_button.toggled = False

        G.config.set("Controls", active_button.id, pyglet.window.key.symbol_string(symbol))

        with open(G.config_file, 'wb') as handle:
            G.config.write(handle)
        
        
class TexturesView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        image = frame_image
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(backdrop, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        self.buttons = []
        self.texture_buttons = []
        
        button = ToggleButton(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption='Default', batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        button.id = 'default'
        self.buttons.append(button)
        self.texture_buttons.append(button)
            
        texturepacks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'texturepacks')
        
        for directories in os.listdir(texturepacks_dir): 
            dir = os.path.join(texturepacks_dir, directories)
            pack_name = os.path.basename(dir)
        
            button = ToggleButton(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption=pack_name, batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
            button.id = pack_name
            self.buttons.append(button)
            self.texture_buttons.append(button)
        self.button_return = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_return.push_handlers(on_click=self.controller.game_options_func)
        self.buttons.append(self.button_return)
            
        self.on_resize(width, height)

    def on_mouse_press(self, x, y, button, modifiers):
        super(TexturesView, self).on_mouse_press(x, y, button, modifiers)
        for button in self.texture_buttons:
            if button.toggled:
                G.config.set("Graphics", "texture_pack", button.id)
                G.TEXTURE_PACK = button.id
                for block in G.BLOCKS_DIR.values():
                    block.__init__() #Reload textures

                with open(G.config_file, 'wb') as handle:
                    G.config.write(handle)
                    
                button.toggled = False

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x, self.background.y = 0, 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        button_x = button_x = self.frame.x + (self.frame.width - self.texture_buttons[0].width) / 2
        button_y = self.frame.y + (self.frame.height) / 2 + 10
        for button in self.texture_buttons:
            button.position = button_x, button_y
            button_y -= button.height + 20
        self.button_return.position = button_x, button_y
