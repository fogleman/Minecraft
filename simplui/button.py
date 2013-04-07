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
from geometry import Rect, Size
from widget import Widget

class Button(Widget):
	"""Clickable button"""
	def __init__(self, text, **kwargs):
		'''Create a button control
		
		Keyword arguments:
		action -- callback to be invoked when the button is clicked
		'''
		Widget.__init__(self, **kwargs)
		
		self.elements['label'] = BasicLabel(text, font_size=8, color=(0,0,0,255), anchor_x='left', anchor_y='bottom')
		self.shapes['frame'] = Rectangle()
		self.active_region = Rect(0, 0, 0, 0)
		
		self.action = kwargs.get('action', None)
		self._down = False
	
	def _get_text(self):
		return self.elements['label'].text
	def _set_text(self, text):
		self.elements['label'].text = text
	text = property(_get_text, _set_text)
	
	def update_theme(self, theme):
		Widget.update_theme(self, theme)
		
		if theme:
			patch = theme['button'][('image_down' if self._down else 'image_up')]
			
			label = self.elements['label']
			label.font_name = self.theme['font']
			label.font_size = self.theme['font_size']
			label.color = theme['font_color']
			
			font = label.document.get_font()
			height = font.ascent - font.descent
			
			self._pref_size = Size(patch.padding_left + label.content_width + patch.padding_right, patch.padding_bottom + height + patch.padding_top)
			
			label.x = patch.padding_left + label.content_width/2
			label.y = patch.padding_bottom + height/2 - font.descent
			
			self.shapes['frame'].patch = patch
	
	def update_elements(self):
		if self._dirty and self.theme:
			patch = self.theme['button'][('image_down' if self._down else 'image_up')]
						
			label = self.elements['label']
			
			font = label.document.get_font()
			height = font.ascent - font.descent
			
			left = 0
			if self.halign == 'center':
				left = self.w/2 - self._pref_size[0]/2
			elif self.halign == 'right':
				left = self.w - self._pref_size[0]
			
			bottom = 0
			if self.valign == 'center':
				bottom = self.h/2 - self._pref_size[1]/2
			elif self.valign == 'top':
				bottom = self.h - self._pref_size[1]
			
			label.x = self._gx + left + patch.padding_left
			label.y = self._gy + bottom + patch.padding_bottom
			
			self.shapes['frame'].update(self._gx + left + patch.padding_left, self._gy + bottom + patch.padding_bottom, label.content_width, height)
			
			self.active_region = Rect(self._gx + left + patch.padding_left, self._gy + bottom + patch.padding_bottom, label.content_width, height)
		
		Widget.update_elements(self)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self.active_region.hit_test(x, y):
			self.shapes['frame'].patch = self.theme['button']['image_down']
			self._down = True
			return pyglet.event.EVENT_HANDLED
		
		Widget.on_mouse_press(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._down:
			if self.active_region.hit_test(x, y):
				self.shapes['frame'].patch = self.theme['button']['image_down']
			else:
				self.shapes['frame'].patch = self.theme['button']['image_up']
			
			return pyglet.event.EVENT_HANDLED
				
		Widget.on_mouse_drag(self, x, y, dx, dy, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._down:
			self.shapes['frame'].patch = self.theme['button']['image_up']
			self._down = False
			if self.active_region.hit_test(x, y):
				if self.action:
					self.action(self)
				return pyglet.event.EVENT_HANDLED
		
		Widget.on_mouse_press(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
