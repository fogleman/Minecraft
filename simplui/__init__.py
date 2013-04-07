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

"""simplui - a minimal GUI toolkit for pyglet

Intended purely as a tool for developers, to allow the
quick addition of GUIs for configuration and debug displays.

--------------------

See 'demo.py' in the enclosing directory for a brief tutorial.

--------------------

* Root element:
	The root GUI element must be a Frame, and the frame takes care
	of event handling:
	
	frame = Frame(w=window.width, h=window.height)
	window.push_handlers(frame)
	
	Every element has a name, which may be specified as a keyword
	argument to the constructor. You can use the frame to retrieve
	any named element:
	
	frame.add( Label('some text', name='my_label') )
	e = frame.get_element_by_name('my_label')
	
	Note that names must be unique within a single frame
	
* Containers:
	There are two types of containers provided by the library,
	list and single.
	
	List containers can contain an arbitrary number of elements,
	including other containers. The list containers provided are:
	
	+ Container - pixel positioning, does not auto-resize
	+ VerticalLayout - arranges elements vertically, auto-resizes
										 to fit contents
	
	Single containers can contain only a single item, typically
	another container. If you do not provide a content element,
	a Container will be created for you. The single containers
	provided are:
	
	+ Dialogue - floating window, resizes to fit contents
	+ FoldingBox - vertically collapsible box, resizes to fit contents

* Controls:
	A limitted set of controls is provided:
	
	+ Label - simple textual label
	+ Button - clickable button
	+ Checkbox - clickable 2-state checkbox, with text label
	+ TextInput - editable text field
	+ Slider - simple value slider
	
	Each of Button, Checkbox, TextInput and Slider have an action attribute.
	The action is a callback which will be invoked when the control is
	used (clicking for button or checkbox, end enditing for text input).
	The action may be provided as a keyword argument to the constructor:
	
	button = Button('Click Me!', action=my_function)

* Questions?
	Contact me on the web at http://swiftcoder.wordpress.com
	or by email to swiftcoder@gmail.com
	
	- Tristam MacDonald
"""

__author__ =  'Tristam MacDonald'
__version__=  '1.0.3'

from theme import Theme
from frame import Frame

from dialogue import Dialogue

from container import Container
from layout import HLayout, VLayout
from flow_layout import FlowLayout
from folding_box import FoldingBox

from label import Label
from checkbox import Checkbox
from button import Button
from text_input import TextInput
from slider import Slider
