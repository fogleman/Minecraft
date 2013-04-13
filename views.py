from gui import *

class View(object):
    def __init__(self, controller):
        self.controller = controller
        self.batch = pyglet.graphics.Batch()

    def setup(self):
        pass

    def push_handlers(self):
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

    def on_draw(self):
        self.clear()
        glColor3d(1, 1, 1)
        self.controller.set_2d()
        self.batch.draw()
        
        
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
        self.start_game = Button(0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Start game", batch=self.batch, group=self.group, label_group=self.labels_group, on_click=self.controller.start_game_func, font_name='ChunkFive Roman')
        self.game_options = Button(0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Options...", batch=self.batch, group=self.group, label_group=self.labels_group, on_click=self.controller.game_options_func, font_name='ChunkFive Roman')
        self.exit_game = Button(0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Exit game", batch=self.batch, group=self.group, label_group=self.labels_group, on_click=self.controller.exit_game_func, font_name='ChunkFive Roman')
        self.buttons = [self.start_game, self.game_options, self.exit_game]
        self.label = Label(globals.APP_NAME, font_name='ChunkFive Roman', font_size=50, x=width/2, y=self.frame.y + self.frame.height,
            anchor_x='center', anchor_y='top', color=(255, 255, 255, 255), batch=self.batch,
            group=self.labels_group)
            
        self.on_resize(width, height)

    def on_mouse_press(self, x, y, button, modifiers):
        # maybe we can add a GUIManager to do the hit test automatically
        for button in self.buttons:
            if button.hit_test(x, y):
                button.on_mouse_click()

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

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x = 0
        self.background.y = 0
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
        self.button_return = Button(0, 0, 160, 50, image=button_image, image_highlighted=button_highlighted, caption="Done", batch=self.batch, group=self.group, label_group=self.labels_group, on_click=self.controller.main_menu_func, font_name='ChunkFive Roman')
        self.buttons = [self.button_return]
            
        self.on_resize(width, height)

    def on_mouse_press(self, x, y, button, modifiers):
        # maybe we can add a GUIManager to do the hit test automatically
        for button in self.buttons:
            if button.hit_test(x, y):
                button.on_mouse_click()

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

    def on_resize(self, width, height):
        self.background.scale = 1.0
        self.background.scale = max(float(width) / self.background.width, float(height) / self.background.height)
        self.background.x = 0
        self.background.y = 0
        self.frame.x, self.frame.y = (width - self.frame.width) / 2, (height - self.frame.height) / 2
        button_x = self.frame.x + (self.frame.width - self.button_return.width) / 2
        button_y = self.frame.y + (self.frame.height - self.button_return.height) / 2 - 130
        self.button_return.position = button_x, button_y
