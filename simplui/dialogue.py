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
from container import Container, SingleContainer

class Dialogue(SingleContainer):
	"""Moveable window, optionally resizeable"""
	def __init__(self, title, **kwargs):
		'''Create a dialogue
		
		Keyword arguments:
		name -- unique widget identifier
		content -- child container
		'''
		SingleContainer.__init__(self, **kwargs)
		
		self.resizeable = kwargs.get('resizeable', False)
		
		self.shapes['background'] = Rectangle()
		self.shapes['title_bar'] = Rectangle()
		self.elements['title'] = BasicLabel(title, anchor_x='center')
		
		self.topbar = Rect(0, 0, 0, 15)
		
		self._in_drag = False
		
		self.content = kwargs.get('content', None)
	
	def _get_title(self):
		return self.elements['title'].text
	def _set_title(self, title):
		self.elements['title'].text = title
	title = property(_get_title, _set_title)	
	
	def update_theme(self, theme):
		SingleContainer.update_theme(self, theme)
		
		if theme:
			background_patch = theme['window']['image_background']
			title_patch = theme['window']['image_title_bar']
			
			self.shapes['background'].patch = background_patch
			self.shapes['title_bar'].patch = title_patch
			
			self.elements['title'].font_name = theme['font']
			self.elements['title'].font_size = theme['font_size_small']
			self.elements['title'].color = theme['font_color']
			
			font = self.elements['title'].document.get_font()
			height = font.ascent - font.descent
			
			self._pref_size = Size(title_patch.padding_x + self.elements['title'].content_width, background_patch.padding_y + title_patch.padding_y + height)
	
	def update_elements(self):
		if self._dirty and self.theme:
			background = self.theme['window']['image_background']
			title_bar = self.theme['window']['image_title_bar']
			
			font = self.elements['title'].document.get_font()
			height = font.ascent - font.descent
			
			h = title_bar.padding_bottom + height + title_bar.padding_top
			
			self.shapes['background'].update(self._gx, self._gy, self.w, self.h)
			self.shapes['title_bar'].update_in(self._gx - background.padding_left, self._gy + self.h, self.w + background.padding_left + background.padding_right, h)
			
			self.elements['title'].x = self._gx + self.w/2
			
			self.topbar = Rect(-background.padding_left, self.h, self.w + background.padding_left + background.padding_right, h)
			self.elements['title'].y = self._gy + self.h + title_bar.padding_bottom - font.descent
		
		SingleContainer.update_elements(self)
	
	def reset_size(self, size):
		self._y += self._h - size.h
		SingleContainer.reset_size(self, size)
	
	def bounds(self):
		return Rect(self._gx, self._gy, self.w, self.h + self.topbar.h)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and \
				self.topbar.hit_test(x - self.x, y - self.y):
			self._in_drag = True
			self._offset_x = x - self.x
			self._offset_y = y - self.y
			return pyglet.event.EVENT_HANDLED
		
		SingleContainer.on_mouse_press(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._in_drag:
			self._x = x - self._offset_x
			self._y = y - self._offset_y
			self.find_root().update_layout()
			return pyglet.event.EVENT_HANDLED
		
		SingleContainer.on_mouse_drag(self, x, y, dx, dy, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
	
	def on_mouse_release(self, x, y, button, modifiers):
		if button == pyglet.window.mouse.LEFT and self._in_drag:
			self._in_drag = False
			return pyglet.event.EVENT_HANDLED
		
		SingleContainer.on_mouse_release(self, x, y, button, modifiers)
		return pyglet.event.EVENT_UNHANDLED
