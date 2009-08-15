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
		self._visible = visible
		self._batch = None
		self._patch = None
		self._vertices = None

	def _get_visible(self):
		return self._visible
	def _set_visible(self, visible):
		if visible != self.visible:
			self._visible = visible
			if visible:
				self._build()
			else:
				self._unbuild()
	visible = property(_get_visible, _set_visible)
	
	def _get_batch(self):
		return self._batch
	def _set_batch(self, batch):
		if batch != self.batch:
			self._unbuild()
			self._batch = batch
			self._build()
	batch = property(_get_batch, _set_batch)
	
	def _get_patch(self):
		return self._patch
	def _set_patch(self, patch):
		if patch != self.patch:
			self._unbuild()
			self._patch = patch
			self._build()
	patch = property(_get_patch, _set_patch)
	
	def _build(self):
		if self._batch and self._patch and self._visible:
			if self._vertices == None:
				self._vertices = self._patch.build_vertex_list(self._batch)
			self._patch.update_vertex_list_around(self._vertices, self.x, self.y, self.w, self.h)
	
	def _unbuild(self):
		if self._vertices != None:
			self._vertices.delete()
			self._vertices = None
	
	def update(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h
		
		if self._patch and self._batch and self._visible:
			self._patch.update_vertex_list_around(self._vertices, x, y, w, h)
	
	def update_in(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h
		
		if self._patch and self._batch and self._visible:
			self._patch.update_vertex_list(self._vertices, x, y, w, h)
