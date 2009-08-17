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

from geometry import Rect, Size

class Widget(object):
	"""Base class for all GUI elements"""
	def __init__(self, **kwargs):
		'''Initialise a Widget
		
		Keyword arguments:
		name -- unique widget identifier
		'''
		self._x, self._y = kwargs.get('x', 0), kwargs.get('y', 0)
		self._w, self._h = kwargs.get('w', 0), kwargs.get('h', 0)
		self._gx, self._gy = self._x, self._y
		
		self._pref_size = Size()
		
		self._name = kwargs.get('name')
		
		self.parent = None
		self._theme = None
		self._batch = None
		self._group = None
		
		self._dirty = False
		
		self._visible = True
		
		self.halign = kwargs.get('halign', 'center')
		self.valign = kwargs.get('valign', 'center')
		
		self.shapes = {}
		self.elements = {}
		
		self.expandable = [kwargs.get('hexpand', self._w==0), kwargs.get('vexpand', self._h==0)]
	
	def _get_x(self):
		return self._x
	def _set_x(self, x):
		self._x = x
		self.find_root().update_layout()
	x = property(_get_x, _set_x)
	
	def _get_y(self):
		return self._y
	def _set_y(self, y):
		self._y = y
		self.find_root().update_layout()
	y = property(_get_y, _set_y)

	def _get_w(self):
		return self._w
	def _set_w(self, w):
		self._w = w
		self.find_root().update_layout()
	w = property(_get_w, _set_w)
	
	def _get_h(self):
		return self._h
	def _set_h(self, h):
		self._h = h
		self.find_root().update_layout()
	h = property(_get_h, _set_h)
	
	def _get_name(self):
		return self._name
	def _set_name(self, name):
		_name = self._name
		self._name = name
		self.update_names(_name)
	name = property(_get_name, _set_name)
	
	def _get_theme(self):
		return self._theme
	theme = property(_get_theme)
	
	def _get_batch(self):
		return self._batch
	batch = property(_get_batch)
	
	def _get_visible(self):
		return self._visible
	def _set_visible(self, visible):
		self._visible = visible
		self.update_batch(self._batch, self._group)
	visible = property(_get_visible, _set_visible)
	
	def remove_from_parent(self):
		self.parent.remove(self)
	
	def find_root(self):
		root = self
		
		while root.parent:
			root = root.parent
		
		return root
	
	def update_names(self, oldname=None):
		from frame import Frame
		r = self.find_root()
		if isinstance(r, Frame):
			if oldname:
				del r.names[oldname]
			if self.name:
				r.names[self.name] = self
	
	def remove_names(self):
		from frame import Frame
		r = self.find_root()
		if isinstance(r, Frame):
			if self.name:
				del r.names[self.name]
	
	def update_global_coords(self):
		if self.parent:
			self._gx, self._gy = self.parent._gx + self._x, self.parent._gy + self._y
		else:
			self._gx, self._gy = self._x, self._y
	
	def update_layout(self):
		self._dirty = True
	
	def update_elements(self):
		self._dirty = False
	
	def update_theme(self, theme):
		self._theme = theme
		self._dirty = True
	
	def update_batch(self, batch, group):
		self._batch, self._group = batch, group
		
		shape_group = pyglet.graphics.OrderedGroup(0, group)
		text_group = pyglet.graphics.OrderedGroup(1, group)
		
		for k, e in self.shapes.iteritems():
			e.update_batch((batch if self.visible else None), shape_group)
		
		for k, e in self.elements.iteritems():
			e.update_batch((batch if self.visible else None), text_group)
		
		self._dirty = True
	
	def determine_size(self):
		pass
	
	def reset_size(self, size):
		self._w, self._h = size
		self._dirty = True
	
	def on_mouse_press(self, x, y, button, modifiers):
		pass
	
	def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
		pass
	
	def on_mouse_release(self, x, y, button, modifiers):
		pass
	
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		pass
	
	def on_key_press(self, symbol, modifiers):
		pass
	
	def on_text(self, text):
		pass
	
	def on_text_motion(self, motion, select=False):
		pass
	
	def hit_test(self, x, y):
		return self.bounds().hit_test(x, y)
	
	def bounds(self):
		return Rect(self._gx, self._gy, self.w, self.h)
