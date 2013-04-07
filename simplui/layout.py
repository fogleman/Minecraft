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

from shape import Rectangle
from widget import Widget
from container import Container
from geometry import Size

class Layout(Container):
	def __init__(self, axis, **kwargs):
		Container.__init__(self, **kwargs)
		
		self._axis = axis
		self.padding = (kwargs.get('hpadding', 5), kwargs.get('vpadding', 5))
		
		self.expandable[self._axis] = True
	
	def determine_size(self):
		w, h = 0, self.padding[self._axis]
		for c in self.children:
			c.determine_size()
			min = c._pref_size
			
			if min[1-self._axis] > w:
				w = min[1-self._axis]
			h += min[self._axis] + self.padding[self._axis]
		
		if self._axis == 1:
			self._pref_size = Size(w + self.padding[1-self._axis]*2, h)
		else:
			self._pref_size = Size(h, w + self.padding[1-self._axis]*2)
	
	def reset_size(self, size):
		Widget.reset_size(self, size)
				
		minh = self._pref_size[self._axis]
		freeh = size[self._axis] - minh
		
		flexible = [c for c in self.children if c.expandable[self._axis]]
		l = len(flexible)
		
		if l > 0:
			extrah = freeh / len(flexible)
		
		th = self.padding[self._axis]
		
		step = (1, -1)[self._axis]
		
		for c in self.children[::step]:
			if self._axis == 1:
				c._x, c._y = self.padding[1-self._axis], th
			else:
				c._y, c._x = self.padding[1-self._axis], th
			
			min = c._pref_size
			if c.expandable[1-self._axis]:
				nw = size[1-self._axis] - self.padding[1-self._axis]*2
			else:
				nw = min[1-self._axis]
			if c.expandable[self._axis]:
				nh = min[self._axis] + extrah
			else:
				nh = min[self._axis]
			
			if self._axis == 1:
				c.reset_size(Size(nw, nh))
			else:
				c.reset_size(Size(nh, nw))
			
			th += nh + self.padding[self._axis]

class HLayout(Layout):
	"""Horizontally arranging and resizing layout"""
	def __init__(self, **kwargs):
		Layout.__init__(self, 0, **kwargs)

class VLayout(Layout):
	"""Vertically arranging and resizing layout"""
	def __init__(self, **kwargs):
		Layout.__init__(self, 1, **kwargs)
