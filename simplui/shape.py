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

class Rectangle(object):
	"""Basic rectangular element for renderering and hit testing"""
	def __init__(self, visible=True):
		self.x, self.y, self.w, self.h = 0, 0, 1, 1
		self._patch = None
		self._batch = None
		self._group = None
		self._vertices = None
	
	def _get_patch(self):
		return self._patch
	def _set_patch(self, patch):
		self._patch = patch
		self.update_batch(self._batch, self._group)
	patch = property(_get_patch, _set_patch)
	
	def update_batch(self, batch, group):	
		self._batch, self._group = batch, group
		
		if self._vertices:
			self._vertices.delete()
			self._vertices = None
		
		if self.patch and batch:
			self._vertices = self.patch.build_vertex_list(batch, group)
	
	def update(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h
		
		if self._vertices:
			self.patch.update_vertex_list_around(self._vertices, x, y, w, h)
	
	def update_in(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h
		
		if self._vertices:
			self.patch.update_vertex_list(self._vertices, x, y, w, h)

class BasicLabel(pyglet.text.Label):
	### workaround for pyglet issue 427
	_cached_groups = {} 
	def _init_groups(self, group): 
		if not group: 
			return 
		if group not in self.__class__._cached_groups.keys(): 
			top = pyglet.text.layout.TextLayoutGroup(group) 
			bg = pyglet.graphics.OrderedGroup(0,top) 
			fg = pyglet.text.layout.TextLayoutForegroundGroup(1,top) 
			fg2 = pyglet.text.layout.TextLayoutForegroundDecorationGroup (2,top) 
			self.__class__._cached_groups[group] = [top,bg,fg,fg2,0] 
		groups = self.__class__._cached_groups[group] 
		self.top_group= groups[0] 
		self.background_group = groups[1] 
		self.foreground_group = groups[2] 
		self.foreground_decoration_group = groups[3] 
		groups[4] += 1
	
	def delete(self): 
		pyglet.text.Label.delete(self) 
		group = self.top_group.parent 
		if group is not None: 
			groups = self.__class__._cached_groups[group] 
			groups[4] -= 1 
			if not groups[4]: 
				del self.__class__._cached_groups[group] 
			self.top_group = None 
			self.background_self = None 
			self.foreground_group = None 
			self.foreground_decoration_group = None 
	### end workaround
	
	def update_batch(self, batch, group):
		self.delete()
		
		if not batch:
			batch = pyglet.graphics.Batch()
			self._own_batch = True
		else:
			self._own_batch = False
		
		self.batch = batch
		
		self._init_groups(group)
		self._update()

class EditableLabel(object):
	def __init__(self, text):
		self.document = pyglet.text.document.UnformattedDocument(text)
		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, 1, 1, multiline=False)
		self.caret = pyglet.text.caret.Caret(self.layout)
	
	def _get_text(self):
		return self.document.text
	def _set_text(self, text):
		self.document.text = text
	text = property(_get_text, _set_text)
	
	def update_batch(self, batch, group):
		self.caret.delete()
		self.layout.delete()
		
		### workaround for pyglet issue 408
		self.layout.batch = None
		if self.layout._document:
			self.layout._document.remove_handlers(self.layout)
		self.layout._document = None
		### end workaround
		
		self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, self.layout.width, self.layout.height, multiline=False, batch=batch, group=group)
		self.caret = pyglet.text.caret.Caret(self.layout)
		self.caret.visible = False
