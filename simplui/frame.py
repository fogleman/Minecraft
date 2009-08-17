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
from pyglet.gl import *

from shape import Rectangle
from widget import Widget
from container import Container

class Frame(Container):
	"""Root GUI container"""
	def __init__(self, theme, **kwargs):
		"""Create a frame
		
		Keyword arguments:
		children -- list of child elements to be added to this container
		"""
		Container.__init__(self, **kwargs)
		
		self.names = {}
		self.focus = []
		
		self.theme = theme
	
	def _get_theme(self):
		return self._theme
	def _set_theme(self, theme):
		self.update_theme(theme)
		self.update_batch(pyglet.graphics.Batch(), None)
		self.update_layout()
	theme = property(_get_theme, _set_theme)
	
	def update_batch(self, batch, group):
		self._batch, self._group = batch, group
		
		count = len(self.children)
		for c, i in zip(self.children, range(count-1, -1, -1)):
			order = pyglet.graphics.OrderedGroup(i, group)
			c.update_batch(batch, order)
		
	def add(self, child):
		Container.add(self, child)
		
		self.update_batch(pyglet.graphics.Batch(), self._group)
	
	def remove(self, child):
		Container.remove(self, child)
		
		self.update_batch(pyglet.graphics.Batch(), self._group)
	
	def get_element_by_name(self, name):
		return self.names[name]
	
	def on_mouse_press(self, x, y, button, modifiers):
		if len(self.focus) > 0:
			return self.focus[-1].on_mouse_press(x, y, button, modifiers)
		
		if self.children[0].hit_test(x, y):
			return self.children[0].on_mouse_press(x, y, button, modifiers)
		
		for c in self.children:
			if c.hit_test(x, y):
				self.children.remove(c)
				self.children.insert(0, c)
				c.on_mouse_press(x, y, button, modifiers)
				self.update_batch(pyglet.graphics.Batch(), self._group)
				return
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		if len(self.focus) > 0:
			return self.focus[-1].on_mouse_drag(x, y, dx, dy, button, modifiers)
		return Container.on_mouse_drag(self, x, y, dx, dy, button, modifiers)
	
	def on_mouse_release(self, x, y, button, modifiers):
		if len(self.focus) > 0:
			return self.focus[-1].on_mouse_release(x, y, button, modifiers)
		return Container.on_mouse_release(self, x, y, button, modifiers)
	
	def on_key_press(self, symbol, modifiers):
		if len(self.focus) > 0:
			return self.focus[-1].on_key_press(symbol, modifiers)
		return Container.on_key_press(self, symbol, modifiers)
	
	def on_text(self, text):
		if len(self.focus) > 0:
			return self.focus[-1].on_text(text)
		return Container.on_text(self, text)
	
	def update_layout(self):
		for c in self.children:
			c.determine_size()
			c.reset_size(c._pref_size)
	
	def draw(self):
		self.update_global_coords()
		self.update_elements()
		
		glPushAttrib(GL_ENABLE_BIT)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		self.batch.draw()
		
		glPopAttrib()
