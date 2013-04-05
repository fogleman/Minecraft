from pyglet.gl import *
from math import floor
from blocks import *

class InventorySelector(object):
    def __init__(self, width, height, player, model):
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)
        self.amount_labels_group = pyglet.graphics.OrderedGroup(2)
        self.amount_labels = []
        self.model = model
        self.player = player
        self.max_items = 27
        self.current_index = 1
        self.icon_size = self.model.group.texture.width / 8 #4
        self.selected_item = None
        self.selected_item_icon = None
        image = pyglet.image.load('inventory.png')
        self.frame = pyglet.sprite.Sprite(image.get_region(0, 0, image.width, image.height), batch=self.batch, group=pyglet.graphics.OrderedGroup(0))
        #self.active = pyglet.sprite.Sprite(image.get_region(0, 0, image.height / 4, image.height / 4), batch=self.batch, group=pyglet.graphics.OrderedGroup(2))
        #self.active.opacity = 0
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size + 20 # 20 is padding

    def change_index(self, change):
        self.set_index(self.current_index + change)

    def set_index(self, index):
        index = int(index)
        if self.current_index == index:
            return
        self.current_index = index
        if self.current_index >= self.max_items:
            self.current_index = 0
        elif self.current_index < 0:
            self.current_index = self.max_items - 1
        self.update_current()

    def update_items(self):
        rows = floor(self.max_items / 9)
        inventory_y = 43
        inventory_height = (rows * (self.icon_size * 0.5)) + ((rows+1) * 3)
        self.icons = []
        for amount_label in self.amount_labels:
            amount_label.delete()
        self.amount_labels = []
        x = self.frame.x + 7
        y = self.frame.y + inventory_y + inventory_height
        items = self.player.inventory.get_items()
        items = items[:self.max_items]
        for i, item in enumerate(items):
            if not item:
                x += (self.icon_size * 0.5) + 3
                if x >= (self.frame.x + self.frame.width) - 7:
                    x = self.frame.x + 7
                    y -= (self.icon_size * 0.5) + 3
                continue
            block = BLOCKS_DIR[item.type]
            block_icon = self.model.group.texture.get_region(
                int(block.side_texture[0] * 8) * self.icon_size,
                int(block.side_texture[1] * 8) * self.icon_size, self.icon_size,
                self.icon_size)
            icon = pyglet.sprite.Sprite(block_icon, batch=self.batch,
                                        group=self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = y - icon.height
            x += (self.icon_size * 0.5) + 3
            if x >= (self.frame.x + self.frame.width) - 7:
                x = self.frame.x + 7
                y -= (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name='Arial', font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=block.amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
            
        items = self.player.quick_slots.get_items()
        items = items[:self.player.quick_slots.slot_count]
        for i, item in enumerate(items):
            if not item:
                x += (self.icon_size * 0.5) + 3
                continue
            block = BLOCKS_DIR[item.type]
            block_icon = self.model.group.texture.get_region(
                int(block.side_texture[0] * 8) * self.icon_size,
                int(block.side_texture[1] * 8) * self.icon_size, self.icon_size,
                self.icon_size)
            icon = pyglet.sprite.Sprite(block_icon, batch=self.batch,
                                        group=self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = self.frame.y + 7
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name='Arial', font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=block.amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
        self.update_current()

        
    def update_current(self):
        '''self.active.x = self.frame.x + ((self.current_index % 9) * self.icon_size * 0.5) + (self.current_index % 9) * 3
        self.active.y = self.frame.y + floor(self.current_index / 9) * self.icon_size * 0.5 + floor(self.current_index / 9) * 6'''
        
    def set_position(self, width, height):
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size + 20 # 20 is padding
        self.update_current()
        self.update_items()

    def get_current_block_item_and_amount(self):
        item = self.player.inventory.at(self.current_index)
        if item:
            amount = item.amount
            self.player.inventory.remove_by_index(self.current_index, quantity=item.amount)
            return item, amount
        return False

    def toggle_active_frame_visibility(self):
        '''self.active.opacity = 0 if self.active.opacity == 255 else 255'''

    def mouse_coords_to_index(self, x, y):
        rows = floor(self.max_items / 9)
        quick_slots_y = self.frame.y + 4
        inventory_y = quick_slots_y + 42
        inventory_height = (rows * (self.icon_size * 0.5)) + (rows * 3)
        # out of bound
        
        if (x <= self.frame.x + 7) or (x >= (self.frame.x + self.frame.width) - 7) or (y <= quick_slots_y) or y >= (inventory_y + inventory_height):
            return -1, -1

        x_offset = x - (self.frame.x + 7)

        if y >= inventory_y:
            y_offset = (y - (inventory_y + inventory_height)) * -1
            row = floor(y_offset // (self.icon_size * 0.5 + 3))
            inventory = self.player.inventory
        elif y <= quick_slots_y + 35:
            row = 0.0
            inventory = self.player.quick_slots
        else:
            return -1, -1

        col = x_offset // (self.icon_size * 0.5 + 3)
        
        return inventory, int(row * 9 + col)

    def set_selected_item(self, item):
        if not item:
            self.remove_selected_item()
            return
        self.selected_item = item

        block = BLOCKS_DIR[item.type]
        item_icon = self.model.group.texture.get_region(int(block.side_texture[0] * 8) * self.icon_size, int(block.side_texture[1] * 8) * self.icon_size, self.icon_size, self.icon_size)
        self.selected_item_icon = pyglet.sprite.Sprite(item_icon, batch=self.batch, group=self.group)
        self.selected_item_icon.scale = 0.4

    def remove_selected_item(self):
        self.selected_item = None
        self.selected_item_icon = None

    def on_mouse_press(self, x, y, button):
        if x < 0.0 or y < 0.0:
            return False
        inventory, index = self.mouse_coords_to_index(x, y)
        if self.selected_item:
            if index == -1:
                # throw it
                self.update_items()
                return False
            item = inventory.at(index)
            inventory.slots[index] = self.selected_item
            self.set_selected_item(item)
            if self.selected_item_icon:
                self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
                self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)
        else:
            if index == -1:
                return False
            item = inventory.at(index)
            if not item:
                return True

            self.set_selected_item(item)
            if self.selected_item_icon:
                self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
                self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)

            inventory.remove_all_by_index(index)

        self.update_items()
        self.update_current()
        return True

    def on_mouse_motion(self, x, y, dx, dy):
        if self.selected_item_icon:
            self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
            self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)
            return

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.selected_item_icon:
            self.on_mouse_motion(x, y, dx, dy)
