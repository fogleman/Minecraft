from gui import *

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

        background = load_image('resources', 'textures', 'main_menu_background.png')
        image = load_image('resources', 'textures', 'frame.png')
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(background, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        button_image = load_image('resources', 'textures', 'button.png')
        button_highlighted = load_image('resources', 'textures', 'button_highlighted.png')
        self.start_game = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Start game", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.start_game.push_handlers(on_click=self.controller.start_game_func)
        self.game_options = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Options...", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.game_options.push_handlers(on_click=self.controller.game_options_func)
        self.exit_game = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Exit game", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.exit_game.push_handlers(on_click=self.controller.exit_game_func)
        self.buttons = [self.start_game, self.game_options, self.exit_game]
        self.label = Label(globals.APP_NAME, font_name='ChunkFive Roman', font_size=50, x=width/2, y=self.frame.y + self.frame.height,
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
        button_x = self.frame.x + (self.frame.width - self.start_game.width) / 2
        button_y = self.frame.y + (self.frame.height - self.start_game.height) / 2 + 10
        self.start_game.position = button_x, button_y
        button_y -= self.start_game.height + 20
        self.game_options.position = button_x, button_y
        button_y -= self.game_options.height + 20
        self.exit_game.position = button_x, button_y
        
        
class OptionsView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        background = load_image('resources', 'textures', 'main_menu_background.png')
        image = load_image('resources', 'textures', 'frame.png')
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(background, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        button_image = load_image('resources', 'textures', 'button.png')
        button_highlighted = load_image('resources', 'textures', 'button_highlighted.png')
        self.button_return = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_return.push_handlers(on_click=self.controller.main_menu_func)
        self.controls_button = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Controls...", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.controls_button.push_handlers(on_click=self.controller.controls_func)
        self.buttons = [self.controls_button, self.button_return]
            
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
        self.button_return.position = button_x, button_y
        
        
class ControlsView(View):
    def setup(self):
        self.group = pyglet.graphics.OrderedGroup(2)
        self.labels_group = pyglet.graphics.OrderedGroup(3)

        width, height = self.controller.window.width, self.controller.window.height

        background = load_image('resources', 'textures', 'main_menu_background.png')
        image = load_image('resources', 'textures', 'frame.png')
        self.frame_rect = Rectangle(0, 0, image.width, image.height)
        self.background = image_sprite(background, self.batch, 0)
        self.background.scale = max(float(self.controller.window.get_size()[0]) / self.background.width, float(self.controller.window.get_size()[1]) / self.background.height)
        self.frame = image_sprite(image, self.batch, 1)
        button_image = load_image('resources', 'textures', 'button.png')
        button_highlighted = load_image('resources', 'textures', 'button_highlighted.png')
        self.button_attack = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Attack", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_attack.push_handlers(on_click=self.capture_key_func)
        self.button_return = Button(self, 0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, font_name='ChunkFive Roman')
        self.button_return.push_handlers(on_click=self.controller.game_options_func)
        self.buttons = [self.button_attack, self.button_return]
            
        self.on_resize(width, height)

    def capture_key_func(self):
        pass

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x, self.background.y = 0, 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        button_x = self.frame.x + (self.frame.width - self.button_attack.width) / 2
        button_y = self.frame.y + (self.frame.height - self.button_attack.height) / 2 + 10
        self.button_attack.position = button_x, button_y
        button_y -= self.button_attack.height + 20
        self.button_return.position = button_x, button_y
