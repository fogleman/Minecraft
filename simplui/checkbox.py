# ----------------------------------------------------------------------
# Copyright (c) 2009 Tristam MacDonald
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of DarkCoda nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

import pyglet

from shape import Rectangle, BasicLabel
from widget import Widget
from geometry import Size

class Checkbox(Widget):
	"""Clickable checkbox with textual label"""
	def __init__(self, text, **kwargs):
		'''Create a checkbox control
		
		Keyword arguments:
		name -- unique widget identifier
		value -- initial value
		action -- callback to be invoked when the value changes
		'''
		label = BasicLabel(text, font_size=8, color=(0,0,0,255), x=15, y=0, anchor_x='left', anchor_y='bottom')
		
		Widget.__init__(self, **kwargs)
		self.elements['label'] = label
		self.shapes['box'] = Rectangle()
		
		self._value = kwargs.get('value', False)
		self.action = kwargs.get('action', None)
		
		self._down = False
	
	def _get_text(self):
		return self.elements['label'].text
	def _set_text(self, text):
		self.elements['label'].text = text
	text = property(_get_text, _set_text)
	
	def _get_value(self):
		return self._value
	def _set_value(self, value):
		self._value = value
		self.shapes['box'].patch = self.theme['checkbox'][('image_checked' if self.value else 'image_unchecked')]
	value = property(_get_value, _set_value)
	
	def update_theme(self, theme):
		Widget.update_theme(self, theme)
		
		if theme:
			patch = theme['checkbox'][('image_checked' if self.value else 'image_unchecked')]
			
			label = self.elements['label']
			label.font_name = theme['font']
			label.font_size = theme['font_size']
			label.color = theme['font_color']
			
			font = label.document.get_font()
			height = font.ascent - font.descent
			
			self._pref_size = Size(patch.padding_left + label.content_width + patch.padding_right, patch.padding_bottom + height + patch.padding_top)
			
			self.shapes['box'].patch = patch
	
	def update_elements(self):
		if self._dirty and self.theme:
			patch = self.theme['checkbox'][('image_checked' if self.value else 'image_unchecked')]
			
			label = self.elements['label']
			
			label.x = self._gx + patch.padding_left
			label.y = self._gy + patch.padding_bottom
			
			self.shapes['box'].update(self._gx + patch.padding_left, self._gy + patch.padding_right, self.w - patch.padding_left, 0)
		
		Widget.update_elements(self)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self.hit_test(x, y):
			self.shapes['box'].patch = self.theme['checkbox'][('image_checked' if not self.value else 'image_unchecked')]
			self._down = True
			return pyglet.event.EVENT_HANDLED
		
		Widget.on_mouse_press(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._down:
			if self.hit_test(x, y):
				self.shapes['box'].patch = self.theme['checkbox'][('image_checked' if not self.value else 'image_unchecked')]
			else:
				self.shapes['box'].patch = self.theme['checkbox'][('image_checked' if self.value else 'image_unchecked')]
			
			return pyglet.event.EVENT_HANDLED
				
		Widget.on_mouse_drag(self, x, y, dx, dy, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._down:
			self._down = False
			if self.hit_test(x, y):
				self.value = not self.value
				if self.action:
					self.action(self)
				return pyglet.event.EVENT_HANDLED
		
		Widget.on_mouse_press(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
