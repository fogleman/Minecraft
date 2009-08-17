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

from widget import Widget
from container import Container
from geometry import Size

class FlowLayout(Container):
	"""Automatically overflows into lines, and centers each line"""
	def __init__(self, **kwargs):
		kwargs.setdefault('w', 150)
		
		Container.__init__(self, **kwargs)
		
		self.padding = (kwargs.get('hpadding', 5), kwargs.get('vpadding', 5))
	
	def determine_size(self):
		maxw = self.w - self.padding[0]*2
		
		w, h, maxh = self.padding[0], self.padding[1], 0
		
		self.lines = []
		line = []
		
		for c in self.children:
			c.determine_size()
			min = c._pref_size
			
			if w + min.w < maxw:
				line.append(c)
			else:				
				self.lines.append((maxh, w, line))
				line = [c]
				
				h += maxh + self.padding[1]
				w, maxh = self.padding[0], 0
			
			if min.h > maxh:
				maxh = min.h
			w += min.w + self.padding[0]
		
		if len(line) > 0:
			self.lines.append((maxh, w, line))
			h += maxh + self.padding[1]
		
		self._pref_size = Size(self.w, max(h, self.padding[1]*2))
	
	def reset_size(self, size):
		Widget.reset_size(self, size)
		
		maxw = size.w - self.padding[0]*2
		
		h = self.padding[1]
		
		for maxh, width, line in self.lines[::-1]:
			w = maxw/2 - width/2 + self.padding[0]
			
			for c in line:
				c._x, c._y = w, h + maxh/2 - c._pref_size.h/2
				c.reset_size(c._pref_size)
				w += c._pref_size[0] + self.padding[0]
			h += maxh + self.padding[1]
