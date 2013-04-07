from math import floor, ceil
import os

from pyglet.gl import *
from pyglet.window import key

from blocks import *
from crafting import *
from globals import *
from inventory import *
from items import *


class InventorySelector(object):
    def __init__(self, parent, player, model):
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)
        self.amount_labels_group = pyglet.graphics.OrderedGroup(2)
        self.amount_labels = []
        self.parent = parent
        self.model = model
        self.player = player
        self.max_items = self.player.inventory.slot_count
        self.current_index = 1
        self.icon_size = self.model.group.texture.width / TILESET_SIZE
        self.selected_item = None
        self.selected_item_icon = None
        image = pyglet.image.load(os.path.join('resources', 'textures', 'inventory.png'))
        self.frame = pyglet.sprite.Sprite(image.get_region(0, 0, image.width, image.height), batch=self.batch, group=pyglet.graphics.OrderedGroup(0))
        self.crafting_panel = Inventory(4)
        self.crafting_outcome = None  # should be an item stack
        self.crafting_outcome_icon = None
        #self.active = pyglet.sprite.Sprite(image.get_region(0, 0, image.height / 4, image.height / 4), batch=self.batch, group=pyglet.graphics.OrderedGroup(2))
        #self.active.opacity = 0
        self.frame.x = (parent.window.width - self.frame.width) / 2
        self.frame.y = self.icon_size / 2 - 4
        self.visible = False

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
                int(block.side_texture[0] * TILESET_SIZE) * self.icon_size,
                int(block.side_texture[1] * TILESET_SIZE) * self.icon_size, self.icon_size,
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
                int(block.side_texture[0] * TILESET_SIZE) * self.icon_size,
                int(block.side_texture[1] * TILESET_SIZE) * self.icon_size, self.icon_size,
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

        crafting_y = inventory_y + inventory_height + 42
        crafting_rows = 2
        crafting_height = (crafting_rows * (self.icon_size * 0.5)) + (crafting_rows * 3)
        x = self.frame.x + 165
        y = self.frame.y + crafting_y + crafting_height
        items = self.crafting_panel.get_items()
        items = items[:self.crafting_panel.slot_count]
        # NOTE: each line in the crafting panel should be a sub-list in the crafting ingredient list
        crafting_ingredients = [[], []]
        for i, item in enumerate(items):
            if not item:
                x += (self.icon_size * 0.5) + 3
                if x >= (self.frame.x + 165) + 67:
                    x = self.frame.x + 165
                    y -= (self.icon_size * 0.5) + 3
                continue
            block = BLOCKS_DIR[item.type]
            block_icon = self.model.group.texture.get_region(
                int(block.side_texture[0] * TILESET_SIZE) * self.icon_size,
                int(block.side_texture[1] * TILESET_SIZE) * self.icon_size, self.icon_size,
                self.icon_size)
            icon = pyglet.sprite.Sprite(block_icon, batch=self.batch,
                                        group=self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = y - icon.height
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            if x >= (self.frame.x + 165) + 67:
                x = self.frame.x + 165
                y -= (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name='Arial', font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=block.amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
            if block.id > 0:
                crafting_ingredients[int(floor(i / 2))].append(block)

        if len(crafting_ingredients) > 0:
            outcome = recipes.craft(crafting_ingredients)
            if outcome:
                self.set_crafting_outcome(outcome)
            elif self.crafting_outcome:
                self.remove_crafting_outcome()

        self.update_current()


    def update_current(self):
        '''self.active.x = self.frame.x + ((self.current_index % 9) * self.icon_size * 0.5) + (self.current_index % 9) * 3
        self.active.y = self.frame.y + floor(self.current_index / 9) * self.icon_size * 0.5 + floor(self.current_index / 9) * 6'''

    def get_current_block_item_and_amount(self):
        item = self.player.inventory.at(self.current_index)
        if item:
            amount = item.amount
            self.player.inventory.remove_by_index(self.current_index, quantity=item.amount)
            return item, amount
        return False

    def toggle(self):
        if not self.visible:
            self.update_items()
        self.parent.item_list.toggle()
        self.parent.window.set_exclusive_mouse(self.visible)
        self.visible = not self.visible

    def mouse_coords_to_index(self, x, y):
        inventory_rows = floor(self.max_items / 9)
        crafting_rows = 2
        quick_slots_y = self.frame.y + 4
        inventory_y = quick_slots_y + 42
        inventory_height = (inventory_rows * (self.icon_size * 0.5)) + (inventory_rows * 3)
        crafting_items_per_row = 2
        crafting_y = inventory_y + inventory_height + 42
        crafting_x = self.frame.x + 165
        crafting_height = (crafting_rows * (self.icon_size * 0.5)) + (crafting_rows * 3)
        crafting_width = (crafting_items_per_row * (self.icon_size * 0.5)) + (crafting_items_per_row-1) * 3

        crafting_outcome_y = inventory_y + inventory_height + 60
        crafting_outcome_x = self.frame.x + 270
        crafting_outcome_width = crafting_outcome_height = self.icon_size * 0.5
        # out of bound

        if (x <= self.frame.x + 7) or (x >= (self.frame.x + self.frame.width) - 7) or (y <= quick_slots_y) or y >= (crafting_y + crafting_height):
            return -1, -1

        x_offset = x - (self.frame.x + 7)

        if y <= quick_slots_y + 35:
            row = 0.0
            inventory = self.player.quick_slots
            items_per_row = 9
        elif y <= inventory_y + inventory_height and y >= inventory_y:
            y_offset = (y - (inventory_y + inventory_height)) * -1
            row = floor(y_offset // (self.icon_size * 0.5 + 3))
            self.crafting_panel.remove_unnecessary_stacks()
            inventory = self.player.inventory
            items_per_row = 9
        elif crafting_y <= y <= crafting_y + crafting_height and x >= crafting_x \
            and x <= crafting_x + crafting_width:
            y_offset = (y - (crafting_y + crafting_height)) * -1
            row = floor(y_offset // (self.icon_size * 0.5 + 3))
            self.crafting_panel.remove_unnecessary_stacks()
            inventory = self.crafting_panel
            x_offset = x - crafting_x
            items_per_row = crafting_items_per_row
        elif crafting_outcome_y <= y <= crafting_outcome_y + crafting_outcome_height and \
            crafting_outcome_x <= x <= crafting_outcome_x + crafting_outcome_width:
            return 0, 256   # 256 for crafting outcome
        else:
            return -1, -1

        col = x_offset // (self.icon_size * 0.5 + 3)

        return inventory, int(row * items_per_row + col)

    def set_crafting_outcome(self, item):
        if not item:
            self.remove_crafting_outcome()
            return
        self.crafting_outcome = item

        block = BLOCKS_DIR[item.type]
        item_icon = self.model.group.texture.get_region(int(block.side_texture[0] * TILESET_SIZE) * self.icon_size, int(block.side_texture[1] * TILESET_SIZE) * self.icon_size, int(self.icon_size * 0.5), int(self.icon_size * 0.5))
        self.crafting_outcome_icon = pyglet.sprite.Sprite(item_icon, batch=self.batch, group=self.group)
        inventory_rows = floor(self.max_items / 9)
        inventory_height = (inventory_rows * (self.icon_size * 0.5)) + (inventory_rows * 3)
        quick_slots_y = self.frame.y + 4
        inventory_y = quick_slots_y + 42
        self.crafting_outcome_icon.y = inventory_y + inventory_height + 60
        self.crafting_outcome_icon.x = self.frame.x + 270

    def remove_crafting_outcome(self):
        self.crafting_outcome = None
        self.crafting_outcome_icon = None

    def set_selected_item(self, item):
        if not item:
            self.remove_selected_item()
            return
        self.selected_item = item

        block = BLOCKS_DIR[item.type]
        item_icon = self.model.group.texture.get_region(int(block.side_texture[0] * TILESET_SIZE) * self.icon_size, int(block.side_texture[1] * TILESET_SIZE) * self.icon_size, self.icon_size, self.icon_size)
        self.selected_item_icon = pyglet.sprite.Sprite(item_icon, batch=self.batch, group=self.group)
        self.selected_item_icon.scale = 0.4

    def remove_selected_item(self):
        self.selected_item = None
        self.selected_item_icon = None

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.visible:
            return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.visible:
            return False
        if x < 0.0 or y < 0.0:
            return pyglet.event.EVENT_HANDLED
        inventory, index = self.mouse_coords_to_index(x, y)
        if index == 256:    # 256 for crafting outcome
            if self.crafting_outcome:
                self.remove_selected_item()
                # set selected_item to the crafting outcome so that users can put it in inventory
                self.set_selected_item(self.crafting_outcome)
                # set coordinates
                inventory_rows = floor(self.max_items / 9)
                inventory_height = (inventory_rows * (self.icon_size * 0.5)) + (inventory_rows * 3)
                quick_slots_y = self.frame.y + 4
                inventory_y = quick_slots_y + 42
                self.selected_item_icon.y = inventory_y + inventory_height + 60
                self.selected_item_icon.x = self.frame.x + 270
                # cost
                for ingre in self.crafting_panel.slots:
                    if ingre :
                        ingre.change_amount(-1)
                        # ingredient has been used up
                        if ingre.amount <= 0:
                            self.remove_crafting_outcome()
                self.crafting_panel.remove_unnecessary_stacks()
                return pyglet.event.EVENT_HANDLED
            else:   # nothing happens
                return pyglet.event.EVENT_HANDLED
        if self.selected_item:
            if index == -1:
                # throw it
                self.update_items()
                return pyglet.event.EVENT_HANDLED
            item = inventory.at(index)
            if (item and item.type == self.selected_item.type) or not item:
                amount_to_change = 1
                if button != pyglet.window.mouse.RIGHT:
                    amount_to_change = self.selected_item.amount
                if item:
                    remaining = item.change_amount(amount_to_change)
                else:
                    inventory.slots[index] = ItemStack(type=self.selected_item.type, amount=amount_to_change)
                    remaining = self.selected_item.amount - amount_to_change
                if remaining > 0:
                    self.selected_item.change_amount((self.selected_item.amount - remaining) * -1)
                else:
                    self.set_selected_item(None)
                self.update_items()
                return pyglet.event.EVENT_HANDLED
            inventory.slots[index] = self.selected_item
            self.set_selected_item(item)
            if self.selected_item_icon:
                self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
                self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)
        else:
            if index == -1:
                return pyglet.event.EVENT_HANDLED
            item = inventory.at(index)
            if not item:
                return pyglet.event.EVENT_HANDLED

            if modifiers & pyglet.window.key.MOD_SHIFT:
                add_to = self.player.quick_slots if inventory == self.player.inventory else self.player.inventory
                add_to.add_item(item.type, item.amount)
                inventory.remove_all_by_index(index)
                self.update_items()
                return pyglet.event.EVENT_HANDLED

            new_stack = False
            if button == pyglet.window.mouse.RIGHT:
                if item.amount > 1:
                    split_amount = int(ceil(item.amount / 2))
                    item.change_amount(split_amount * -1)
                    new_item = ItemStack(item.type, split_amount, item.durability, item.data)
                    self.set_selected_item(new_item)
                    new_stack = True

            if not new_stack:
                self.set_selected_item(item)
            if self.selected_item_icon:
                self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
                self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)

            if not new_stack:
                inventory.remove_all_by_index(index)

        self.update_items()
        self.update_current()
        return pyglet.event.EVENT_HANDLED

    def on_mouse_motion(self, x, y, dx, dy):
        if self.visible:
            if self.selected_item_icon:
                self.selected_item_icon.x = x - (self.selected_item_icon.width / 2)
                self.selected_item_icon.y = y - (self.selected_item_icon.height / 2)
            return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.visible:
            if button == pyglet.window.mouse.LEFT:
                self.on_mouse_motion(x, y, dx, dy)
            return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        if self.visible:
            if symbol == key.ESCAPE:
                self.toggle()
                return pyglet.event.EVENT_HANDLED
            elif symbol == key.ENTER:
                return pyglet.event.EVENT_HANDLED

    def on_resize(self, width, height):
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size / 2 - 4
        if self.visible:
            self.update_current()
            self.update_items()

    def draw(self):
        if self.visible:
            self.batch.draw()
            if self.selected_item_icon:
                self.selected_item_icon.draw()
            if self.crafting_outcome_icon:
                self.crafting_outcome_icon.draw()
