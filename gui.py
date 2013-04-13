from math import floor, ceil
import os

from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.gl import *
from pyglet.window import key

from blocks import *
from crafting import *
import globals
from inventory import *
from items import *
from utils import load_image, image_sprite, hidden_image_sprite, get_block_icon

class Rectangle(object):
    def __init__(self, x, y, width, height):
        self.position = x, y
        self.size = width, height

    def hit_test(self, x, y):
        return (x >= self.min[0] and x <= self.max[0]) and (y >= self.min[1] and y <= self.max[1])

    def vertex_list(self):
        return [self.x, self.y,
                self.x + self.width, self.y,
                self.x + self.width, self.y + self.height,
                self.x, self.y + self.height]

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, position):
        self.x, self.y = position

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, size):
        self.width, self.height = size

    @property
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    @property
    def min(self):
        return (self.x, self.y)

    @property
    def max(self):
        return (self.x + self.width, self.y + self.height)

class Button(pyglet.event.EventDispatcher, Rectangle):
    def __init__(self, parent, x, y, width, height, image=None, image_highlighted=None, caption=None, batch=None, group=None, label_group=None, font_name=globals.DEFAULT_FONT):
        super(Button, self).__init__(x, y, width, height)
        parent.push_handlers(self)
        self.batch, self.group, self.label_group = batch, group, label_group
        self.sprite = image_sprite(image, self.batch, self.group)
        self.sprite_highlighted = hidden_image_sprite(image_highlighted, self.batch, self.group)
        self.highlighted = False
        self.label = Label(str(caption), font_name, 12, anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255), batch=self.batch, group=self.label_group) if caption else None
        self.position = x, y

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, position):
        self.x, self.y = position
        if hasattr(self, 'sprite') and self.sprite:
            self.sprite.x, self.sprite.y = position
        if hasattr(self, 'sprite_highlighted') and self.sprite_highlighted:
            self.sprite_highlighted.x, self.sprite_highlighted.y = position
        if hasattr(self, 'label') and self.label:
            self.label.x, self.label.y = self.center

    def draw(self):
        self.draw_sprite()
        self.draw_label()

    def draw_sprite(self):
        if self.sprite and not (self.sprite_highlighted and self.highlighted):
            self.sprite_highlighted.visible, self.sprite.visible = False, True
            self.sprite.draw()
        elif self.sprite_highlighted and self.highlighted:
            self.sprite_highlighted.visible, self.sprite.visible = True, False
            self.sprite_highlighted.draw()

    def draw_label(self):
        if self.label:
            self.label.draw()

    def on_mouse_click(self, x, y, button, modifiers):
        if self.hit_test(x, y):
            self.dispatch_event('on_click')

Button.register_event_type('on_click')

class Control(object):
    def __init__(self, parent, anchor_style=globals.ANCHOR_NONE, visible=True, *args, **kwargs):
        self.parent = parent
        self.visible = visible
        self.anchor_style = anchor_style
        self._anchor_points = (None,) * 4

    def toggle(self):
        self.visible = not self.visible
        self._on_toggled()

    def draw(self):
        if self.visible:
            self._on_draw()

    def _on_resize(self):
        pw, ph = self.parent.window.get_size()
        al, at, ar, ab = None, None, None, None
        if (self.anchor_style & globals.ANCHOR_RIGHT) == globals.ANCHOR_RIGHT:
            ar = pw
        if (self.anchor_style & globals.ANCHOR_BOTTOM) == globals.ANCHOR_BOTTOM:
            ab = 0
        # TODO: Implement ANCHOR_LEFT and ANCHOR_TOP
        self._anchor_points = (al, at, ar, ab)

    def _on_toggled(self):
        pass

    def _on_draw(self):
        pass

class AbstractInventory(Control):
    def __init__(self, parent, *args, **kwargs):
        self._current_index = 0
        self.parent = parent

    @property
    def current_index(self):
        return int(self._current_index)

    @current_index.setter
    def current_index(self, value):
        self._current_index = value % self.max_items
        self.update_current()

class ItemSelector(AbstractInventory):
    def __init__(self, parent, player, model, *args, **kwargs):
        super(ItemSelector, self).__init__(parent, *args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)
        self.labels_group = pyglet.graphics.OrderedGroup(2)
        self.amount_labels = []
        self.model = model
        self.player = player
        self.max_items = 9
        self.icon_size = self.model.group.texture.width / globals.TILESET_SIZE
        self.visible = True
        self.num_keys = [getattr(globals, 'INVENTORY_%d_KEY' % i)
                         for i in range(1, 10)]

        image = load_image('resources', 'textures', 'slots.png')
        heart_image = load_image('resources', 'textures', 'heart.png')
        frame_size = image.height / 2
        self.frame = image_sprite(image, self.batch, 0, y=frame_size, height=frame_size)
        self.active = image_sprite(image, self.batch, 2, width=frame_size, height=frame_size)
        self.hearts = []
        for i in range(0, 10):
            heart = image_sprite(heart_image, self.batch, 0)
            self.hearts.append(heart)
        self.current_block_label = None

    def update_items(self):
        self.player.quick_slots.remove_unnecessary_stacks()
        self.icons = []
        for amount_label in self.amount_labels:
            amount_label.delete()
        self.amount_labels = []
        x = self.frame.x + 3
        items = self.player.quick_slots.get_items()
        items = items[:self.max_items]
        for item in items:
            if not item:
                x += (self.icon_size * 0.5) + 3
                continue
            icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = self.frame.y + 3
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=item.get_object().amount_label_color, batch=self.batch,
                group=self.labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
        self.update_current()

    def update_current(self):
        if self.current_block_label:
            self.current_block_label.delete()
        if hasattr(self.get_current_block_item(False), 'quickslots_x') and hasattr(self.get_current_block_item(False), 'quickslots_y'):
            self.current_block_label = pyglet.text.Label(
                self.get_current_block_item(False).name, font_name=globals.DEFAULT_FONT, font_size=9,
                x=self.get_current_block_item(False).quickslots_x + 0.25 * self.icon_size, y=self.get_current_block_item(False).quickslots_y - 20,
                anchor_x='center', anchor_y='bottom',
                color=(255, 255, 255, 255), batch=self.batch,
                group=self.labels_group)
        self.active.x = self.frame.x + (self.current_index * 35)

    def update_health(self):
        hearts_to_show = self.player.health
        showed_hearts = 0
        for i, heart in enumerate(self.hearts):
            heart.x = self.frame.x + i * (20 + 2) + (self.frame.width - hearts_to_show * (20 + 2)) / 2
            heart.y = self.icon_size * 1.0 + 12
            heart.visible = True
            if showed_hearts >= hearts_to_show:
                heart.visible = False
            showed_hearts += 1

    def get_current_block(self):
        item = self.player.quick_slots.at(self.current_index)
        if not item:
            return
        return item.get_object()

    def get_current_block_item(self, remove=False):
        item = self.player.quick_slots.at(self.current_index)
        if remove:
            self.player.quick_slots.remove_by_index(self.current_index,
                                                        quantity=item.amount)
        return item

    def get_current_block_item_and_amount(self, remove=True):
        item = self.player.quick_slots.at(self.current_index)
        if item:
            amount = item.amount
            if remove:
                self.player.quick_slots.remove_by_index(self.current_index,
                                                        quantity=item.amount)
            return item, amount
        return False

    def remove_current_block(self, quantity=1):
        self.player.quick_slots.remove_by_index(self.current_index, quantity=quantity)
        self.update_items()

    def _on_toggled(self):
        if self.visible:
            self.update_items()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.visible and self.parent.window.exclusive:
            self.current_index -= scroll_y
            return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        if self.visible:
            if symbol in self.num_keys:
                index = (symbol - self.num_keys[0])
                self.set_index(index)
                return pyglet.event.EVENT_HANDLED
            elif symbol == globals.VALIDATE_KEY:
                current_block = self.get_current_block_item_and_amount()
                if current_block:
                    if not self.player.inventory.add_item(
                            current_block[0].id, quantity=current_block[1]):
                        self.player.quick_slots.add_item(
                            current_block[0].id, quantity=current_block[1])
                    self.update_items()
                    return pyglet.event.EVENT_HANDLED

    def on_resize(self, width, height):
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size * 0.5
        self.active.y = self.frame.y
        if self.visible:
            self.update_health()
            self.update_current()
            self.update_items()

    def _on_draw(self):
        self.batch.draw()


class InventorySelector(AbstractInventory):
    def __init__(self, parent, player, model, *args, **kwargs):
        super(InventorySelector, self).__init__(parent, *args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.OrderedGroup(1)
        self.amount_labels_group = pyglet.graphics.OrderedGroup(2)
        self.amount_labels = []
        self.parent = parent
        self.model = model
        self.player = player
        self.max_items = self.player.inventory.slot_count
        self.current_index = 1
        self.icon_size = self.model.group.texture.width / globals.TILESET_SIZE
        self.selected_item = None
        self.selected_item_icon = None
        self.mode = 0 # 0 - Normal inventory, 1 - Crafting Table
        self.change_image()
        self.crafting_panel = Inventory(4)
        self.crafting_outcome = None  # should be an item stack
        self.crafting_outcome_icon = None
        self.crafting_outcome_label = None
        self.crafting_table_panel = Inventory(9)
        self.visible = False

    def change_image(self):
        if self.mode == 0:
            image = load_image('resources', 'textures', 'inventory.png')
        elif self.mode == 1:
            image = load_image('resources', 'textures', 'inventory_when_crafting_table.png')
        self.frame = image_sprite(image, self.batch, 0)
        self.frame.x = (self.parent.window.width - self.frame.width) / 2
        self.frame.y = self.icon_size / 2 - 4

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
            icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = y - icon.height
            x += (self.icon_size * 0.5) + 3
            if x >= (self.frame.x + self.frame.width) - 7:
                x = self.frame.x + 7
                y -= (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=item.get_object().amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)

        items = self.player.quick_slots.get_items()
        items = items[:self.player.quick_slots.slot_count]
        for i, item in enumerate(items):
            if not item:
                x += (self.icon_size * 0.5) + 3
                continue
            icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = self.frame.y + 7
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=item.get_object().amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)

        items = self.player.armor.get_items()
        items = items[:4]
        x = self.frame.x + 7
        y = inventory_y + inventory_height + 10 + 4 * self.icon_size * 0.5 + 9
        for i, item in enumerate(items):
            if not item:
                y -= (self.icon_size * 0.5) + 3
                continue
            icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = y
            amount_label = pyglet.text.Label(
                str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=item.get_object().amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
        self.update_current()

        crafting_y = inventory_y + inventory_height + (42 if self.mode == 0 else 14)
        crafting_rows = (2 if self.mode == 0 else 3)
        crafting_height = (crafting_rows * (self.icon_size * 0.5)) + (crafting_rows * 3)
        x = self.frame.x + (165 if self.mode == 0 else 72)
        y = self.frame.y + crafting_y + crafting_height
        items = self.crafting_panel.get_items() if self.mode == 0 else self.crafting_table_panel.get_items()
        items = items[:self.crafting_panel.slot_count] if self.mode == 0 else items[:self.crafting_table_panel.slot_count]
        # NOTE: each line in the crafting panel should be a sub-list in the crafting ingredient list
        crafting_ingredients = [[], []] if self.mode == 0 else [[], [], []]
        for i, item in enumerate(items):
            if not item:
                # placeholder
                crafting_ingredients[int(floor(i / (2 if self.mode == 0 else 3)))].append(air_block)
                x += (self.icon_size * 0.5) + 3
                if x >= (self.frame.x + (165 if self.mode == 0 else 72)) + 35 * ((2 if self.mode == 0 else 3)):
                    x = self.frame.x + (165 if self.mode == 0 else 72)
                    y -= (self.icon_size * 0.5) + 3
                continue
            icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
            icon.scale = 0.5
            icon.x = x
            icon.y = y - icon.height
            item.quickslots_x = icon.x
            item.quickslots_y = icon.y
            x += (self.icon_size * 0.5) + 3
            if x >= (self.frame.x + (165 if self.mode == 0 else 72)) + 35 * ((2 if self.mode == 0 else 3)):
                x = self.frame.x + (165 if self.mode == 0 else 72)
                y -= (self.icon_size * 0.5) + 3
            amount_label = pyglet.text.Label(
                str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
                x=icon.x + 3, y=icon.y, anchor_x='left', anchor_y='bottom',
                color=item.get_object().amount_label_color, batch=self.batch,
                group=self.amount_labels_group)
            self.amount_labels.append(amount_label)
            self.icons.append(icon)
            if item.get_object().id > 0:
                crafting_ingredients[int(floor(i / (2 if self.mode == 0 else 3)))].append(item.get_object())

        if len(crafting_ingredients) > 0:
            outcome = globals.recipes.craft(crafting_ingredients)
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

    def toggle(self, reset_mode=True):
        if not self.visible:
            self.update_items()
        if reset_mode:
            self.mode = 0
        self.change_image()
        self.parent.item_list.toggle()
        self.parent.window.set_exclusive_mouse(self.visible)
        self.visible = not self.visible

    def mouse_coords_to_index(self, x, y):
        inventory_rows = floor(self.max_items / 9)
        crafting_rows = (2 if self.mode == 0 else 3)
        quick_slots_y = self.frame.y + 4
        inventory_y = quick_slots_y + 42
        inventory_height = (inventory_rows * (self.icon_size * 0.5)) + (inventory_rows * 3)
        crafting_items_per_row = (2 if self.mode == 0 else 3)
        crafting_y = inventory_y + inventory_height + (42 if self.mode == 0 else 14)
        crafting_x = self.frame.x + (165 if self.mode == 0 else 72)
        crafting_height = (crafting_rows * (self.icon_size * 0.5)) + (crafting_rows * 3)
        crafting_width = (crafting_items_per_row * (self.icon_size * 0.5)) + (crafting_items_per_row-1) * 3

        armor_y = inventory_y + inventory_height + 10
        armor_x = self.frame.x + 7
        armor_height = 4 * (self.icon_size * 0.5 + 3)
        armor_width = self.icon_size * 0.5

        crafting_outcome_y = inventory_y + inventory_height + (60 if self.mode == 0 else 42)
        crafting_outcome_x = self.frame.x + (270 if self.mode == 0 else 222)
        crafting_outcome_width = crafting_outcome_height = self.icon_size * 0.5
        # out of bound

        if (x <= self.frame.x + 7) or (x >= (self.frame.x + self.frame.width) - 7) or (y <= quick_slots_y) or y >= (armor_y + armor_height):
            return -1, -1

        x_offset = x - (self.frame.x + 7)

        if y <= quick_slots_y + 35:
            row = 0.0
            inventory = self.player.quick_slots
            items_per_row = 9
        elif y <= inventory_y + inventory_height and y >= inventory_y:
            y_offset = (y - (inventory_y + inventory_height)) * -1
            row = floor(y_offset // (self.icon_size * 0.5 + 3))
            if self.mode == 0:
                self.crafting_panel.remove_unnecessary_stacks()
            elif self.mode == 1:
                self.crafting_table_panel.remove_unnecessary_stacks()
            inventory = self.player.inventory
            items_per_row = 9
        elif crafting_y <= y <= crafting_y + crafting_height and x >= crafting_x \
            and x <= crafting_x + crafting_width:
            y_offset = (y - (crafting_y + crafting_height)) * -1
            row = floor(y_offset // (self.icon_size * 0.5 + 3))
            if self.mode == 0:
                self.crafting_panel.remove_unnecessary_stacks()
                inventory = self.crafting_panel
            elif self.mode == 1:
                self.crafting_table_panel.remove_unnecessary_stacks()
                inventory = self.crafting_table_panel
            x_offset = x - crafting_x
            items_per_row = crafting_items_per_row
        elif crafting_outcome_y <= y <= crafting_outcome_y + crafting_outcome_height and \
            crafting_outcome_x <= x <= crafting_outcome_x + crafting_outcome_width:
            #print('Crafting outcome!')
            return 0, 256   # 256 for crafting outcome
        elif armor_y <= y <= armor_y + armor_height and \
            armor_x <= x <= armor_x + armor_width:
            items_per_row = 1
            row = floor((armor_y + armor_height - y) // (self.icon_size * 0.5))
            x_offset = 0
            inventory = self.player.armor
        else:
            return -1, -1

        col = x_offset // (self.icon_size * 0.5 + 3)

        #print(row)
        #print(col)
        return inventory, int(row * items_per_row + col)

    def set_crafting_outcome(self, item):
        if not item:
            self.remove_crafting_outcome()
            return
        self.crafting_outcome = item

        self.crafting_outcome_icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
        inventory_rows = floor(self.max_items / 9)
        inventory_height = (inventory_rows * (self.icon_size * 0.5)) + (inventory_rows * 3)
        quick_slots_y = self.frame.y + 4
        inventory_y = quick_slots_y + (42 if self.mode == 0 else 14)
        if self.mode == 0:
            self.crafting_outcome_icon.scale = 0.5
            self.crafting_outcome_icon.y = inventory_y + inventory_height + 62
            self.crafting_outcome_icon.x = self.frame.x + 270
        elif self.mode == 1:
            self.crafting_outcome_icon.scale = 0.5
            self.crafting_outcome_icon.y = inventory_y + inventory_height + 80
            self.crafting_outcome_icon.x = self.frame.x + 225
        self.crafting_outcome_label = pyglet.text.Label(
            str(item.amount), font_name=globals.DEFAULT_FONT, font_size=9,
            x= self.crafting_outcome_icon.x + 3, y= self.crafting_outcome_icon.y, anchor_x='left', anchor_y='bottom',
            color=item.get_object().amount_label_color,
            group=self.group)

    def remove_crafting_outcome(self):
        self.crafting_outcome = None
        self.crafting_outcome_icon = None
        if self.crafting_outcome_label: self.crafting_outcome_label.delete()
    def set_selected_item(self, item):
        if not item:
            self.remove_selected_item()
            return
        self.selected_item = item

        self.selected_item_icon = image_sprite(get_block_icon(item.get_object(), self.icon_size, self.model), self.batch, self.group)
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
                inventory_y = quick_slots_y + (42 if self.mode == 0 else 14)
                self.selected_item_icon.y = inventory_y + inventory_height + (60 if self.mode == 0 else 42)
                self.selected_item_icon.x = self.frame.x + (270 if self.mode == 0 else 222)
                # cost
                current_panel = self.crafting_panel if self.mode == 0 else self.crafting_table_panel
                for ingre in current_panel.slots:
                    if ingre :
                        ingre.change_amount(-1)
                        # ingredient has been used up
                        if ingre.amount <= 0:
                            self.remove_crafting_outcome()
                current_panel.remove_unnecessary_stacks()
                self.update_items()
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
            if symbol == globals.ESCAPE_KEY:
                self.toggle()
                return pyglet.event.EVENT_HANDLED
            elif symbol == globals.VALIDATE_KEY:
                return pyglet.event.EVENT_HANDLED

    def on_resize(self, width, height):
        self.frame.x = (width - self.frame.width) / 2
        self.frame.y = self.icon_size / 2 - 4
        if self.visible:
            self.update_current()
            self.update_items()

    def _on_draw(self):
        self.batch.draw()
        if self.selected_item_icon:
            self.selected_item_icon.draw()
        if self.crafting_outcome_icon:
            self.crafting_outcome_icon.draw()
        if self.crafting_outcome_label:
            self.crafting_outcome_label.draw()


class TextWidget(Control):
    """
    Variation of this example: http://www.pyglet.org/doc/programming_guide/text_input.py
    """
    def __init__(self, parent, text, x, y, width, multi_line=False, key_released=None, *args, **kwargs):
        super(TextWidget, self).__init__(parent, *args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = None
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        self.padding = 10
        self.height = (font.ascent - font.descent) + self.padding
        self.x, self.y, self.width = x, y + self.height, width

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, self.width, self.height, multiline=False, batch=self.batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y
        self._on_resize()
        self._key_released = key_released
        self.multi_line = multi_line

    def focus(self):
        self.caret.visible = True
        self.caret.mark = 0
        self.caret.position = len(self.document.text)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)

    @property
    def text(self):
        return self.document.text

    @text.setter
    def text(self, text):
        self.document.text = text

    def _on_resize(self):
        super(TextWidget, self)._on_resize()
        # Check if anchor points have been set
        if any(self._anchor_points):
            al, at, ar, ab = self._anchor_points
            self.width = ar
            self.y = ab
        # Recreate the bounding box
        self.rectangle = Rectangle(self.x - self.padding, self.y - self.padding,
                                   self.width + self.padding, self.height + self.padding)
        # And reposition the text layout
        self.layout.x = self.x + self.padding
        self.layout.y = (self.rectangle.y + (self.rectangle.height/2) - (self.height/2))
        self.layout.width = self.rectangle.width - self.padding
        self.layout.height = self.rectangle.height - self.padding
        if self.vertex_list:
            self.vertex_list.delete()
        self.vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, None,
                                          ('v2i', self.rectangle.vertex_list()),
                                          ('c4B', [200, 200, 200, 128] * 4)
        )

    def _on_draw(self):
        self.batch.draw()

    def _on_toggled(self):
        self.parent.window.set_exclusive_mouse(not self.visible)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.visible:
            self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            return pyglet.event.EVENT_HANDLED

    def on_text(self, text):
        if self.visible:
            if not self.multi_line:
                text = text.replace('\r', '')  # Remove carriage returns
            self.caret.on_text(text)
            return pyglet.event.EVENT_HANDLED

    def on_text_motion(self, motion):
        if self.visible:
            self.caret.on_text_motion(motion)
            return pyglet.event.EVENT_HANDLED

    def on_text_motion_select(self, motion):
        if self.visible:
            self.caret.on_text_motion_select(motion)
            return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifier):
        if self.visible:
            return pyglet.event.EVENT_HANDLED

    def on_key_release(self, symbol, modifier):
        if self.visible:
            if symbol == globals.ESCAPE_KEY:
                self.toggle()
                self.parent.window.pop_handlers()
            if self._key_released:
                ret = self._key_released(self, symbol, modifier)
                if ret:
                    return ret
            return pyglet.event.EVENT_HANDLED
